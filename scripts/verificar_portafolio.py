#!/usr/bin/env python3
"""QA estática del portafolio ADL. No afirma pruebas en navegador."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from collections import Counter
import re

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "portafolio/index.html"
CSS = ROOT / "portafolio/portafolio.css"
JS = ROOT / "portafolio/portafolio.js"

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.tags = Counter()
        self.cards = []
        self.scopes = []
        self.lifecycles = []
        self.links = []
        self.images_missing_alt = []
        self.main_nav = 0

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        self.tags[tag] += 1
        if "id" in data:
            self.ids.append(data["id"])
        if tag == "article" and "catalog-card" in data.get("class", "").split():
            self.cards.append(data.get("data-state"))
            self.scopes.append(data.get("data-scope"))
            self.lifecycles.append(data.get("data-lifecycle"))
        if tag == "a":
            self.links.append(data)
        if tag == "img" and "alt" not in data:
            self.images_missing_alt.append(data.get("src"))
        if tag == "nav" and data.get("aria-label") == "Navegación principal":
            self.main_nav += 1

def check(condition, message):
    if not condition:
        raise AssertionError(message)

def main():
    html = HTML.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")
    doc = Inspector()
    doc.feed(html)
    counts = Counter(doc.cards)
    scope_counts = Counter(doc.scopes)
    progress_counts = Counter(doc.lifecycles)

    check(counts == {"publicados": 9, "desarrollo": 8, "pausados": 3}, f"Conteo incorrecto: {counts}")
    check(scope_counts == {"academico": 11, "empresarial": 3, "conocimiento": 6}, f"Clasificación incorrecta: {scope_counts}")
    for title in ("Académico e institucional · 11", "Comercial y consultoría · 3", "Laboratorio y divulgación · 6"):
        check(title in html, f"Falta selector de línea: {title}")
    check(progress_counts == {"produccion": 8, "desarrollo": 9, "pausa": 2, "planificado": 1},
          f"Estados de avance inconsistentes: {progress_counts}")
    for symbol in ("stage-live", "stage-build", "stage-pause", "stage-plan"):
        svg=(ROOT/'arias-data-lab/ui-icons.svg').read_text(encoding='utf-8')
        check(f'id="{symbol}"' in svg, f"Falta icono de estado: {symbol}")
        check(f'#' + symbol in html, f"Icono de etapa no referenciado: {symbol}")
    check(len(re.findall(r'class="adl-stage-legend"', html)) == 1,
          "Falta la leyenda visual de las cuatro etapas")
    check(html.count('class="adl-stage-icon"') >= 4,
          "Faltan iconos en leyenda o tarjetas")
    check('portafolio.css?v=2.4' in html, "Versión de estilos de estados desactualizada")
    project_cards = [
        m.group(0) for m in re.finditer(
            r'<article class="catalog-card"[^>]*>.*?</article>', html, re.S
        )
    ]
    check(len(project_cards) == 20, "Faltan fichas en el catálogo")
    check(all('data-naturaleza="' in card and 'data-acceso="' in card and 'class="adl-card-meta"' in card for card in project_cards), "Faltan metadatos de naturaleza/acceso visibles")
    check(html.count("<h3>INEM Analítica Académica</h3>") == 1, "Falta el piloto INEM Analítica Académica o está duplicado")
    for name in ("Tablero ICFES INEM", "Red Piezométrica"):
        matching = [card for card in project_cards if f"<h3>{name}</h3>" in card]
        check(len(matching) == 1, f"Tarjeta no única: {name}")
        check('data-lifecycle="desarrollo"' in matching[0],
              f"{name} no puede presentarse como producción certificada")
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    for internal in ("ADL Academic Core", "ADL Business Core", "Confort Térmico Oficina"):
        check(f"<h3>{internal}</h3>" not in html, f"Ficha interna o duplicada: {internal}")
    check(html.count("<h3>Confort Térmico Educativo</h3>") == 1, "El producto térmico debe aparecer una sola vez")
    check("aulas, oficinas y hogar" in html, "Faltan los ámbitos de confort térmico")
    check("<strong>Arias Data Lab</strong>" in home and "<strong>Arias Data Lab</strong>" in html,
          "La identidad visible debe usar Arias Data Lab")
    check("Arias-Data-Lab" not in home and "Arias-Data-Lab" not in html,
          "Persisten variantes de marca anteriores")
    check("ADL Academic Core" not in home and "ADL Business Core" not in home,
          "La portada no debe publicitar los núcleos arquitectónicos internos")
    check(len(doc.ids) == len(set(doc.ids)), "IDs HTML duplicados")
    check(doc.tags["h1"] == 1 and doc.tags["main"] == 1, "Jerarquía básica inválida")
    check(doc.main_nav == 1, "Navegación principal duplicada o ausente")
    check(not doc.images_missing_alt, f"Imágenes sin alt: {doc.images_missing_alt}")
    check(len(re.findall(r'class="card-foot"><a href="https://', html)) == 9, "Enlaces de proyectos incorrectos")
    check(len(re.findall(r'data-filter="', html)) == 4, "Faltan filtros de estado")
    check('id="portfolio-controls" hidden' in html, "La búsqueda debe degradar sin JavaScript")
    check('class="adl-scope-picker" hidden' in html and 'class="taxonomy-controls" hidden' in html,
          "Los filtros interactivos deben estar ocultos sin JavaScript")
    check("scopePicker.hidden = false" in js and "taxonomy.hidden = false" in js,
          "Los filtros interactivos deben mostrarse al inicializarse JavaScript")
    check('prefers-reduced-motion: reduce' in js and 'behavior: reducedMotion ? "auto" : "smooth"' in js,
          "El desplazamiento programático debe respetar movimiento reducido")
    check('aria-labelledby="status-filter-label"' in html, "Filtros sin etiqueta de grupo")
    check("adl-control-center.vercel.app" not in html, "El portafolio público expone el centro de gestión privado")
    check('portafolio.css?v=2.4' in html and 'portafolio.js?v=2.2' in html, "Versiones de recursos desfasadas")
    check('architecture.css?v=1.3' in html, "No carga la navegación del ecosistema")
    check('href="../observatorio-ia/"' in html and 'adl-editorial-signpost' in html, "Falta el observatorio agrupado")
    check(html.index('<h3>IA al Día</h3>') < html.index('<h3>Aula Inteligente</h3>'), "Las líneas editoriales no están juntas y ordenadas")
    card_markup = re.findall(r'<article class="catalog-card"[^>]*>.*?</article>', html, flags=re.S)
    check(any('data-scope="conocimiento"' in card and '<h3>Aula Inteligente</h3>' in card for card in card_markup), "Aula Inteligente no comparte la categoría de observatorio")
    check(len(re.findall(r'data-scope="', html)) == 23, "Faltan ámbitos en filtros o tarjetas")
    check(len(re.findall(r'class="adl-public-url"', html)) == 9, "No se muestran las nueve URLs documentadas")
    check('href="https://inemsimonbolivarsm.edu.co/icfes-inem/login.php"' in html,
          "Enlace institucional del Tablero ICFES INEM ausente")
    official = "https://inemsimonbolivarsm.edu.co/icfes-inem/login.php"
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    brochure = (ROOT / "proyectos/tablero-icfes-inem/index.html").read_text(encoding="utf-8")
    demo = (ROOT / "proyectos/tablero-icfes-inem/demo.html").read_text(encoding="utf-8")
    check(home.count('href="' + official + '"') >= 2,
          "Las dos tarjetas de portada deben enlazar al acceso institucional")
    check(brochure.count('href="' + official + '"') >= 2,
          "Ambos CTA de la ficha técnica deben enlazar al acceso institucional")
    check('href="' + official + '"' in demo,
          "La demostración histórica debe informar el acceso institucional")
    check('href="https://ljarias.github.io/tablero-icfes-inem/"' not in brochure,
          "Hay un enlace histórico incorrecto en la ficha técnica")
    check('href="proyectos/tablero-icfes-inem/demo.html"' not in home,
          "La portada aún redirige a la demostración sintética")
    check("Acceso institucional publicado" in home and
          "Acceso institucional publicado" in brochure,
          "Falta informar el estado institucional")
    check("URL de acceso: inemsimonbolivarsm.edu.co/icfes-inem/login.php" in html,
          "URL institucional ICFES no visible")
    check('selectedScope' in js and '.adl-scope-buttons button[data-scope]' in js, "Filtro por ámbito ausente o mal seleccionado")
    check((ROOT / "arias-data-lab/architecture.css").exists(), "Faltan estilos de arquitectura")
    check((ROOT / "arias-data-lab/ui-icons.svg").exists(), "Falta la colección de iconos")
    check("@media(max-width:700px)" in css and "@media(max-width:520px)" in css, "Faltan puntos de ruptura")
    check(".adl-portfolio [hidden]" in css, "Falta regla de ocultación de filtros")
    check('controls.hidden = false' in js, "No se activan controles con JS")
    check("const normalize" in js, "Falta normalización de búsqueda")
    check("ADL_STATE_GITHUB_TOKEN" not in html and "ADL_EDITOR_SECRET" not in html, "Referencias a secretos")
    for link in doc.links:
        if link.get("target") == "_blank":
            rel = set(link.get("rel", "").split())
            check({"noopener", "noreferrer"} <= rel, f"Enlace sin protección: {link.get('href')}")
    print("OK: 20 proyectos (9/8/3 por etapa; 11 académicos, 3 comerciales, 6 transversales).")
    print("Nueve URLs visibles, cuatro etapas (8/9/2/1), iconos, filtros, navegación y privacidad revisados.")
    print("Nota: QA estática; no es una prueba visual, HTTP ni auditoría WCAG completa.")

if __name__ == "__main__":
    main()

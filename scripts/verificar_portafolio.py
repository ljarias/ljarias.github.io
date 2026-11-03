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

    check(counts == {"publicados": 9, "desarrollo": 9, "pausados": 4}, f"Conteo incorrecto: {counts}")
    check(scope_counts == {"academico": 11, "empresarial": 4, "conocimiento": 7}, f"Clasificación incorrecta: {scope_counts}")
    for title in ("Académico e institucional · 11", "Comercial y consultoría · 4", "Laboratorio y divulgación · 7"):
        check(title in html, f"Falta selector de línea: {title}")
    check(len(doc.ids) == len(set(doc.ids)), "IDs HTML duplicados")
    check(doc.tags["h1"] == 1 and doc.tags["main"] == 1, "Jerarquía básica inválida")
    check(doc.main_nav == 1, "Navegación principal duplicada o ausente")
    check(not doc.images_missing_alt, f"Imágenes sin alt: {doc.images_missing_alt}")
    check(len(re.findall(r'class="card-foot"><a href="https://', html)) == 9, "Enlaces de proyectos incorrectos")
    check(len(re.findall(r'data-filter="', html)) == 4, "Faltan filtros de estado")
    check('id="portfolio-controls" hidden' in html, "La búsqueda debe degradar sin JavaScript")
    check('aria-labelledby="status-filter-label"' in html, "Filtros sin etiqueta de grupo")
    check('id="gestión-privada"' in html, "Se perdió el ancla de la versión anterior")
    check('portafolio.css?v=2.0' in html and 'portafolio.js?v=2.1' in html, "Versiones de recursos desfasadas")
    check('architecture.css?v=1.2' in html, "No carga la navegación del ecosistema")
    check('href="../observatorio-ia/"' in html and 'adl-editorial-signpost' in html, "Falta el observatorio agrupado")
    check(html.index('<h3>IA al Día</h3>') < html.index('<h3>Aula Inteligente</h3>'), "Las líneas editoriales no están juntas y ordenadas")
    card_markup = re.findall(r'<article class="catalog-card"[^>]*>.*?</article>', html, flags=re.S)
    check(any('data-scope="conocimiento"' in card and '<h3>Aula Inteligente</h3>' in card for card in card_markup), "Aula Inteligente no comparte la categoría de observatorio")
    check(len(re.findall(r'data-scope="', html)) == 25, "Faltan ámbitos en filtros o tarjetas")
    check(len(re.findall(r'class="adl-public-url"', html)) == 9, "No se muestran las nueve URLs documentadas")
    check('href="https://inemsimonbolivarsm.edu.co/icfes-inem/login.php"' in html,
          "Enlace institucional del Tablero ICFES INEM ausente")
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
    print("OK: 22 proyectos (9/9/4 por etapa; 11 académicos, 4 comerciales, 7 transversales).")
    print("Nueve URLs visibles, filtros combinables, navegación, iconos y privacidad revisados.")
    print("Nota: QA estática; no es una prueba visual, HTTP ni auditoría WCAG completa.")

if __name__ == "__main__":
    main()

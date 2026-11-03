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

    check(counts == {"publicados": 9, "desarrollo": 9, "pausados": 4}, f"Conteo incorrecto: {counts}")
    check(len(doc.ids) == len(set(doc.ids)), "IDs HTML duplicados")
    check(doc.tags["h1"] == 1 and doc.tags["main"] == 1, "Jerarquía básica inválida")
    check(doc.main_nav == 1, "Navegación principal duplicada o ausente")
    check(not doc.images_missing_alt, f"Imágenes sin alt: {doc.images_missing_alt}")
    check(len(re.findall(r'class="card-foot"><a href="https://', html)) == 9, "Enlaces de proyectos incorrectos")
    check(len(re.findall(r'data-filter="', html)) == 4, "Faltan filtros de estado")
    check('id="portfolio-controls" hidden' in html, "La búsqueda debe degradar sin JavaScript")
    check('aria-labelledby="status-filter-label"' in html, "Filtros sin etiqueta de grupo")
    check('id="gestión-privada"' in html, "Se perdió el ancla de la versión anterior")
    check('portafolio.css?v=2.0' in html and 'portafolio.js?v=2.0' in html, "Versiones de recursos desfasadas")
    check("@media(max-width:700px)" in css and "@media(max-width:520px)" in css, "Faltan puntos de ruptura")
    check(".adl-portfolio [hidden]" in css, "Falta regla de ocultación de filtros")
    check('controls.hidden = false' in js, "No se activan controles con JS")
    check("const normalize" in js, "Falta normalización de búsqueda")
    check("ADL_STATE_GITHUB_TOKEN" not in html and "ADL_EDITOR_SECRET" not in html, "Referencias a secretos")
    for link in doc.links:
        if link.get("target") == "_blank":
            rel = set(link.get("rel", "").split())
            check({"noopener", "noreferrer"} <= rel, f"Enlace sin protección: {link.get('href')}")
    print("OK: 22 proyectos (9/9/4), nueve enlaces, navegación, filtros y privacidad revisados.")
    print("Nota: QA estática; no es una prueba visual, HTTP ni auditoría WCAG completa.")

if __name__ == "__main__":
    main()

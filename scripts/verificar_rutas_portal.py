#!/usr/bin/env python3
"""Verifica la portada corporativa y las rutas Jekyll de IA al Día.

Ejecutar antes y después de compilar Jekyll:
  python3 scripts/verificar_rutas_portal.py
  python3 scripts/verificar_rutas_portal.py --built
Sin dependencias externas.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "_site"
BUILT = "--built" in sys.argv
ISSUES: list[str] = []
ARTICLES = [
    "2026/09/15/bienvenida",
    "2026/09/15/ia-al-dia",
    "2026/09/16/ia-al-dia",
    "2026/09/28/ia-al-dia",
    "2026/10/04/ia-al-dia",
    "2026/10/11/ia-al-dia",
]

def verify(condition: bool, message: str) -> None:
    if not condition:
        ISSUES.append(message)

def source(path: str) -> str:
    f = ROOT / path
    verify(f.is_file(), f"Falta el archivo fuente {path}")
    return f.read_text(encoding="utf-8") if f.exists() else ""

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[str] = []
        self.ids: set[str] = set()
        self.h1 = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "h1":
            self.h1 += 1
        for field in ("href", "src"):
            if a.get(field) and tag in ("a", "img", "link", "script"):
                self.links.append(a[field])

config = source("_config.yml")
verify('title: "Arias-Data-Lab"' in config, "La identidad Jekyll no es Arias-Data-Lab")
verify("permalink: /ia-al-dia/:year/:month/:day/:title/" in config, "Permalink de noticias fuera de /ia-al-dia/")
verify('url: "https://ljarias.github.io"' in config, "URL canónica del sitio no definida")
verify(not (ROOT / "index.md").exists(), "index.md heredado entra en conflicto con index.html")

home = source("index.html")
verify("<title>Arias-Data-Lab" in home and 'href="ia-al-dia/"' in home, "La portada no enlaza el observatorio")
verify("arias-data-lab/productos/" in home, "La portada no enlaza el catálogo")
verify('href="arias-data-lab/portal.css?' in home, "La portada no aplica el CSS corporativo")
verify("meta http-equiv=\"refresh\"" not in home, "La portada principal no debe redirigir")
verify("ADL_logo-maestro-color_EDITABLE_v4.0.svg" in home, "Logo vectorial oficial ausente de la portada")
verify(not re.search(r'href=["\']https://github.com/ljarias/(?:prestamos-saas|acceso-escolar-inem)', home),
       "La portada enlaza repositorios privados")

for p, marker in [
    ("ia-al-dia/index.md", "permalink: /ia-al-dia/"),
    ("ia-al-dia/acerca.md", "permalink: /ia-al-dia/acerca/"),
    ("ia-al-dia/telemetria.md", "permalink: /ia-al-dia/telemetria/"),
]:
    verify(marker in source(p), f"Destino {p} no configurado")
verify("permalink: /acerca/" not in source("ia-al-dia/acerca.md"), "Ruta antigua en acerca")
verify("permalink: /telemetria/" not in source("ia-al-dia/telemetria.md"), "Ruta antigua en telemetria")

layout = source("_layouts/default.html")
post = source("_layouts/post.html")
for endpoint in ("/ia-al-dia/", "/ia-al-dia/acerca/", "/ia-al-dia/telemetria/"):
    verify(endpoint in layout, f"Falta navegación hacia {endpoint}")
verify("'/ia-al-dia/'" in post, "No se actualizó el retorno desde una publicación")

data = json.loads(source("_data/infografias.json"))
verify(len(data) > 0, "Sin registros de infografías")
for entry in data:
    verify(entry["post_url"].startswith("/ia-al-dia/20"), f"Enlace viejo de infografía: {entry['post_url']}")
verify('post_url = f"/ia-al-dia/' in source("scripts/generar_infografia.py"), "El generador aún produce enlaces antiguos")

for slug in ARTICLES:
    filename = "rutas-anteriores/" + slug.replace("/", "-") + ".html"
    if slug.endswith("bienvenida"):
        filename = "rutas-anteriores/2026-09-15-bienvenida.html"
    body = source(filename)
    verify("permalink: /" + slug + "/" in body and "/ia-al-dia/" + slug + "/" in body,
           f"Redirección histórica errónea {slug}")
for path,old,new in [
    ("rutas-anteriores/acerca-ia.html","/acerca/","/ia-al-dia/acerca/"),
    ("rutas-anteriores/telemetria-ia.html","/telemetria/","/ia-al-dia/telemetria/"),
]:
    text = source(path)
    verify("permalink: " + old in text and new in text, "Redirección histórica incorrecta "+path)

alias = source("arias-data-lab/index.html")
verify('https://ljarias.github.io/' in alias and "location.hash" in alias, "Falta alias del portal previo")

if BUILT:
    def generated(path: str) -> str:
        f = PUBLIC / path
        verify(f.is_file(), f"Jekyll no produjo {path}")
        return f.read_text(encoding="utf-8") if f.exists() else ""

    root = generated("index.html")
    ia = generated("ia-al-dia/index.html")
    verify("Tecnología para" in root, "La portada compilada no es corporativa")
    verify("Entender la IA exige" in ia, "El observatorio compilado carece de su portada")
    verify("portal.css" in root, "CSS ausente en portada raíz")
    generated("ia-al-dia/acerca/index.html")
    generated("ia-al-dia/telemetria/index.html")
    generated("arias-data-lab/index.html")

    for slug in ARTICLES:
        generated("ia-al-dia/" + slug + "/index.html")
        redirect_page = generated(slug + "/index.html")
        verify("/ia-al-dia/" + slug + "/" in redirect_page, "Ruta antigua no redirige: "+slug)

    generated("acerca/index.html")
    generated("telemetria/index.html")

    for path in (
        "index.html", "ia-al-dia/index.html", "ia-al-dia/acerca/index.html",
        "arias-data-lab/productos/index.html",
        "arias-data-lab/productos/prestamos-saas.html",
        "arias-data-lab/productos/acceso-escolar-inem.html",
        "banco-problemas-caribe/index.html",
    ):
        doc = generated(path)
        parser = LinkParser()
        parser.feed(doc)
        verify(parser.h1 >= 1 if path == "banco-problemas-caribe/index.html" else parser.h1 == 1,
               f"Encabezado principal incorrecto en {path}: {parser.h1}")
        for url in parser.links:
            if url.startswith(("https:", "http:", "mailto:", "data:", "tel:", "{{")):
                continue
            parsed = urlsplit(url)
            if not parsed.path and parsed.fragment and parsed.fragment not in parser.ids:
                ISSUES.append(f"Ancla interna sin destino: {path} → #{parsed.fragment}")
            if url.startswith("#") or not parsed.path:
                continue
            # Se comprueba existencia del destino local, sin confundir rutas Jekyll con externas.
            resolved = (PUBLIC / unquote(parsed.path.lstrip("/"))) if parsed.path.startswith("/") else (PUBLIC / path).parent / unquote(parsed.path)
            if not resolved.suffix:
                resolved = resolved / "index.html"
            verify(resolved.exists(), f"Enlace/recurso local roto: {path} → {url}")

if ISSUES:
    print(f"Falló la validación ({len(ISSUES)} problemas):")
    for issue in ISSUES:
        print(" -", issue)
    sys.exit(1)
print("OK: portada raíz corporativa, IA al Día independiente, enlaces, redirecciones y automatización preservados." + (" Jekyll compilado y comprobado." if BUILT else ""))

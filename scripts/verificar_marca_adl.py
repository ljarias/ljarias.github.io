#!/usr/bin/env python3
"""Verificación estática de identidad Arias-Data-Lab v4.0.

No usa red, no necesita dependencias externas, no modifica archivos.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "assets/brand/logo/v4.0"
MASTER = "ADL_logo-maestro-color_EDITABLE_v4.0.svg"
ISOTYPE = "ADL_isotipo-cuadrado_EDITABLE_v4.0.svg"
PAGES = [
    "_layouts/default.html",
    "arias-data-lab/index.html",
    "arias-data-lab/productos/index.html",
    "arias-data-lab/productos/prestamos-saas.html",
    "arias-data-lab/productos/acceso-escolar-inem.html",
    "banco-problemas-caribe/index.html",
    "banco-problemas-caribe/acerca-de.html",
    "banco-problemas-caribe/guia-documentacion.html",
    "banco-problemas-caribe/prompt-maestro.html",
]

errors = []

def verify(condition: bool, description: str) -> None:
    if not condition:
        errors.append(description)

manifest = json.loads((BRAND / "manifest.json").read_text(encoding="utf-8"))
verify(manifest.get("canonical") == MASTER, "El archivo maestro declarado no coincide")
verify(len(manifest.get("files", [])) == 6, "Se esperan seis variantes oficiales")

for record in manifest.get("files", []):
    p = BRAND / record["name"]
    verify(p.is_file(), f"Falta archivo vectorial: {p}")
    if not p.is_file():
        continue
    data = p.read_bytes()
    verify(hashlib.sha256(data).hexdigest() == record["sha256"],
           f"El SVG difiere del kit aprobado: {p}")
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        errors.append(f"SVG XML inválido: {p} ({exc})")
        continue
    verify(root.tag.endswith("}svg"), f"Elemento raíz no SVG: {p}")
    tags = [el.tag.rsplit("}", 1)[-1] for el in root.iter()]
    verify("path" in tags, f"No hay trazados editables: {p}")
    verify(not any(tag in ("image", "script", "foreignObject") for tag in tags),
           f"SVG incluye recursos incrustados o código no permitido: {p}")
    if record["name"] == MASTER:
        verify(tags.count("path") == 25 and tags.count("linearGradient") == 13,
               "El maestro no conserva los 25 trazados y 13 degradados")

for page in PAGES:
    p = ROOT / page
    verify(p.is_file(), f"Falta página: {page}")
    if not p.is_file():
        continue
    body = p.read_text(encoding="utf-8")
    verify(MASTER in body, f"Falta logo SVG v4 en {page}")
    verify(ISOTYPE in body, f"Falta isotipo SVG v4 en {page}")
    verify("logo-adl-v3.webp" not in body, f"Logo WebP antiguo aún activo en {page}")
    verify('type="image/svg+xml"' in body, f"Falta declaración favicon SVG en {page}")
    verify("favicon-32.png" in body, f"Falta favicon PNG de respaldo en {page}")
    if page.startswith("arias-data-lab/"):
        verify(not re.search(r'href=["\']https://github.com/ljarias/(?:prestamos-saas|acceso-escolar-inem)', body),
               f"Enlace público hacia repo privado en {page}")
    for match in re.finditer(r'(?:\.\./)+assets/brand/logo/v4\.0/[\w.-]+\.svg|/assets/brand/logo/v4\.0/[\w.-]+\.svg', body):
        value = match.group(0)
        if value.startswith("{{"):
            continue
        path = (ROOT / value.lstrip("/")) if value.startswith("/") else (p.parent / value)
        verify(path.is_file(), f"Ruta SVG no resuelta en {page}: {value}")

if errors:
    print(f"ERROR: {len(errors)} comprobaciones de identidad no superadas", file=sys.stderr)
    for error in errors:
        print(f" - {error}", file=sys.stderr)
    sys.exit(1)
print(f"OK: {len(manifest['files'])} SVG oficiales íntegros y {len(PAGES)} páginas migradas; repositorios privados no enlazados.")

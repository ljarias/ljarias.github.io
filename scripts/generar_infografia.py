from __future__ import annotations

import base64
import json
import os
import re
import urllib.request
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent
STYLE_PROMPT_PATH = ROOT / "prompts" / "infografia_ia.md"
POSTS_DIR = ROOT / "_posts"
INFO_DIR = ROOT / "assets" / "infografias"
DATA_PATH = ROOT / "_data" / "infografias.json"
TZ = ZoneInfo("America/Bogota")
MODEL = os.getenv("INFOGRAPHIC_MODEL", "gpt-image-2.5-flare-2026-09-08")
FORCE = os.getenv("FORCE_INFOGRAFIA", "false").lower() in {"1", "true", "yes", "si", "sí"}

MONTHS = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]


def strip_md(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"[*_`>#]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def short(text: str, limit: int = 210) -> str:
    text = strip_md(text)
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(".,;:")
    return cut + "…"


def section(block: str, heading: str) -> str:
    pattern = rf"^###\s+{re.escape(heading)}\s*\n(.*?)(?=^###\s+|\Z)"
    match = re.search(pattern, block, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def extract_news(markdown: str) -> list[dict]:
    pattern = r"^##\s+(\d+)\.\s+(.+?)\s*\n(.*?)(?=^##\s+\d+\.|^##\s+Semáforo|^##\s+Concepto|^##\s+Tres preguntas|^##\s+Nota editorial|\Z)"
    items = []
    for number, title, block in re.findall(pattern, markdown, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE):
        tipo = re.search(r"\*\*Tipo:\*\*\s*([^\n]+)", block, flags=re.IGNORECASE)
        tema = re.search(r"\*\*Tema:\*\*\s*([^\n]+)", block, flags=re.IGNORECASE)
        occurred = section(block, "Qué ocurrió")
        items.append({
            "number": number,
            "title": short(title, 80),
            "type": short(tipo.group(1), 42) if tipo else "NOTICIA",
            "topic": short(tema.group(1), 55) if tema else "Inteligencia artificial",
            "summary": short(occurred, 240) if occurred else short(block, 240),
        })
    return items[:6]


def extract_semaphore(markdown: str) -> list[str]:
    match = re.search(r"^##\s+Semáforo de la jornada\s*\n(.*?)(?=^##\s+|\Z)", markdown, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if not match:
        return []
    lines = []
    for line in match.group(1).splitlines():
        line = strip_md(line.lstrip("- "))
        if line:
            lines.append(short(line, 90))
    return lines[:3]


def source_names(markdown: str) -> list[str]:
    domains = []
    for url in re.findall(r"https?://[^\s)\]>\"']+", markdown):
        host = urlparse(url.rstrip(".,;:")).netloc.lower().removeprefix("www.")
        if host and host not in domains:
            domains.append(host)
    pretty = {
        "reuters.com": "Reuters",
        "apnews.com": "Associated Press",
        "bbc.com": "BBC",
        "bbc.co.uk": "BBC",
        "nature.com": "Nature",
        "science.org": "Science",
        "unesco.org": "UNESCO",
        "oecd.org": "OECD",
        "nist.gov": "NIST",
    }
    names = []
    for domain in domains:
        name = pretty.get(domain, domain)
        if name not in names:
            names.append(name)
    return names[:5]


def load_metadata() -> list[dict]:
    if not DATA_PATH.exists():
        return []
    try:
        data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def save_metadata(record: dict) -> None:
    rows = [row for row in load_metadata() if row.get("date") != record["date"]]
    rows.append(record)
    rows.sort(key=lambda row: row.get("date", ""))
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(rows[-120:], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Falta OPENAI_API_KEY; no se puede generar la infografía.")

    now = datetime.now(TZ)
    date_iso = now.date().isoformat()
    human_date = f"{now.day} de {MONTHS[now.month - 1]} de {now.year}"
    post_path = POSTS_DIR / f"{date_iso}-ia-al-dia.md"
    if not post_path.exists():
        print(f"No existe {post_path.relative_to(ROOT)}. No hay infografía para generar.")
        return

    INFO_DIR.mkdir(parents=True, exist_ok=True)
    image_path = INFO_DIR / f"{date_iso}.png"
    post_url = f"/{now:%Y/%m/%d}/ia-al-dia/"

    if image_path.exists() and not FORCE:
        save_metadata({
            "date": date_iso,
            "title": f"Infografía IA al Día — {human_date}",
            "image": f"/assets/infografias/{date_iso}.png",
            "post_url": post_url,
            "alt": f"Infografía con el resumen de noticias de inteligencia artificial del {human_date}",
            "model": MODEL,
        })
        print(f"La infografía de hoy ya existe: {image_path.relative_to(ROOT)}")
        return

    markdown = post_path.read_text(encoding="utf-8")
    news = extract_news(markdown)
    if len(news) < 3:
        raise RuntimeError("No se pudieron extraer suficientes noticias del resumen diario.")

    style = STYLE_PROMPT_PATH.read_text(encoding="utf-8")
    semaphore = extract_semaphore(markdown)
    sources = source_names(markdown)

    news_text = "\n\n".join(
        f"{item['number']}. {item['title']}\nTipo: {item['type']}\nTema: {item['topic']}\nResumen autorizado: {item['summary']}"
        for item in news
    )
    sem_text = "\n".join(f"- {item}" for item in semaphore) or "- Seguridad y control\n- Empleo y regulación\n- Educación y oportunidades"
    source_text = ", ".join(sources) if sources else "Fuentes enlazadas en la edición diaria"

    prompt = f"""
{style}

FECHA QUE DEBE APARECER: {human_date}

CONTENIDO AUTORIZADO. Usa únicamente estas noticias; no inventes cifras, nombres ni hechos adicionales:

{news_text}

SEMÁFORO AUTORIZADO:
{sem_text}

FUENTES PARA EL PIE: {source_text}

Regla de fidelidad: si el espacio no alcanza, reduce el texto de los resúmenes, pero conserva los títulos y el sentido. No agregues datos nuevos. Mantén todo el texto en español correcto y muy legible.
""".strip()

    client = OpenAI()
    result = client.images.generate(
        model=MODEL,
        prompt=prompt,
        size="1024x1536",
        quality="medium",
    )

    item = result.data[0]
    image_bytes = None
    b64 = getattr(item, "b64_json", None)
    url = getattr(item, "url", None)
    if b64:
        image_bytes = base64.b64decode(b64)
    elif url:
        with urllib.request.urlopen(url, timeout=120) as response:
            image_bytes = response.read()

    if not image_bytes:
        raise RuntimeError("La API de imágenes no devolvió una imagen utilizable.")

    image_path.write_bytes(image_bytes)
    save_metadata({
        "date": date_iso,
        "title": f"Infografía IA al Día — {human_date}",
        "image": f"/assets/infografias/{date_iso}.png",
        "post_url": post_url,
        "alt": f"Infografía con el resumen de noticias de inteligencia artificial del {human_date}",
        "model": MODEL,
    })

    print(f"Infografía generada: {image_path.relative_to(ROOT)}")
    print(f"Modelo: {MODEL}")
    print(f"Noticias resumidas: {len(news)}")


if __name__ == "__main__":
    main()

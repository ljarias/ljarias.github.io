from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent
PROMPT_PATH = ROOT / "prompts" / "editor_ia.md"
HISTORY_PATH = ROOT / "data" / "historial.json"
POSTS_DIR = ROOT / "_posts"
TZ = ZoneInfo("America/Bogota")
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")

MONTHS = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]


def load_history() -> list[dict]:
    if not HISTORY_PATH.exists():
        return []
    try:
        return json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def clean_markdown(text: str) -> str:
    text = text.strip()
    if text.startswith("```markdown"):
        text = text[len("```markdown"):]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


def yaml_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def extract_urls(markdown: str) -> list[str]:
    urls = re.findall(r"https?://[^\s)\]>\"']+", markdown)
    return sorted(set(url.rstrip(".,;:") for url in urls))


def extract_titles(markdown: str) -> list[str]:
    found = re.findall(r"^##\s+\d+\.\s+(.+)$", markdown, flags=re.MULTILINE)
    return [re.sub(r"[*_`]", "", title).strip() for title in found]


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit(
            "Falta OPENAI_API_KEY. Configúrala como secreto de GitHub Actions antes de ejecutar el agente."
        )

    now = datetime.now(TZ)
    date_iso = now.date().isoformat()
    human_date = f"{now.day} de {MONTHS[now.month - 1]} de {now.year}"

    editorial_prompt = PROMPT_PATH.read_text(encoding="utf-8")
    history = load_history()
    recent_history = history[-30:]

    context = {
        "fecha_actual": date_iso,
        "zona_horaria": "America/Bogota",
        "ediciones_recientes": recent_history,
    }

    input_text = f"""
{editorial_prompt}

## Contexto de esta ejecución

Hoy es {human_date}. Busca información reciente a nivel mundial y prioriza desarrollos de las últimas 24 a 36 horas.

Para reducir duplicados, esta es la memoria editorial de las últimas ediciones:

{json.dumps(context, ensure_ascii=False, indent=2)}

Si un tema ya aparece allí, inclúyelo solamente si hay un desarrollo nuevo y sustancial. Comprueba las fechas de publicación y, cuando sea posible, la fecha real del acontecimiento.
""".strip()

    client = OpenAI()
    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "low"},
        tools=[{"type": "web_search_preview", "search_context_size": "medium"}],
        input=input_text,
        max_output_tokens=6500,
    )

    body = clean_markdown(response.output_text or "")
    if len(body) < 500:
        raise RuntimeError("La respuesta del agente fue demasiado corta; se cancela la publicación.")

    title = f"IA al Día — {human_date}"
    summary = (
        "Selección diaria de noticias mundiales sobre inteligencia artificial, "
        "con contexto, riesgos, oportunidades y preguntas para el aula."
    )

    front_matter = f'''---\nlayout: post\ntitle: "{yaml_escape(title)}"\ndate: {now.strftime('%Y-%m-%d %H:%M:%S %z')}\nsummary: "{yaml_escape(summary)}"\nreading_time: "8–12 min"\ncategories: [ia, noticias, educacion]\n---\n\n'''

    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    post_path = POSTS_DIR / f"{date_iso}-ia-al-dia.md"
    post_path.write_text(front_matter + body + "\n", encoding="utf-8")

    record = {
        "date": date_iso,
        "post": str(post_path.relative_to(ROOT)),
        "titles": extract_titles(body)[:7],
        "urls": extract_urls(body)[:40],
        "model": MODEL,
    }

    history = [item for item in history if item.get("date") != date_iso]
    history.append(record)
    history = history[-120:]

    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_PATH.write_text(
        json.dumps(history, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Publicación generada: {post_path.relative_to(ROOT)}")
    print(f"Noticias detectadas: {len(record['titles'])}")
    print(f"URLs registradas: {len(record['urls'])}")


if __name__ == "__main__":
    main()

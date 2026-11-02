from __future__ import annotations

import json
import math
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent
PROMPT_PATH = ROOT / "prompts" / "editor_aula_inteligente.md"
POSTS_DIR = ROOT / "_posts"
INFO_DIR = ROOT / "assets" / "infografias"
HISTORY_PATH = ROOT / "data" / "aula_inteligente_historial.json"
TZ = ZoneInfo("America/Bogota")
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")


def load_history() -> list[dict]:
    if not HISTORY_PATH.exists():
        return []
    try:
        value = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
        return value if isinstance(value, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def yaml_escape(value: str) -> str:
    return str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def clean_body(text: str) -> str:
    text = text.strip()
    text = re.sub(r"```(?:markdown)?\s*", "", text, flags=re.IGNORECASE)
    return text.replace("```", "").strip()


def parse_chart(text: str) -> tuple[dict, str]:
    match = re.search(r"DATA_CHART_START\s*(\{.*?\})\s*DATA_CHART_END", text, flags=re.DOTALL)
    if not match:
        raise RuntimeError("La respuesta no incluyó un bloque DATA_CHART válido.")
    try:
        chart = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise RuntimeError("El bloque DATA_CHART no es JSON válido.") from exc
    labels = chart.get("labels")
    values = chart.get("values")
    if not isinstance(labels, list) or not isinstance(values, list) or not 2 <= len(labels) <= 8 or len(labels) != len(values):
        raise RuntimeError("La gráfica debe tener entre 2 y 8 categorías y valores coincidentes.")
    if not all(isinstance(label, str) and label.strip() for label in labels):
        raise RuntimeError("Las etiquetas de la gráfica no son válidas.")
    numeric = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
            raise RuntimeError("La gráfica contiene valores no numéricos o negativos.")
        numeric.append(float(value))
    chart["values"] = numeric
    for required in ("title", "unit", "source", "sample", "caption"):
        if not isinstance(chart.get(required), str) or not chart[required].strip():
            raise RuntimeError(f"Falta el campo de gráfica: {required}.")
    body = re.sub(r"\n?DATA_CHART_START\s*\{.*?\}\s*DATA_CHART_END\s*", "\n", text, flags=re.DOTALL).strip()
    return chart, clean_body(body)


def esc(value: str) -> str:
    return (str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def wrap(text: str, width: int) -> list[str]:
    words = str(text).split()
    lines, line = [], ""
    for word in words:
        if line and len(line) + 1 + len(word) > width:
            lines.append(line)
            line = word
        else:
            line = (line + " " + word).strip()
    if line:
        lines.append(line)
    return lines or [""]


def make_svg(chart: dict, date_iso: str) -> str:
    width, height = 1200, 860
    margin_left, chart_top, chart_bottom = 105, 240, 650
    values = chart["values"]
    maximum = max(values) or 1
    scale_max = maximum * 1.15
    count = len(values)
    band = 1000 / count
    bar_width = min(72, band * 0.52)
    colors = ["#2F6BFF", "#16A6A0", "#F26B5E", "#7C5CFC", "#F2B84B", "#3BA272", "#D14D72", "#5B8FF9"]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">']
    parts += [f'<title id="title">{esc(chart["title"])}</title>', f'<desc id="desc">{esc(chart["caption"])}</desc>', '<rect width="100%" height="100%" fill="#F7F8FC"/>']
    parts.append(f'<text x="80" y="78" font-family="Arial,sans-serif" font-size="34" font-weight="700" fill="#132238">{esc(chart["title"])}</text>')
    parts.append(f'<text x="80" y="118" font-family="Arial,sans-serif" font-size="21" fill="#667085">Aula Inteligente · {date_iso}</text>')
    for tick in range(5):
        value = scale_max * tick / 4
        y = chart_bottom - (chart_bottom - chart_top) * tick / 4
        parts.append(f'<line x1="{margin_left}" y1="{y:.1f}" x2="1110" y2="{y:.1f}" stroke="#D0D5DD" stroke-width="1"/>')
        parts.append(f'<text x="82" y="{y+7:.1f}" text-anchor="end" font-family="Arial,sans-serif" font-size="17" fill="#667085">{value:.0f}{esc(chart["unit"])}</text>')
    for index, (label, value) in enumerate(zip(chart["labels"], values)):
        x = margin_left + band * index + band / 2
        bar_height = (chart_bottom - chart_top) * value / scale_max
        y = chart_bottom - bar_height
        color = colors[index % len(colors)]
        parts.append(f'<rect x="{x-bar_width/2:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{bar_height:.1f}" rx="12" fill="{color}"/>')
        parts.append(f'<text x="{x:.1f}" y="{max(y-14, chart_top-8):.1f}" text-anchor="middle" font-family="Arial,sans-serif" font-size="22" font-weight="700" fill="{color}">{value:g}{esc(chart["unit"])}</text>')
        label_lines = wrap(label, 15)
        for line_index, line in enumerate(label_lines[:2]):
            parts.append(f'<text x="{x:.1f}" y="{chart_bottom+38+line_index*23}" text-anchor="middle" font-family="Arial,sans-serif" font-size="16" fill="#1D2939">{esc(line)}</text>')
    caption_lines = wrap(chart["caption"], 92)
    y = 760
    for line in caption_lines[:2]:
        parts.append(f'<text x="80" y="{y}" font-family="Arial,sans-serif" font-size="16" fill="#344054">{esc(line)}</text>')
        y += 22
    parts.append(f'<text x="80" y="825" font-family="Arial,sans-serif" font-size="14" fill="#667085">Fuente: {esc(chart["source"])} · {esc(chart["sample"])}</text>')
    parts.append('</svg>')
    return "\n".join(parts)


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Falta OPENAI_API_KEY en los secretos de GitHub Actions.")
    now = datetime.now(TZ)
    date_iso = now.date().isoformat()
    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    history = load_history()[-10:]
    context = json.dumps({"fecha": date_iso, "zona_horaria": "America/Bogota", "ediciones_anteriores": history}, ensure_ascii=False, indent=2)
    input_text = f"{prompt}\n\n## Contexto de ejecución\nHoy es {date_iso}. Investiga las últimas 24–48 horas, sin repetir una historia anterior salvo que exista un desarrollo sustancial.\n\n{context}"
    client = OpenAI()
    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "low"},
        tools=[{"type": "web_search_preview", "search_context_size": "medium"}],
        input=input_text,
        max_output_tokens=7000,
    )
    chart, body = parse_chart(response.output_text or "")
    if len(body) < 700:
        raise RuntimeError("La edición generada es demasiado corta para publicarse.")
    title = f"Aula Inteligente — {chart['title']}"
    summary = "Noticias diarias sobre inteligencia artificial y educación, con fuentes verificables, contexto pedagógico y una gráfica de datos." 
    front = (
        "---\nlayout: post\n"
        f'title: "{yaml_escape(title)}"\n'
        f"date: {now.strftime('%Y-%m-%d %H:%M:%S %z')}\n"
        f'summary: "{yaml_escape(summary)}"\n'
        'reading_time: "5–8 min"\n'
        'categories: ["aula-inteligente", "ia", "educacion", "diario"]\n'
        f'chart_image: "/assets/infografias/aula-{date_iso}.svg"\n'
        f'chart_alt: "{yaml_escape(chart["title"] + ". " + chart["caption"])}"\n---\n\n'
    )
    POSTS_DIR.mkdir(exist_ok=True)
    INFO_DIR.mkdir(parents=True, exist_ok=True)
    post_path = POSTS_DIR / f"{date_iso}-aula-inteligente.md"
    svg_path = INFO_DIR / f"aula-{date_iso}.svg"
    post_path.write_text(front + body + "\n", encoding="utf-8")
    svg_path.write_text(make_svg(chart, date_iso), encoding="utf-8")
    history = [item for item in history if item.get("date") != date_iso]
    history.append({"date": date_iso, "title": title, "source": chart["source"], "chart": str(svg_path.relative_to(ROOT))})
    HISTORY_PATH.parent.mkdir(exist_ok=True)
    HISTORY_PATH.write_text(json.dumps(history[-120:], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Edición diaria generada: {post_path.relative_to(ROOT)}")
    print(f"Gráfica generada: {svg_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

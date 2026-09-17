from __future__ import annotations

import html
import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "_posts"
INFO_DIR = ROOT / "assets" / "infografias"
DATA_PATH = ROOT / "_data" / "infografias.json"
TZ = ZoneInfo("America/Bogota")
FORCE = os.getenv("FORCE_INFOGRAFIA", "false").lower() in {"1", "true", "yes", "si", "sí"}

MONTHS = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]

COLORS = [
    ("#FDE8EC", "#E9365A", "#7F1D2D"),
    ("#E5F2FF", "#1376C5", "#103B66"),
    ("#FFF3C9", "#F2B705", "#6B4F00"),
    ("#EDE8FF", "#6748C8", "#36256C"),
    ("#DCF7EA", "#078766", "#064E3B"),
    ("#FFE5EC", "#EC2E62", "#7A1735"),
]


def esc(text: str) -> str:
    return html.escape(text, quote=True)


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


def wrap(text: str, max_chars: int, max_lines: int) -> list[str]:
    words = strip_md(text).split()
    lines, current = [], []
    for word in words:
        trial = " ".join(current + [word])
        if len(trial) <= max_chars or not current:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]
            if len(lines) >= max_lines:
                break
    if len(lines) < max_lines and current:
        lines.append(" ".join(current))
    consumed = sum(len(line.split()) for line in lines)
    if consumed < len(words) and lines:
        lines[-1] = lines[-1].rstrip(".,;:") + "…"
    return lines[:max_lines]


def section(block: str, heading: str) -> str:
    pattern = rf"^###\s+{re.escape(heading)}\s*\n(.*?)(?=^###\s+|\Z)"
    match = re.search(pattern, block, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def extract_news(markdown: str) -> list[dict]:
    pattern = (
        r"^##\s+(\d+)\.\s+(.+?)\s*\n(.*?)"
        r"(?=^##\s+\d+\.|^##\s+Los tres temas|^##\s+Semáforo|^##\s+Concepto|^##\s+Cinco preguntas|^##\s+Tres preguntas|^##\s+Nota editorial|\Z)"
    )
    items = []
    for number, title, block in re.findall(pattern, markdown, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE):
        tipo = re.search(r"\*\*Tipo:\*\*\s*([^\n]+)", block, flags=re.IGNORECASE)
        tema = re.search(r"\*\*Tema:\*\*\s*([^\n]+)", block, flags=re.IGNORECASE)
        criticality = re.search(r"\*\*Nivel de criticidad:\*\*\s*([^\n]+)", block, flags=re.IGNORECASE)
        occurred = section(block, "Qué ocurrió")
        topic = short(tema.group(1), 34) if tema else "IA"
        if criticality:
            topic = f"{topic} · {short(criticality.group(1), 10)}"
        items.append({
            "number": number,
            "title": short(title, 88),
            "type": short(tipo.group(1), 34) if tipo else "NOTICIA",
            "topic": topic,
            "summary": short(occurred, 260) if occurred else short(block, 260),
        })
    return items[:6]


def extract_semaphore(markdown: str) -> list[str]:
    match = re.search(
        r"^##\s+Semáforo de (?:la semana|la jornada)\s*\n(.*?)(?=^##\s+|\Z)",
        markdown,
        flags=re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if not match:
        return ["Riesgo relevante", "Tema para observar", "Avance positivo"]
    lines = []
    for line in match.group(1).splitlines():
        line = strip_md(line.lstrip("- "))
        if line:
            line = re.sub(r"^[🟢🟡🔴]\s*", "", line)
            lines.append(short(line, 70))
    return (lines + ["Tema para observar", "Avance positivo"])[:3]


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
        "technologyreview.com": "MIT Technology Review",
        "quantamagazine.org": "Quanta",
        "newscientist.com": "New Scientist",
        "arstechnica.com": "Ars Technica",
        "wired.com": "Wired",
        "theverge.com": "The Verge",
        "spectrum.ieee.org": "IEEE Spectrum",
        "arxiv.org": "arXiv",
        "unesco.org": "UNESCO",
        "oecd.org": "OECD",
        "nist.gov": "NIST",
    }
    names = []
    for domain in domains:
        name = pretty.get(domain, domain)
        if name not in names:
            names.append(name)
    return names[:5] or ["Fuentes enlazadas en el consolidado semanal"]


def load_metadata() -> list[dict]:
    if not DATA_PATH.exists():
        return []
    try:
        value = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        return value if isinstance(value, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def save_metadata(record: dict) -> None:
    rows = [row for row in load_metadata() if row.get("date") != record["date"]]
    rows.append(record)
    rows.sort(key=lambda row: row.get("date", ""))
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(rows[-120:], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def tspans(lines: list[str], x: int, y: int, line_height: int, css: str) -> str:
    spans = []
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else line_height
        spans.append(f'<tspan x="{x}" dy="{dy}">{esc(line)}</tspan>')
    return f'<text x="{x}" y="{y}" style="{css}">' + "".join(spans) + "</text>"


def icon_svg(index: int, x: int, y: int, accent: str) -> str:
    if index == 0:
        return f'<g transform="translate({x},{y})" stroke="{accent}" stroke-width="5" fill="none" stroke-linecap="round"><path d="M5 32 L48 8 L91 32 Z"/><rect x="14" y="34" width="68" height="48" rx="4"/><line x1="26" y1="40" x2="26" y2="74"/><line x1="48" y1="40" x2="48" y2="74"/><line x1="70" y1="40" x2="70" y2="74"/><line x1="7" y1="86" x2="89" y2="86"/></g>'
    if index == 1:
        return f'<g transform="translate({x},{y})"><rect x="8" y="20" width="82" height="62" rx="24" fill="white" stroke="{accent}" stroke-width="5"/><rect x="22" y="34" width="54" height="30" rx="14" fill="#0F2947"/><circle cx="38" cy="49" r="5" fill="#23D5E8"/><circle cx="61" cy="49" r="5" fill="#23D5E8"/><line x1="49" y1="20" x2="49" y2="9" stroke="{accent}" stroke-width="5"/><circle cx="49" cy="6" r="5" fill="{accent}"/></g>'
    if index == 2:
        return f'<g transform="translate({x},{y})"><path d="M50 5 L94 83 H6 Z" fill="#FFD54A" stroke="{accent}" stroke-width="5"/><line x1="50" y1="29" x2="50" y2="58" stroke="{accent}" stroke-width="7" stroke-linecap="round"/><circle cx="50" cy="70" r="4" fill="{accent}"/></g>'
    if index == 3:
        return f'<g transform="translate({x},{y})" fill="none" stroke="{accent}" stroke-width="5"><circle cx="50" cy="50" r="42"/><ellipse cx="50" cy="50" rx="18" ry="42"/><path d="M8 50 H92 M18 30 H82 M18 70 H82"/></g>'
    if index == 4:
        return f'<g transform="translate({x},{y})"><rect x="8" y="55" width="18" height="35" rx="3" fill="#4F8DEB"/><rect x="36" y="36" width="18" height="54" rx="3" fill="#38BFA3"/><rect x="64" y="20" width="18" height="70" rx="3" fill="#F2B705"/><path d="M5 18 L32 34 L55 24 L88 44" fill="none" stroke="{accent}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></g>'
    return f'<g transform="translate({x},{y})"><circle cx="34" cy="45" r="13" fill="#F2B705"/><circle cx="65" cy="42" r="15" fill="#38BFA3"/><circle cx="52" cy="68" r="16" fill="#4F8DEB"/><path d="M12 92 Q34 62 56 92" fill="#FF8DA7"/><path d="M42 94 Q66 58 90 94" fill="#7DD3FC"/><path d="M64 8 Q91 13 83 37 Q62 31 64 8" fill="#46C98C" stroke="{accent}" stroke-width="3"/></g>'


def build_svg(news: list[dict], semaphore: list[str], sources: list[str], week_label: str) -> str:
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">',
        '<rect width="1080" height="1920" fill="#F8FBFF"/>',
        '<path d="M0 0 H1080 V270 C870 330 690 245 480 300 C285 350 145 310 0 260 Z" fill="#073C68"/>',
        '<path d="M760 0 H1080 V420 C972 383 900 320 842 235 C806 181 778 93 760 0 Z" fill="#0A74A9" opacity=".92"/>',
        '<path d="M875 0 H1010 L890 316 C854 289 824 253 801 210 Z" fill="#35C8E8" opacity=".95"/>',
        '<text x="48" y="105" font-family="Arial,Helvetica,sans-serif" font-size="82" font-weight="900" fill="#FFFFFF">IA <tspan fill="#23D5E8">AL DÍA</tspan></text>',
        f'<text x="50" y="151" font-family="Arial,Helvetica,sans-serif" font-size="25" font-weight="700" fill="#FFFFFF">Consolidado semanal · {esc(week_label)}</text>',
        '<rect x="42" y="178" width="710" height="62" rx="24" fill="#FFD52A"/>',
        '<text x="68" y="219" font-family="Arial,Helvetica,sans-serif" font-size="26" font-weight="800" fill="#0C2F4E">Lo más importante y crítico de la semana</text>',
        '<text x="48" y="285" font-family="Arial,Helvetica,sans-serif" font-size="23" font-style="italic" fill="#163A59">Una semana de avances, riesgos y decisiones.</text>',
        '<text x="48" y="316" font-family="Arial,Helvetica,sans-serif" font-size="23" font-style="italic" fill="#163A59">Estas son las noticias clave para entenderla.</text>',
        '<g transform="translate(830,62)"><ellipse cx="100" cy="92" rx="88" ry="70" fill="#FFFFFF" stroke="#A9D8F2" stroke-width="8"/><rect x="45" y="58" width="112" height="62" rx="29" fill="#092D50"/><path d="M70 88 Q82 72 94 88" fill="none" stroke="#23D5E8" stroke-width="8" stroke-linecap="round"/><path d="M112 88 Q124 72 136 88" fill="none" stroke="#23D5E8" stroke-width="8" stroke-linecap="round"/><rect x="60" y="150" width="85" height="90" rx="35" fill="#FFFFFF" stroke="#A9D8F2" stroke-width="8"/><circle cx="102" cy="187" r="16" fill="#23D5E8"/><line x1="102" y1="20" x2="102" y2="7" stroke="#A9D8F2" stroke-width="8"/><circle cx="102" cy="4" r="7" fill="#23D5E8"/></g>',
        '<rect x="833" y="272" width="207" height="62" rx="18" fill="#20D2D8"/><text x="856" y="298" font-family="Arial" font-size="17" font-weight="900" fill="#06395C">TECNOLOGÍA</text><text x="856" y="319" font-family="Arial" font-size="17" font-weight="900" fill="#06395C">PERSONAS · SOCIEDAD</text>',
    ]

    card_w, card_h = 500, 282
    x_positions, y_positions = [30, 550], [360, 660, 960]
    for idx, item in enumerate(news[:6]):
        bg, accent, dark = COLORS[idx]
        x, y = x_positions[idx % 2], y_positions[idx // 2]
        title_lines = wrap(item["title"], 26, 3)
        summary_lines = wrap(item["summary"], 46, 5)
        topic = short(item["topic"], 34)
        out += [
            f'<rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="30" fill="{bg}"/>',
            f'<circle cx="{x+45}" cy="{y+45}" r="28" fill="{accent}"/><text x="{x+45}" y="{y+54}" text-anchor="middle" font-family="Arial" font-size="28" font-weight="900" fill="#FFFFFF">{esc(item["number"])}</text>',
            icon_svg(idx, x+18, y+86, dark),
            tspans(title_lines, x+122, y+48, 30, f"font-family:Arial,Helvetica,sans-serif;font-size:25px;font-weight:900;fill:{dark}"),
            tspans(summary_lines, x+122, y+132, 22, "font-family:Arial,Helvetica,sans-serif;font-size:17px;font-weight:500;fill:#24364B"),
            f'<rect x="{x+122}" y="{y+239}" width="{min(330, 22 + len(topic)*8)}" height="30" rx="15" fill="{accent}" opacity=".95"/>',
            f'<text x="{x+137}" y="{y+260}" font-family="Arial" font-size="13" font-weight="800" fill="#FFFFFF">{esc(topic.upper())}</text>',
        ]

    out += [
        '<rect x="30" y="1270" width="660" height="390" rx="28" fill="#FFFFFF" stroke="#D6E4F0" stroke-width="2"/>',
        '<rect x="30" y="1270" width="660" height="72" rx="28" fill="#073C68"/><rect x="30" y="1314" width="660" height="28" fill="#073C68"/>',
        '<text x="62" y="1318" font-family="Arial" font-size="30" font-weight="900" fill="#FFFFFF">3 claves para leer la semana</text>',
    ]
    ideas = [
        ("1", "Impacto antes que hype", "No toda novedad cambia el panorama: importa el alcance real y la evidencia."),
        ("2", "Riesgo ≠ certeza", "Una advertencia seria merece atención, pero no debe presentarse como un hecho consumado."),
        ("3", "Fuentes primero", "Contrasta medios, papers, documentos oficiales y fuentes primarias antes de concluir."),
    ]
    idea_x = [48, 264, 480]
    idea_bg = ["#E5F2FF", "#FFF3C9", "#EDE8FF"]
    idea_accent = ["#1376C5", "#F2B705", "#6748C8"]
    for i, (num, title, desc) in enumerate(ideas):
        x = idea_x[i]
        out += [
            f'<rect x="{x}" y="1360" width="194" height="270" rx="22" fill="{idea_bg[i]}"/>',
            f'<circle cx="{x+30}" cy="1392" r="22" fill="{idea_accent[i]}"/><text x="{x+30}" y="1400" text-anchor="middle" font-family="Arial" font-size="21" font-weight="900" fill="#FFFFFF">{num}</text>',
            tspans(wrap(title, 18, 3), x+18, 1470, 27, "font-family:Arial;font-size:22px;font-weight:900;fill:#102A43"),
            tspans(wrap(desc, 24, 5), x+18, 1562, 20, "font-family:Arial;font-size:15px;font-weight:500;fill:#3E5368"),
        ]

    out += [
        '<rect x="710" y="1270" width="340" height="390" rx="28" fill="#FFFFFF" stroke="#D6E4F0" stroke-width="2"/>',
        '<rect x="710" y="1270" width="340" height="72" rx="28" fill="#073C68"/><rect x="710" y="1314" width="340" height="28" fill="#073C68"/>',
        '<text x="738" y="1318" font-family="Arial" font-size="28" font-weight="900" fill="#FFFFFF">Semáforo semanal</text>',
    ]
    lights = [("#EF4444", semaphore[2] if len(semaphore) > 2 else semaphore[0], "Mayor atención"), ("#F2B705", semaphore[1], "En observación"), ("#10B981", semaphore[0], "Oportunidad")]
    yy = [1383, 1474, 1565]
    for (color, label, state), y in zip(lights, yy):
        out += [
            f'<circle cx="756" cy="{y}" r="25" fill="{color}"/>',
            tspans(wrap(label, 25, 2), 795, y-7, 19, "font-family:Arial;font-size:16px;font-weight:800;fill:#20364A"),
            f'<text x="795" y="{y+38}" font-family="Arial" font-size="13" fill="#667085">{esc(state)}</text>',
        ]

    source_text = " · ".join(sources)
    out += [
        '<path d="M0 1700 C260 1630 430 1745 650 1710 C835 1680 948 1645 1080 1685 V1920 H0 Z" fill="#073C68"/>',
        '<text x="48" y="1785" font-family="cursive" font-size="37" font-style="italic" fill="#FFFFFF">Entender la semana,</text>',
        '<text x="48" y="1832" font-family="cursive" font-size="37" font-style="italic" fill="#FFFFFF">para decidir mejor.</text>',
        '<line x1="52" y1="1861" x2="405" y2="1861" stroke="#23D5E8" stroke-width="8" stroke-linecap="round"/>',
        f'<text x="1030" y="1810" text-anchor="end" font-family="Arial" font-size="15" fill="#D6E7F6">Fuentes: {esc(source_text)}</text>',
        '<text x="1030" y="1840" text-anchor="end" font-family="Arial" font-size="15" fill="#D6E7F6">Consolidado semanal · Observatorio IA al Día</text>',
        '<text x="1030" y="1870" text-anchor="end" font-family="Arial" font-size="14" fill="#9FDFF1">ljarias.github.io</text>',
        '</svg>',
    ]
    return "\n".join(out)


def week_label(start, end) -> str:
    if start.month == end.month and start.year == end.year:
        return f"{start.day}–{end.day} de {MONTHS[end.month - 1]} de {end.year}"
    if start.year == end.year:
        return f"{start.day} de {MONTHS[start.month - 1]} – {end.day} de {MONTHS[end.month - 1]} de {end.year}"
    return f"{start.day}/{start.month}/{start.year} – {end.day}/{end.month}/{end.year}"


def main() -> None:
    now = datetime.now(TZ)
    date_iso = now.date().isoformat()
    week_end = now.date()
    week_start = week_end - timedelta(days=6)
    label = week_label(week_start, week_end)
    post_path = POSTS_DIR / f"{date_iso}-ia-al-dia.md"
    if not post_path.exists():
        print(f"No existe {post_path.relative_to(ROOT)}. No hay infografía semanal para generar.")
        return

    INFO_DIR.mkdir(parents=True, exist_ok=True)
    image_path = INFO_DIR / f"{date_iso}.svg"
    post_url = f"/{now:%Y/%m/%d}/ia-al-dia/"
    record = {
        "date": date_iso,
        "edition_type": "weekly",
        "period_start": week_start.isoformat(),
        "period_end": week_end.isoformat(),
        "title": f"Infografía IA al Día — Semana {label}",
        "image": f"/assets/infografias/{date_iso}.svg",
        "post_url": post_url,
        "alt": f"Infografía con el consolidado semanal de noticias de inteligencia artificial, semana {label}",
        "model": "SVG automático IA al Día",
    }

    if image_path.exists() and not FORCE:
        save_metadata(record)
        print(f"La infografía semanal ya existe: {image_path.relative_to(ROOT)}")
        return

    markdown = post_path.read_text(encoding="utf-8")
    news = extract_news(markdown)
    if len(news) < 3:
        raise RuntimeError("No se pudieron extraer suficientes noticias del consolidado semanal.")
    while len(news) < 6:
        news.append({
            "number": str(len(news) + 1),
            "title": "Tema para seguir",
            "type": "OBSERVACIÓN",
            "topic": "Seguimiento",
            "summary": "Revisa el consolidado semanal para ampliar el contexto y consultar las fuentes enlazadas.",
        })

    svg = build_svg(news[:6], extract_semaphore(markdown), source_names(markdown), label)
    image_path.write_text(svg, encoding="utf-8")
    save_metadata(record)
    print(f"Infografía semanal generada: {image_path.relative_to(ROOT)}")
    print("Formato: SVG 1080×1920, sin costo adicional de generación de imagen.")


if __name__ == "__main__":
    main()

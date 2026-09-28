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

CARD_PALETTES = [
    ("#FDECEF", "#D92D4F", "#6E1730"),
    ("#EAF4FF", "#1F75C9", "#123E69"),
    ("#FFF6D8", "#E2A600", "#5C4700"),
    ("#F0ECFF", "#6C51C7", "#392B73"),
    ("#E5F8EF", "#16976D", "#075E47"),
    ("#FFF0F4", "#DA3A67", "#731A37"),
]

CRITICITY = {
    "ALTO": ("#DC2626", "#FFF1F2", "#FFFFFF"),
    "MEDIO": ("#F59E0B", "#FFFBEB", "#2D2200"),
    "BAJO": ("#16A34A", "#ECFDF5", "#FFFFFF"),
}


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def strip_md(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[*_`>#]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def complete_excerpt(text: str, limit: int = 220) -> str:
    """Resume visualmente sin terminar en una palabra cortada ni usar puntos suspensivos."""
    text = strip_md(text)
    if len(text) <= limit:
        return text
    candidate = text[:limit]
    sentence_end = max(candidate.rfind("."), candidate.rfind("?"), candidate.rfind("!"))
    if sentence_end >= int(limit * 0.55):
        return candidate[: sentence_end + 1].strip()
    return candidate.rsplit(" ", 1)[0].rstrip(" ,;:")


def wrap(text: str, max_chars: int, max_lines: int) -> list[str]:
    words = strip_md(text).split()
    lines: list[str] = []
    current: list[str] = []
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
        tema = re.search(r"\*\*Tema:\*\*\s*([^\n]+)", block, flags=re.IGNORECASE)
        criticality = re.search(r"\*\*Nivel de criticidad:\*\*\s*([^\n]+)", block, flags=re.IGNORECASE)
        occurred = section(block, "Qué ocurrió")
        level = strip_md(criticality.group(1)).upper() if criticality else "MEDIO"
        if level not in CRITICITY:
            level = "MEDIO"
        items.append({
            "number": number,
            "title": strip_md(title),
            "topic": complete_excerpt(tema.group(1), 38) if tema else "Inteligencia artificial",
            "criticality": level,
            "summary": complete_excerpt(occurred if occurred else block, 205),
        })
    return items[:6]


def extract_semaphore(markdown: str) -> list[str]:
    match = re.search(
        r"^##\s+Semáforo de (?:la semana|la jornada)\s*\n(.*?)(?=^##\s+|\Z)",
        markdown,
        flags=re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if not match:
        return ["Avances y usos positivos", "Regulación e infraestructura", "Autonomía sin control suficiente"]
    lines = []
    for line in match.group(1).splitlines():
        if not line.strip().startswith("-"):
            continue
        clean = strip_md(line.lstrip("- "))
        clean = re.sub(r"^[🟢🟡🔴]\s*", "", clean)
        clean = re.sub(r"^(Avance positivo|Tema para observar|Riesgo relevante):\s*", "", clean, flags=re.IGNORECASE)
        if clean:
            lines.append(complete_excerpt(clean, 72))
    return (lines + ["Tema para observar", "Riesgo relevante"])[:3]


def extract_questions(markdown: str) -> list[str]:
    match = re.search(
        r"^##\s+(?:Cinco|Tres) preguntas para el aula\s*\n(.*?)(?=^##\s+|\Z)",
        markdown,
        flags=re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if not match:
        return [
            "¿Qué riesgo de esta semana requiere más supervisión humana?",
            "¿Quién debería responder cuando un agente de IA causa un daño?",
            "¿Cómo equilibrar innovación, seguridad y derechos?",
        ]
    questions = []
    for line in match.group(1).splitlines():
        m = re.match(r"^\s*\d+[.)]\s*(.+)", line)
        if m:
            questions.append(strip_md(m.group(1)))
    return (questions + [
        "¿Qué riesgo de esta semana requiere más supervisión humana?",
        "¿Cómo equilibrar innovación y seguridad?",
    ])[:3]


def source_names(markdown: str) -> list[str]:
    domains = []
    for url in re.findall(r"https?://[^\s)\]>\"']+", markdown):
        host = urlparse(url.rstrip(".,;:")).netloc.lower().removeprefix("www.")
        if host and host not in domains:
            domains.append(host)
    pretty = {
        "reuters.com": "Reuters", "apnews.com": "AP", "bbc.com": "BBC", "bbc.co.uk": "BBC",
        "nature.com": "Nature", "science.org": "Science",
        "technologyreview.com": "MIT Technology Review", "quantamagazine.org": "Quanta",
        "newscientist.com": "New Scientist", "arstechnica.com": "Ars Technica",
        "wired.com": "Wired", "theverge.com": "The Verge",
        "spectrum.ieee.org": "IEEE Spectrum", "arxiv.org": "arXiv",
        "unesco.org": "UNESCO", "oecd.org": "OECD", "nist.gov": "NIST",
    }
    names = []
    for domain in domains:
        name = pretty.get(domain, domain)
        if name not in names:
            names.append(name)
    return names[:5] or ["Fuentes enlazadas en la edición"]


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
    icons = [
        f'<g transform="translate({x},{y})" stroke="{accent}" stroke-width="5" fill="none" stroke-linecap="round"><path d="M5 32 L48 8 L91 32 Z"/><rect x="14" y="34" width="68" height="48" rx="4"/><line x1="26" y1="40" x2="26" y2="74"/><line x1="48" y1="40" x2="48" y2="74"/><line x1="70" y1="40" x2="70" y2="74"/><line x1="7" y1="86" x2="89" y2="86"/></g>',
        f'<g transform="translate({x},{y})"><rect x="8" y="20" width="82" height="62" rx="24" fill="white" stroke="{accent}" stroke-width="5"/><rect x="22" y="34" width="54" height="30" rx="14" fill="#0F2947"/><circle cx="38" cy="49" r="5" fill="#23D5E8"/><circle cx="61" cy="49" r="5" fill="#23D5E8"/><line x1="49" y1="20" x2="49" y2="9" stroke="{accent}" stroke-width="5"/><circle cx="49" cy="6" r="5" fill="{accent}"/></g>',
        f'<g transform="translate({x},{y})"><path d="M50 5 L94 83 H6 Z" fill="#FFD54A" stroke="{accent}" stroke-width="5"/><line x1="50" y1="29" x2="50" y2="58" stroke="{accent}" stroke-width="7" stroke-linecap="round"/><circle cx="50" cy="70" r="4" fill="{accent}"/></g>',
        f'<g transform="translate({x},{y})" fill="none" stroke="{accent}" stroke-width="5"><circle cx="50" cy="50" r="42"/><ellipse cx="50" cy="50" rx="18" ry="42"/><path d="M8 50 H92 M18 30 H82 M18 70 H82"/></g>',
        f'<g transform="translate({x},{y})"><rect x="8" y="55" width="18" height="35" rx="3" fill="#4F8DEB"/><rect x="36" y="36" width="18" height="54" rx="3" fill="#38BFA3"/><rect x="64" y="20" width="18" height="70" rx="3" fill="#F2B705"/><path d="M5 18 L32 34 L55 24 L88 44" fill="none" stroke="{accent}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></g>',
        f'<g transform="translate({x},{y})"><circle cx="34" cy="45" r="13" fill="#F2B705"/><circle cx="65" cy="42" r="15" fill="#38BFA3"/><circle cx="52" cy="68" r="16" fill="#4F8DEB"/><path d="M12 92 Q34 62 56 92" fill="#FF8DA7"/><path d="M42 94 Q66 58 90 94" fill="#7DD3FC"/></g>',
    ]
    return icons[index % len(icons)]


def build_svg(news: list[dict], semaphore: list[str], questions: list[str], sources: list[str], week_label: str) -> str:
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">',
        '<rect width="1080" height="1920" fill="#F6FAFE"/>',
        '<rect x="0" y="0" width="1080" height="315" fill="#073C68"/>',
        '<path d="M775 0 H1080 V315 H905 C860 257 820 164 775 0 Z" fill="#0A74A9"/>',
        '<path d="M906 0 H1045 L922 272 C888 239 860 198 840 150 Z" fill="#2BC4E7" opacity=".9"/>',
        '<text x="44" y="88" font-family="Arial,Helvetica,sans-serif" font-size="68" font-weight="700" fill="#FFFFFF">IA <tspan fill="#38D8F1">AL DÍA</tspan></text>',
        f'<text x="47" y="133" font-family="Arial,Helvetica,sans-serif" font-size="24" font-weight="600" fill="#D9F6FF">Consolidado semanal · {esc(week_label)}</text>',
        '<rect x="42" y="166" width="950" height="104" rx="24" fill="#0A4F88"/>',
        '<text x="66" y="205" font-family="Arial,Helvetica,sans-serif" font-size="24" font-weight="500" fill="#FFFFFF">Una semana de avances, riesgos y decisiones.</text>',
        '<text x="66" y="242" font-family="Arial,Helvetica,sans-serif" font-size="24" font-weight="500" fill="#FFFFFF">Estas son las noticias clave para entenderla.</text>',
        '<g transform="translate(858,49)"><ellipse cx="85" cy="78" rx="73" ry="58" fill="#FFFFFF" stroke="#A9D8F2" stroke-width="7"/><rect x="38" y="51" width="94" height="52" rx="25" fill="#092D50"/><path d="M57 77 Q68 63 79 77" fill="none" stroke="#23D5E8" stroke-width="7" stroke-linecap="round"/><path d="M92 77 Q103 63 114 77" fill="none" stroke="#23D5E8" stroke-width="7" stroke-linecap="round"/><rect x="50" y="127" width="70" height="69" rx="29" fill="#FFFFFF" stroke="#A9D8F2" stroke-width="7"/><circle cx="85" cy="156" r="13" fill="#23D5E8"/></g>',
    ]

    card_w, card_h = 505, 275
    x_positions, y_positions = [25, 550], [335, 625, 915]
    for idx, item in enumerate(news[:6]):
        bg, accent, dark = CARD_PALETTES[idx]
        x, y = x_positions[idx % 2], y_positions[idx // 2]
        title_font = 21 if len(item["title"]) <= 72 else 18.5
        title_chars = 30 if title_font >= 21 else 35
        title_lines = wrap(item["title"], title_chars, 4)
        summary_lines = wrap(item["summary"], 48, 4)
        level = item["criticality"]
        badge, level_bg, badge_text = CRITICITY[level]
        topic_lines = wrap(item["topic"], 27, 2)
        out += [
            f'<rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="26" fill="{bg}" stroke="{level_bg}" stroke-width="2"/>',
            f'<circle cx="{x+42}" cy="{y+42}" r="25" fill="{accent}"/><text x="{x+42}" y="{y+50}" text-anchor="middle" font-family="Arial" font-size="24" font-weight="700" fill="#FFFFFF">{esc(item["number"])}</text>',
            icon_svg(idx, x+15, y+83, dark),
            tspans(title_lines, x+118, y+43, 25, f"font-family:Arial,Helvetica,sans-serif;font-size:{title_font}px;font-weight:600;fill:{dark}"),
            tspans(summary_lines, x+118, y+145, 20, "font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:400;fill:#24364B"),
            tspans([line.upper() for line in topic_lines], x+118, y+235, 15, "font-family:Arial,Helvetica,sans-serif;font-size:11.2px;font-weight:600;fill:#52667A"),
            f'<rect x="{x+385}" y="{y+222}" width="100" height="34" rx="17" fill="{badge}"/>',
            f'<text x="{x+435}" y="{y+245}" text-anchor="middle" font-family="Arial" font-size="14" font-weight="700" fill="{badge_text}">{esc(level)}</text>',
        ]

    # Bloque "Para discutir en clase" — mantiene la identidad visual de las ediciones previas.
    out += [
        '<rect x="25" y="1215" width="1030" height="250" rx="28" fill="#EAF4FF" stroke="#B8D9F7" stroke-width="2"/>',
        '<rect x="25" y="1215" width="360" height="60" rx="22" fill="#073C68"/>',
        '<text x="50" y="1255" font-family="Arial,Helvetica,sans-serif" font-size="28" font-weight="700" fill="#FFFFFF">Para discutir en clase</text>',
    ]
    q_y = [1310, 1365, 1420]
    for i, (q, y) in enumerate(zip(questions[:3], q_y), start=1):
        out += [
            f'<circle cx="66" cy="{y-7}" r="20" fill="#1F75C9"/>',
            f'<text x="66" y="{y}" text-anchor="middle" font-family="Arial" font-size="17" font-weight="700" fill="#FFFFFF">{i}</text>',
            tspans(wrap(q, 72, 2), 100, y-6, 22, "font-family:Arial,Helvetica,sans-serif;font-size:17px;font-weight:500;fill:#153A5B"),
        ]

    # Semáforo semanal.
    out += [
        '<rect x="25" y="1490" width="1030" height="265" rx="28" fill="#073C68"/>',
        '<text x="55" y="1540" font-family="Arial,Helvetica,sans-serif" font-size="28" font-weight="700" fill="#FFFFFF">Semáforo de la semana</text>',
    ]
    sem_items = [
        ("#EF4444", "Riesgo", semaphore[2] if len(semaphore) > 2 else "Autonomía sin control suficiente"),
        ("#F2B705", "Atención", semaphore[1] if len(semaphore) > 1 else "Regulación e infraestructura"),
        ("#10B981", "Oportunidad", semaphore[0] if semaphore else "Ciencia y usos positivos"),
    ]
    sx = [48, 380, 712]
    light_bg = ["#FFE4E7", "#FFF2C4", "#DCF7EA"]
    for i, ((color, label, text_value), x) in enumerate(zip(sem_items, sx)):
        out += [
            f'<rect x="{x}" y="1570" width="300" height="155" rx="20" fill="{light_bg[i]}"/>',
            f'<circle cx="{x+42}" cy="1612" r="22" fill="{color}"/>',
            f'<text x="{x+78}" y="1608" font-family="Arial" font-size="17" font-weight="700" fill="#18324A">{label}:</text>',
            tspans(wrap(text_value, 27, 5), x+78, 1633, 17, "font-family:Arial,Helvetica,sans-serif;font-size:13.5px;font-weight:500;fill:#273E54"),
        ]

    source_text = " · ".join(sources)
    out += [
        '<rect x="0" y="1785" width="1080" height="135" fill="#073C68"/>',
        '<text x="45" y="1830" font-family="Arial,Helvetica,sans-serif" font-size="18" font-weight="600" fill="#FFFFFF">Fuentes principales</text>',
        tspans(wrap(source_text, 62, 2), 45, 1857, 20, "font-family:Arial,Helvetica,sans-serif;font-size:14px;font-weight:400;fill:#D6E7F6"),
        '<text x="1035" y="1840" text-anchor="end" font-family="Arial" font-size="14" fill="#D6E7F6">Observatorio IA al Día</text>',
        '<text x="1035" y="1865" text-anchor="end" font-family="Arial" font-size="13" fill="#9FDFF1">ljarias.github.io</text>',
        '<text x="1035" y="1890" text-anchor="end" font-family="Arial" font-size="12" fill="#D6E7F6">Proyecto liderado por Leonardo Arias-Alemán</text>',
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
            "topic": "Seguimiento",
            "criticality": "MEDIO",
            "summary": "Consulta el consolidado semanal para ampliar el contexto y revisar las fuentes.",
        })

    svg = build_svg(
        news[:6],
        extract_semaphore(markdown),
        extract_questions(markdown),
        source_names(markdown),
        label,
    )
    image_path.write_text(svg, encoding="utf-8")
    save_metadata(record)
    print(f"Infografía semanal generada: {image_path.relative_to(ROOT)}")
    print("Formato: SVG 1080×1920, optimizado para contraste y lectura móvil.")


if __name__ == "__main__":
    main()

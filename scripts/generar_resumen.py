from __future__ import annotations

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent
PROMPT_PATH = ROOT / "prompts" / "editor_ia.md"
HISTORY_PATH = ROOT / "data" / "historial.json"
TELEMETRY_PATH = ROOT / "_data" / "consumo_api.json"
POSTS_DIR = ROOT / "_posts"
TZ = ZoneInfo("America/Bogota")
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")

# Tarifas vigentes consultadas en la documentación oficial de OpenAI
# el 17 de septiembre de 2026. Valores en USD por 1M tokens.
PRICING = {
    "gpt-5.6-luna": {
        "short": {
            "input": 0.20,
            "cached_input": 0.02,
            "cache_write": 0.25,
            "output": 1.20,
        },
        "long": {
            "input": 0.40,
            "cached_input": 0.04,
            "cache_write": 0.50,
            "output": 1.80,
        },
        "web_search_call": 0.01,
    }
}
LONG_CONTEXT_THRESHOLD = 272_000
PRICING_SOURCE = "https://developers.openai.com/api/docs/pricing"
PRICING_CHECKED_AT = "2026-09-17"

MONTHS = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def load_history() -> list[dict]:
    return load_json(HISTORY_PATH, [])


def load_telemetry() -> list[dict]:
    return load_json(TELEMETRY_PATH, [])


def save_telemetry(records: list[dict]) -> None:
    TELEMETRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    TELEMETRY_PATH.write_text(
        json.dumps(records[-365:], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


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


def human_date(value) -> str:
    return f"{value.day} de {MONTHS[value.month - 1]} de {value.year}"


def human_week_range(start, end) -> str:
    if start.year == end.year and start.month == end.month:
        return f"del {start.day} al {end.day} de {MONTHS[end.month - 1]} de {end.year}"
    if start.year == end.year:
        return (
            f"del {start.day} de {MONTHS[start.month - 1]} "
            f"al {end.day} de {MONTHS[end.month - 1]} de {end.year}"
        )
    return (
        f"del {start.day} de {MONTHS[start.month - 1]} de {start.year} "
        f"al {end.day} de {MONTHS[end.month - 1]} de {end.year}"
    )


def _attr(obj, name: str, default=0):
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def count_web_search_calls(response) -> int:
    total = 0
    for item in (getattr(response, "output", None) or []):
        item_type = _attr(item, "type", "")
        if item_type in {"web_search_call", "web_search_preview_call"}:
            total += 1
    return total


def calculate_cost(response, model: str) -> dict:
    usage = getattr(response, "usage", None)
    input_tokens = int(_attr(usage, "input_tokens", 0) or 0)
    output_tokens = int(_attr(usage, "output_tokens", 0) or 0)
    total_tokens = int(_attr(usage, "total_tokens", input_tokens + output_tokens) or 0)

    input_details = _attr(usage, "input_tokens_details", None)
    output_details = _attr(usage, "output_tokens_details", None)
    cached_tokens = int(_attr(input_details, "cached_tokens", 0) or 0)
    cache_write_tokens = int(_attr(input_details, "cache_write_tokens", 0) or 0)
    reasoning_tokens = int(_attr(output_details, "reasoning_tokens", 0) or 0)

    uncached_input_tokens = max(input_tokens - cached_tokens - cache_write_tokens, 0)
    web_search_calls = count_web_search_calls(response)

    pricing = PRICING.get(model)
    if not pricing:
        return {
            "input_tokens": input_tokens,
            "cached_input_tokens": cached_tokens,
            "cache_write_tokens": cache_write_tokens,
            "uncached_input_tokens": uncached_input_tokens,
            "output_tokens": output_tokens,
            "reasoning_tokens": reasoning_tokens,
            "total_tokens": total_tokens,
            "web_search_calls": web_search_calls,
            "long_context": input_tokens > LONG_CONTEXT_THRESHOLD,
            "cost_input_usd": None,
            "cost_cached_input_usd": None,
            "cost_cache_write_usd": None,
            "cost_output_usd": None,
            "cost_web_search_usd": None,
            "estimated_cost_usd": None,
            "pricing_known": False,
        }

    context_tier = "long" if input_tokens > LONG_CONTEXT_THRESHOLD else "short"
    rates = pricing[context_tier]
    million = 1_000_000

    cost_input = uncached_input_tokens / million * rates["input"]
    cost_cached = cached_tokens / million * rates["cached_input"]
    cost_cache_write = cache_write_tokens / million * rates["cache_write"]
    cost_output = output_tokens / million * rates["output"]
    cost_web = web_search_calls * pricing["web_search_call"]
    total_cost = cost_input + cost_cached + cost_cache_write + cost_output + cost_web

    return {
        "input_tokens": input_tokens,
        "cached_input_tokens": cached_tokens,
        "cache_write_tokens": cache_write_tokens,
        "uncached_input_tokens": uncached_input_tokens,
        "output_tokens": output_tokens,
        "reasoning_tokens": reasoning_tokens,
        "total_tokens": total_tokens,
        "web_search_calls": web_search_calls,
        "long_context": context_tier == "long",
        "cost_input_usd": round(cost_input, 6),
        "cost_cached_input_usd": round(cost_cached, 6),
        "cost_cache_write_usd": round(cost_cache_write, 6),
        "cost_output_usd": round(cost_output, 6),
        "cost_web_search_usd": round(cost_web, 6),
        "estimated_cost_usd": round(total_cost, 6),
        "pricing_known": True,
    }


def add_telemetry_record(record: dict) -> None:
    records = load_telemetry()
    records = [item for item in records if item.get("date") != record.get("date")]
    records.append(record)
    records.sort(key=lambda item: item.get("timestamp", item.get("date", "")))

    successful = [
        item for item in records
        if item.get("status") == "success"
        and isinstance(item.get("estimated_cost_usd"), (int, float))
    ]

    month_prefix = record.get("date", "")[:7]
    month_total = sum(
        float(item.get("estimated_cost_usd", 0) or 0)
        for item in successful
        if item.get("date", "").startswith(month_prefix)
    )
    all_time_total = sum(
        float(item.get("estimated_cost_usd", 0) or 0)
        for item in successful
    )

    record["month_estimated_cost_usd"] = round(month_total, 6)
    record["all_time_estimated_cost_usd"] = round(all_time_total, 6)

    records = [item for item in records if item.get("date") != record.get("date")]
    records.append(record)
    records.sort(key=lambda item: item.get("timestamp", item.get("date", "")))
    save_telemetry(records)


def telemetry_failure(now: datetime, week_start, week_end, exc: Exception) -> None:
    message = str(exc)

    if "credit_balance_exhausted" in message or "insufficient_quota" in message:
        error_code = "credit_balance_exhausted"
    elif "429" in message:
        error_code = "rate_limit_or_quota"
    else:
        error_code = exc.__class__.__name__

    add_telemetry_record({
        "date": now.date().isoformat(),
        "timestamp": now.isoformat(),
        "edition_type": "weekly",
        "period_start": week_start.isoformat(),
        "period_end": week_end.isoformat(),
        "model": MODEL,
        "status": "failed",
        "error_code": error_code,
        "error_message": message[:500],
        "input_tokens": 0,
        "cached_input_tokens": 0,
        "cache_write_tokens": 0,
        "uncached_input_tokens": 0,
        "output_tokens": 0,
        "reasoning_tokens": 0,
        "total_tokens": 0,
        "web_search_calls": 0,
        "estimated_cost_usd": 0.0,
        "pricing_known": MODEL in PRICING,
        "pricing_source": PRICING_SOURCE,
        "pricing_checked_at": PRICING_CHECKED_AT,
        "note": "La llamada falló antes de devolver métricas de uso facturable.",
    })


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit(
            "Falta OPENAI_API_KEY. Configúrala como secreto de GitHub Actions antes de ejecutar el agente."
        )

    now = datetime.now(TZ)
    date_iso = now.date().isoformat()
    week_end = now.date()
    week_start = week_end - timedelta(days=6)
    week_label = human_week_range(week_start, week_end)

    editorial_prompt = PROMPT_PATH.read_text(encoding="utf-8")
    history = load_history()
    recent_history = history[-12:]

    context = {
        "fecha_ejecucion": date_iso,
        "periodo_inicio": week_start.isoformat(),
        "periodo_fin": week_end.isoformat(),
        "zona_horaria": "America/Bogota",
        "ediciones_recientes": recent_history,
    }

    input_text = f"""
{editorial_prompt}

## Contexto de esta ejecución

Hoy es {human_date(now.date())}. Esta es una edición semanal.

El periodo editorial que debes consolidar va {week_label}. Investiga a nivel mundial los hechos más importantes y críticos ocurridos, publicados o sustancialmente actualizados durante ese periodo. Si una noticia fue publicada esta semana pero describe un hecho antiguo, aclara la fecha real del acontecimiento y decide si sigue siendo relevante.

No intentes resumir cada día. Identifica patrones, conecta desarrollos relacionados y selecciona únicamente los asuntos que realmente merecen quedar en el consolidado semanal.

Para reducir duplicados, esta es la memoria editorial de las últimas ediciones:

{json.dumps(context, ensure_ascii=False, indent=2)}

Si un tema ya aparece allí, inclúyelo solamente si hubo un desarrollo nuevo y sustancial durante la semana actual.
""".strip()

    client = OpenAI()

    try:
        response = client.responses.create(
            model=MODEL,
            reasoning={"effort": "low"},
            tools=[{"type": "web_search_preview", "search_context_size": "medium"}],
            input=input_text,
            max_output_tokens=8500,
        )
    except Exception as exc:
        telemetry_failure(now, week_start, week_end, exc)
        raise

    usage_record = calculate_cost(response, MODEL)
    body = clean_markdown(response.output_text or "")

    if len(body) < 700:
        add_telemetry_record({
            "date": date_iso,
            "timestamp": now.isoformat(),
            "edition_type": "weekly",
            "period_start": week_start.isoformat(),
            "period_end": week_end.isoformat(),
            "model": MODEL,
            "response_id": getattr(response, "id", None),
            "status": "failed_content",
            **usage_record,
            "pricing_source": PRICING_SOURCE,
            "pricing_checked_at": PRICING_CHECKED_AT,
            "note": "La API respondió y generó consumo, pero el contenido fue demasiado corto para publicar.",
        })
        raise RuntimeError("La respuesta del agente fue demasiado corta; se cancela la publicación.")

    add_telemetry_record({
        "date": date_iso,
        "timestamp": now.isoformat(),
        "edition_type": "weekly",
        "period_start": week_start.isoformat(),
        "period_end": week_end.isoformat(),
        "model": MODEL,
        "response_id": getattr(response, "id", None),
        "status": "success",
        **usage_record,
        "pricing_source": PRICING_SOURCE,
        "pricing_checked_at": PRICING_CHECKED_AT,
        "pricing_note": (
            "Costo estimado con tarifa Standard. Incluye tokens reportados por Responses API "
            "y USD 0.01 por cada web_search_call detectado. No sustituye la factura oficial."
        ),
    })

    title = f"IA al Día — Consolidado semanal {week_label}"
    summary = (
        "Consolidado semanal de las noticias mundiales más importantes y críticas sobre inteligencia artificial, "
        "con contexto, nivel de criticidad, riesgos, oportunidades y preguntas para el aula."
    )

    front_matter = f'''---\nlayout: post\ntitle: "{yaml_escape(title)}"\ndate: {now.strftime('%Y-%m-%d %H:%M:%S %z')}\nsummary: "{yaml_escape(summary)}"\nreading_time: "12–18 min"\ncategories: [ia, noticias, educacion, semanal]\n---\n\n'''

    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    post_path = POSTS_DIR / f"{date_iso}-ia-al-dia.md"
    post_path.write_text(front_matter + body + "\n", encoding="utf-8")

    record = {
        "date": date_iso,
        "edition_type": "weekly",
        "period_start": week_start.isoformat(),
        "period_end": week_end.isoformat(),
        "post": str(post_path.relative_to(ROOT)),
        "titles": extract_titles(body)[:10],
        "urls": extract_urls(body)[:60],
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

    print(f"Consolidado semanal generado: {post_path.relative_to(ROOT)}")
    print(f"Periodo: {week_start.isoformat()} a {week_end.isoformat()}")
    print(f"Noticias detectadas: {len(record['titles'])}")
    print(f"URLs registradas: {len(record['urls'])}")
    print("Telemetría de consumo:")
    print(f"  Entrada: {usage_record['input_tokens']:,} tokens")
    print(f"  Salida: {usage_record['output_tokens']:,} tokens")
    print(f"  Búsquedas web: {usage_record['web_search_calls']}")
    if usage_record["estimated_cost_usd"] is not None:
        print(f"  Costo estimado: USD {usage_record['estimated_cost_usd']:.4f}")


if __name__ == "__main__":
    main()

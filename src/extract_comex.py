from __future__ import annotations

import time
from typing import Any

import pandas as pd
import requests

from config import COMEX_API_URLS, COMEX_HEADING


def _post_with_fallback(payload: dict[str, Any], timeout: int = 60) -> dict[str, Any]:
    last_error: Exception | None = None
    for url in COMEX_API_URLS:
        try:
            response = requests.post(url, json=payload, timeout=timeout)
            response.raise_for_status()
            body = response.json()
            if not body.get("success", True):
                raise RuntimeError(body.get("message") or f"Comex Stat returned success=false: {url}")
            return body
        except Exception as exc:  # fallback intentionally broad: DNS, timeout, HTTP, JSON
            last_error = exc
            time.sleep(1)
    raise RuntimeError(f"Falha ao consultar Comex Stat: {last_error}")


def extract_comex_period(start: str, end: str, month_detail: bool = True) -> pd.DataFrame:
    """Extrai exportações da posição SH4 0102 (animais vivos da espécie bovina).

    O detalhamento por NCM é preservado para permitir separar bovinos domésticos,
    búfalos e outros bovinos nas etapas analíticas.
    """
    payload = {
        "flow": "export",
        "monthDetail": month_detail,
        "period": {"from": start, "to": end},
        "filters": [{"filter": "heading", "values": [COMEX_HEADING]}],
        "details": ["country", "state", "ncm"],
        "metrics": ["metricFOB", "metricKG", "metricStatistic"],
    }
    body = _post_with_fallback(payload)
    rows = body.get("data", {}).get("list", [])
    df = pd.DataFrame(rows)
    if df.empty:
        return df

    rename = {
        "year": "ano",
        "monthNumber": "mes",
        "country": "pais_destino",
        "state": "uf",
        "ncm": "ncm",
        "metricFOB": "valor_fob_usd",
        "metricKG": "kg_liquido",
        "metricStatistic": "cabecas_exportadas",
    }
    df = df.rename(columns=rename)
    for col in ["ano", "mes", "valor_fob_usd", "kg_liquido", "cabecas_exportadas"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "ncm" in df.columns:
        df["ncm"] = df["ncm"].astype(str).str.replace(".", "", regex=False).str.zfill(8)

    return df

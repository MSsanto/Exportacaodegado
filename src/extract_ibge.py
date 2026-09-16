from __future__ import annotations

import pandas as pd
import requests

from config import (
    SIDRA_BASE_URL,
    SIDRA_BOVINE_CODE,
    SIDRA_HERD_CLASSIFICATION,
    SIDRA_TABLE,
    SIDRA_VARIABLE,
)


def extract_bovine_herd(start_year: int, end_year: int) -> pd.DataFrame:
    """Extrai efetivo bovino anual por UF na PPM/SIDRA tabela 3939."""
    periods = ",".join(str(year) for year in range(start_year, end_year + 1))
    url = (
        f"{SIDRA_BASE_URL}/t/{SIDRA_TABLE}/n3/all/u/y/v/{SIDRA_VARIABLE}"
        f"/p/{periods}/c{SIDRA_HERD_CLASSIFICATION}/{SIDRA_BOVINE_CODE}/f/u"
    )
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    rows = response.json()
    if not rows or len(rows) == 1:
        return pd.DataFrame()

    header = rows[0]
    records = rows[1:]
    df = pd.DataFrame(records)

    # A API SIDRA retorna chaves curtas (D1C, D1N, D2C...).
    # Usamos os nomes do cabeçalho para descobrir a semântica, evitando
    # depender apenas da posição das dimensões.
    semantic = {key: str(label).lower() for key, label in header.items()}

    def find_key(*terms: str) -> str | None:
        for key, label in semantic.items():
            if all(term in label for term in terms):
                return key
        return None

    uf_name_key = find_key("unidade da federação") or find_key("brasil e unidade")
    year_key = find_key("ano")
    value_key = "V" if "V" in df.columns else find_key("valor")

    if not uf_name_key or not year_key or not value_key:
        raise RuntimeError(f"Layout SIDRA inesperado. Cabeçalho recebido: {header}")

    out = df[[uf_name_key, year_key, value_key]].copy()
    out.columns = ["uf_nome", "ano", "rebanho_bovino_cabecas"]
    out["ano"] = pd.to_numeric(out["ano"], errors="coerce")
    out["rebanho_bovino_cabecas"] = pd.to_numeric(
        out["rebanho_bovino_cabecas"].astype(str).str.replace("-", "", regex=False),
        errors="coerce",
    )
    return out.dropna(subset=["ano", "rebanho_bovino_cabecas"])

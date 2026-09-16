from __future__ import annotations

import pandas as pd
import requests

from config import SIDRA_BOVINE_CODE, SIDRA_HERD_CLASSIFICATION, SIDRA_TABLE, SIDRA_VARIABLE

IBGE_AGGREGATES_BASE = "https://servicodados.ibge.gov.br/api/v3/agregados"


def _extract_year(year: int) -> list[dict[str, object]]:
    """Extrai o efetivo bovino por UF para um ano usando a API oficial de Agregados."""
    url = (
        f"{IBGE_AGGREGATES_BASE}/{SIDRA_TABLE}/periodos/{year}/variaveis/{SIDRA_VARIABLE}"
        f"?localidades=N3[all]&classificacao={SIDRA_HERD_CLASSIFICATION}[{SIDRA_BOVINE_CODE}]"
    )
    response = requests.get(
        url,
        timeout=60,
        headers={"User-Agent": "Exportacaodegado-portfolio/1.0"},
    )
    response.raise_for_status()
    payload = response.json()

    rows: list[dict[str, object]] = []
    for variable in payload:
        for result in variable.get("resultados", []):
            for series in result.get("series", []):
                locality = series.get("localidade", {})
                values = series.get("serie", {})
                value = values.get(str(year))
                rows.append(
                    {
                        "uf_nome": locality.get("nome"),
                        "ano": year,
                        "rebanho_bovino_cabecas": value,
                    }
                )
    return rows


def extract_bovine_herd(start_year: int, end_year: int) -> pd.DataFrame:
    """Extrai efetivo bovino anual por UF na PPM/IBGE tabela 3939."""
    rows: list[dict[str, object]] = []
    for year in range(start_year, end_year + 1):
        rows.extend(_extract_year(year))

    if not rows:
        return pd.DataFrame(columns=["uf_nome", "ano", "rebanho_bovino_cabecas"])

    out = pd.DataFrame(rows)
    out["ano"] = pd.to_numeric(out["ano"], errors="coerce")
    out["rebanho_bovino_cabecas"] = pd.to_numeric(
        out["rebanho_bovino_cabecas"].astype(str).replace({"-": "0", "...": pd.NA, "..": pd.NA}),
        errors="coerce",
    )
    return out.dropna(subset=["uf_nome", "ano", "rebanho_bovino_cabecas"])

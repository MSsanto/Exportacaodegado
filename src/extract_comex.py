from __future__ import annotations

from io import StringIO

import pandas as pd
import requests

from config import COMEX_HEADING

COMEX_BULK_BASE = "https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm"
COUNTRY_TABLE_URL = "https://balanca.economia.gov.br/balanca/bd/tabelas/PAIS.csv"


def _country_lookup() -> pd.DataFrame:
    """Carrega a tabela oficial de países do Comex Stat."""
    response = requests.get(COUNTRY_TABLE_URL, timeout=60)
    response.raise_for_status()
    text = response.content.decode("latin-1")
    countries = pd.read_csv(
        StringIO(text),
        sep=";",
        dtype={"CO_PAIS": "string"},
    )
    name_col = "NO_PAIS" if "NO_PAIS" in countries.columns else "NO_PAIS_POR"
    return countries[["CO_PAIS", name_col]].rename(columns={name_col: "pais_destino"})


def _extract_year(year: int) -> pd.DataFrame:
    """Baixa um arquivo anual oficial e mantém apenas NCMs do SH4 0102."""
    url = f"{COMEX_BULK_BASE}/EXP_{year}.csv"
    usecols = [
        "CO_ANO",
        "CO_MES",
        "CO_NCM",
        "CO_PAIS",
        "SG_UF_NCM",
        "QT_ESTAT",
        "KG_LIQUIDO",
        "VL_FOB",
    ]

    parts: list[pd.DataFrame] = []
    for chunk in pd.read_csv(
        url,
        sep=";",
        encoding="latin-1",
        dtype={"CO_NCM": "string", "CO_PAIS": "string", "SG_UF_NCM": "string"},
        usecols=usecols,
        chunksize=250_000,
        low_memory=False,
    ):
        ncm = chunk["CO_NCM"].astype("string").str.zfill(8)
        selected = chunk.loc[ncm.str.startswith(COMEX_HEADING, na=False)].copy()
        if selected.empty:
            continue
        selected["CO_NCM"] = selected["CO_NCM"].astype("string").str.zfill(8)
        parts.append(selected)

    if not parts:
        return pd.DataFrame(columns=usecols)
    return pd.concat(parts, ignore_index=True)


def extract_comex_period(start: str, end: str, month_detail: bool = True) -> pd.DataFrame:
    """Extrai exportações oficiais do SH4 0102 a partir dos CSVs abertos do MDIC.

    Os arquivos anuais do Comex Stat são a fonte oficial de maior detalhe público.
    O NCM de 8 dígitos é preservado para separar bovinos domésticos, búfalos e
    outras subcategorias na análise.
    """
    start_period = pd.Period(start, freq="M")
    end_period = pd.Period(end, freq="M")

    frames = [_extract_year(year) for year in range(start_period.year, end_period.year + 1)]
    df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    if df.empty:
        return df

    df["periodo"] = pd.to_datetime(
        dict(
            year=pd.to_numeric(df["CO_ANO"], errors="coerce"),
            month=pd.to_numeric(df["CO_MES"], errors="coerce"),
            day=1,
        )
    ).dt.to_period("M")
    df = df[df["periodo"].between(start_period, end_period)].copy()

    countries = _country_lookup()
    df = df.merge(countries, on="CO_PAIS", how="left")
    df["pais_destino"] = df["pais_destino"].fillna("Código " + df["CO_PAIS"].astype(str))

    rename = {
        "CO_ANO": "ano",
        "CO_MES": "mes",
        "CO_NCM": "ncm",
        "SG_UF_NCM": "uf",
        "QT_ESTAT": "cabecas_exportadas",
        "KG_LIQUIDO": "kg_liquido",
        "VL_FOB": "valor_fob_usd",
    }
    df = df.rename(columns=rename)

    for col in ["ano", "mes", "valor_fob_usd", "kg_liquido", "cabecas_exportadas"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    columns = [
        "ano",
        "mes",
        "pais_destino",
        "uf",
        "ncm",
        "valor_fob_usd",
        "kg_liquido",
        "cabecas_exportadas",
    ]
    return df[columns]

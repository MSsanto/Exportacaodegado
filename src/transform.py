from __future__ import annotations

import unicodedata

import pandas as pd

from config import UF_TO_REGION

UF_NAME_TO_CODE = {
    "acre": "AC", "alagoas": "AL", "amapa": "AP", "amazonas": "AM", "bahia": "BA",
    "ceara": "CE", "distrito federal": "DF", "espirito santo": "ES", "goias": "GO",
    "maranhao": "MA", "mato grosso": "MT", "mato grosso do sul": "MS", "minas gerais": "MG",
    "para": "PA", "paraiba": "PB", "parana": "PR", "pernambuco": "PE", "piaui": "PI",
    "rio de janeiro": "RJ", "rio grande do norte": "RN", "rio grande do sul": "RS",
    "rondonia": "RO", "roraima": "RR", "santa catarina": "SC", "sao paulo": "SP",
    "sergipe": "SE", "tocantins": "TO",
}


def _norm(value: object) -> str:
    text = "" if value is None else str(value)
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", text) if not unicodedata.combining(ch)
    ).strip().lower()


def state_code(value: object) -> str | None:
    text = str(value).strip().upper()
    if text in UF_TO_REGION:
        return text
    return UF_NAME_TO_CODE.get(_norm(value))


def classify_ncm(ncm: object) -> str:
    code = str(ncm).replace(".", "").zfill(8)
    if code.startswith(("010221", "010229")):
        return "Bovinos domésticos"
    if code.startswith(("010231", "010239")):
        return "Búfalos"
    if code.startswith("010290"):
        return "Outros bovinos"
    return "Outros/estrutura histórica"


def transform_exports(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["uf"] = out["uf"].map(state_code)
    out["regiao"] = out["uf"].map(UF_TO_REGION)
    out["categoria_bovina"] = out["ncm"].map(classify_ncm)
    out["valor_medio_usd_cabeca"] = out["valor_fob_usd"] / out["cabecas_exportadas"].replace(0, pd.NA)
    out["kg_medio_cabeca"] = out["kg_liquido"] / out["cabecas_exportadas"].replace(0, pd.NA)
    return out


def prepare_herd(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["uf"] = out["uf_nome"].map(state_code)
    out["regiao"] = out["uf"].map(UF_TO_REGION)
    return out.dropna(subset=["uf"])


def build_regional_summary(exports: pd.DataFrame, herd: pd.DataFrame) -> pd.DataFrame:
    exp = (
        exports.groupby(["ano", "regiao"], as_index=False)
        .agg(
            cabecas_exportadas=("cabecas_exportadas", "sum"),
            valor_fob_usd=("valor_fob_usd", "sum"),
            kg_liquido=("kg_liquido", "sum"),
        )
    )
    stock = (
        herd.groupby(["ano", "regiao"], as_index=False)
        .agg(rebanho_bovino_cabecas=("rebanho_bovino_cabecas", "sum"))
    )
    out = exp.merge(stock, on=["ano", "regiao"], how="left")
    out["exportacoes_pct_rebanho"] = (
        out["cabecas_exportadas"] / out["rebanho_bovino_cabecas"] * 100
    )
    # Não interpretar como fluxo contábil. O PPM é fotografia anual do efetivo.
    out["rebanho_por_cabeca_exportada"] = (
        out["rebanho_bovino_cabecas"] / out["cabecas_exportadas"].replace(0, pd.NA)
    )
    return out

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"


def cagr(first: float, last: float, periods: int) -> float | None:
    if first <= 0 or last <= 0 or periods <= 0:
        return None
    return (last / first) ** (1 / periods) - 1


def hhi(series: pd.Series) -> float:
    shares = series / series.sum()
    return float((shares.pow(2)).sum())


def main() -> None:
    exports = pd.read_csv(DATA / "fato_exportacao_bovinos.csv")
    herd = pd.read_csv(DATA / "fato_rebanho_bovino.csv")

    closed = exports[exports["periodo_tipo"] == "Ano fechado"].copy()

    annual = (
        closed.groupby("ano", as_index=False)
        .agg(
            cabecas_exportadas=("cabecas_exportadas", "sum"),
            valor_fob_usd=("valor_fob_usd", "sum"),
            kg_liquido=("kg_liquido", "sum"),
        )
        .sort_values("ano")
    )
    annual["valor_medio_usd_cabeca"] = annual["valor_fob_usd"] / annual["cabecas_exportadas"]
    annual["yoy_cabecas_pct"] = annual["cabecas_exportadas"].pct_change() * 100
    annual["yoy_fob_pct"] = annual["valor_fob_usd"].pct_change() * 100

    destination = (
        closed.groupby(["ano", "pais_destino"], as_index=False)
        .agg(valor_fob_usd=("valor_fob_usd", "sum"), cabecas_exportadas=("cabecas_exportadas", "sum"))
    )
    concentration = (
        destination.groupby("ano")
        .apply(lambda g: pd.Series({
            "hhi_fob": hhi(g["valor_fob_usd"]),
            "hhi_cabecas": hhi(g["cabecas_exportadas"]),
            "numero_destinos": g["pais_destino"].nunique(),
        }), include_groups=False)
        .reset_index()
    )

    regional = (
        closed.groupby(["ano", "regiao"], as_index=False)
        .agg(cabecas_exportadas=("cabecas_exportadas", "sum"), valor_fob_usd=("valor_fob_usd", "sum"))
    )
    regional["share_cabecas_pct"] = regional.groupby("ano")["cabecas_exportadas"].transform(lambda s: s / s.sum() * 100)
    regional["share_fob_pct"] = regional.groupby("ano")["valor_fob_usd"].transform(lambda s: s / s.sum() * 100)

    herd_annual = herd.groupby("ano", as_index=False).agg(rebanho_bovino_cabecas=("rebanho_bovino_cabecas", "sum"))
    annual = annual.merge(herd_annual, on="ano", how="left")
    annual["exportacoes_pct_rebanho"] = annual["cabecas_exportadas"] / annual["rebanho_bovino_cabecas"] * 100

    annual.to_csv(DATA / "analise_anual.csv", index=False, encoding="utf-8-sig")
    concentration.to_csv(DATA / "concentracao_destinos.csv", index=False, encoding="utf-8-sig")
    regional.to_csv(DATA / "participacao_regional.csv", index=False, encoding="utf-8-sig")

    first = annual.iloc[0]
    last = annual.iloc[-1]
    years = int(last["ano"] - first["ano"])
    print("=== Resumo estatístico ===")
    print(f"Período: {int(first['ano'])}-{int(last['ano'])}")
    print(f"CAGR cabeças: {cagr(first['cabecas_exportadas'], last['cabecas_exportadas'], years):.2%}")
    print(f"CAGR FOB: {cagr(first['valor_fob_usd'], last['valor_fob_usd'], years):.2%}")
    print(f"Exportações/rebanho no último ano: {last['exportacoes_pct_rebanho']:.3f}%")


if __name__ == "__main__":
    main()

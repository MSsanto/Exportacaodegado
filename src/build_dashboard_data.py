from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
DASHBOARD = ROOT / "dashboard"


def _records(df: pd.DataFrame) -> list[dict]:
    return json.loads(df.to_json(orient="records", force_ascii=False))


def main() -> None:
    exports = pd.read_csv(PROCESSED / "fato_exportacao_bovinos.csv")
    herd = pd.read_csv(PROCESSED / "fato_rebanho_bovino.csv")

    exports["ano"] = pd.to_numeric(exports["ano"], errors="raise").astype(int)
    exports["mes"] = pd.to_numeric(exports["mes"], errors="raise").astype(int)
    herd["ano"] = pd.to_numeric(herd["ano"], errors="raise").astype(int)

    closed = exports[exports["periodo_tipo"].eq("Ano fechado")]
    closed_year = int(closed["ano"].max())
    latest_year = int(exports["ano"].max())
    latest_month = int(exports.loc[exports["ano"].eq(latest_year), "mes"].max())

    yearly = (
        exports.groupby("ano", as_index=False)
        .agg(
            cab=("cabecas_exportadas", "sum"),
            fob=("valor_fob_usd", "sum"),
            kg=("kg_liquido", "sum"),
        )
        .sort_values("ano")
    )
    yearly["avg"] = yearly["fob"] / yearly["cab"].replace(0, pd.NA)

    destinations = (
        exports[exports["ano"].eq(closed_year)]
        .groupby("pais_destino", as_index=False)
        .agg(cab=("cabecas_exportadas", "sum"), fob=("valor_fob_usd", "sum"))
        .sort_values("fob", ascending=False)
        .head(20)
    )

    states = (
        exports[exports["ano"].eq(closed_year)]
        .dropna(subset=["uf"])
        .groupby("uf", as_index=False)
        .agg(cab=("cabecas_exportadas", "sum"), fob=("valor_fob_usd", "sum"))
        .sort_values("fob", ascending=False)
    )

    regions = (
        exports[exports["ano"].eq(closed_year)]
        .dropna(subset=["regiao"])
        .groupby("regiao", as_index=False)
        .agg(cab=("cabecas_exportadas", "sum"), fob=("valor_fob_usd", "sum"))
        .sort_values("fob", ascending=False)
    )

    compare_years = [closed_year, latest_year] if latest_year != closed_year else [closed_year]
    monthly = (
        exports[exports["ano"].isin(compare_years)]
        .groupby(["ano", "mes"], as_index=False)
        .agg(cab=("cabecas_exportadas", "sum"), fob=("valor_fob_usd", "sum"))
        .sort_values(["ano", "mes"])
    )

    herd_yearly = (
        herd.groupby("ano", as_index=False)
        .agg(herd=("rebanho_bovino_cabecas", "sum"))
        .sort_values("ano")
    )

    payload = {
        "meta": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "closed_year": closed_year,
            "latest_year": latest_year,
            "latest_month": latest_month,
            "herd_latest_year": int(herd_yearly["ano"].max()),
            "source": "Comex Stat/MDIC + IBGE",
        },
        "y": _records(yearly.round(2)),
        "d": _records(destinations.round(2)),
        "u": _records(states.round(2)),
        "r": _records(regions.round(2)),
        "m": _records(monthly.round(2)),
        "h": _records(herd_yearly.round(2)),
    }

    DASHBOARD.mkdir(parents=True, exist_ok=True)
    target = DASHBOARD / "data.json"
    target.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"Dashboard data written to {target}")
    print(
        f"closed_year={closed_year} latest={latest_year}-{latest_month:02d} "
        f"rows={len(exports):,}"
    )


if __name__ == "__main__":
    main()

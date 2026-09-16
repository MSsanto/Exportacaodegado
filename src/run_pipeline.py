from __future__ import annotations

import pandas as pd

from config import DATA_PROCESSED, END_YEAR, START_YEAR, YTD_END_MONTH, YTD_YEAR
from extract_comex import extract_comex_period
from extract_ibge import extract_bovine_herd
from transform import build_regional_summary, prepare_herd, transform_exports


def main() -> None:
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    closed = extract_comex_period(f"{START_YEAR}-01", f"{END_YEAR}-12", month_detail=True)
    closed = transform_exports(closed)
    closed["periodo_tipo"] = "Ano fechado"

    ytd = extract_comex_period(f"{YTD_YEAR}-01", f"{YTD_YEAR}-{YTD_END_MONTH:02d}", month_detail=True)
    if not ytd.empty:
        ytd = transform_exports(ytd)
        ytd["periodo_tipo"] = f"YTD jan-{YTD_END_MONTH:02d}"
        exports = pd.concat([closed, ytd], ignore_index=True)
    else:
        exports = closed

    # PPM anual: usa apenas anos disponíveis/fechados para comparações de estoque.
    herd = prepare_herd(extract_bovine_herd(START_YEAR, END_YEAR))

    exports.to_csv(DATA_PROCESSED / "fato_exportacao_bovinos.csv", index=False, encoding="utf-8-sig")
    herd.to_csv(DATA_PROCESSED / "fato_rebanho_bovino.csv", index=False, encoding="utf-8-sig")

    regional = build_regional_summary(
        exports[exports["ano"].between(START_YEAR, END_YEAR)], herd
    )
    regional.to_csv(DATA_PROCESSED / "resumo_regional_anual.csv", index=False, encoding="utf-8-sig")

    destinations = (
        exports.groupby(["ano", "pais_destino"], as_index=False)
        .agg(
            cabecas_exportadas=("cabecas_exportadas", "sum"),
            valor_fob_usd=("valor_fob_usd", "sum"),
            kg_liquido=("kg_liquido", "sum"),
        )
        .sort_values(["ano", "valor_fob_usd"], ascending=[True, False])
    )
    destinations.to_csv(DATA_PROCESSED / "resumo_destinos_anual.csv", index=False, encoding="utf-8-sig")

    print("Pipeline concluído.")
    print(f"Exportações: {len(exports):,} linhas")
    print(f"Rebanho: {len(herd):,} linhas")
    print(f"Saída: {DATA_PROCESSED}")


if __name__ == "__main__":
    main()

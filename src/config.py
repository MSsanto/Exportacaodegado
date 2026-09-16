from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"

# Recorte principal: anos fechados. 2026 é tratado à parte como YTD.
START_YEAR = 2020
END_YEAR = 2025
YTD_YEAR = 2026
YTD_END_MONTH = 8

COMEX_API_URLS = [
    "https://api-comexstat.mdic.gov.br/general?language=pt",
    "https://api.comexstat.dth.mdic.gov.br/general?language=pt",
]

SIDRA_BASE_URL = "https://apisidra.ibge.gov.br/values"

# SIDRA PPM tabela 3939
SIDRA_TABLE = 3939
SIDRA_VARIABLE = 105  # Efetivo dos rebanhos (Cabeças)
SIDRA_HERD_CLASSIFICATION = 79
SIDRA_BOVINE_CODE = 2670

# SH4 0102 = Animais vivos da espécie bovina.
# Atenção: inclui subcategorias de bovinos domésticos, búfalos e outros bovinos.
COMEX_HEADING = "0102"

UF_TO_REGION = {
    "AC": "Norte", "AP": "Norte", "AM": "Norte", "PA": "Norte", "RO": "Norte", "RR": "Norte", "TO": "Norte",
    "AL": "Nordeste", "BA": "Nordeste", "CE": "Nordeste", "MA": "Nordeste", "PB": "Nordeste", "PE": "Nordeste", "PI": "Nordeste", "RN": "Nordeste", "SE": "Nordeste",
    "DF": "Centro-Oeste", "GO": "Centro-Oeste", "MT": "Centro-Oeste", "MS": "Centro-Oeste",
    "ES": "Sudeste", "MG": "Sudeste", "RJ": "Sudeste", "SP": "Sudeste",
    "PR": "Sul", "RS": "Sul", "SC": "Sul",
}

# Power BI — Modelo e Dashboard

## Arquivos de entrada

Após executar `python src/run_pipeline.py` e `python analysis/statistical_analysis.py`, importar:

- `data/processed/fato_exportacao_bovinos.csv`
- `data/processed/fato_rebanho_bovino.csv`
- `data/processed/resumo_regional_anual.csv`
- `data/processed/resumo_destinos_anual.csv`
- `data/processed/concentracao_destinos.csv`

## Modelo recomendado

### Fato exportação
`fato_exportacao_bovinos`

Granularidade aproximada: ano + mês + país + UF + NCM.

### Fato rebanho
`fato_rebanho_bovino`

Granularidade: ano + UF.

### Dimensões

Criar no Power BI:
- `dCalendario`
- `dUF`
- `dPais`
- `dNCM`

Evitar relacionamento direto fato-fato. Use dimensões compartilhadas.

## Páginas do dashboard

### 1. Visão Geral

Cards:
- Cabeças exportadas
- Valor FOB US$
- Valor médio US$/cabeça
- Peso médio kg/cabeça
- Rebanho bovino
- Exportações % do rebanho

Visuais:
- linha: cabeças exportadas por ano;
- linha secundária ou gráfico separado: valor FOB por ano;
- barras: valor FOB por região;
- mapa preenchido: cabeças por UF;
- tooltip com rebanho, FOB e % do rebanho.

### 2. Destinos internacionais

- mapa-múndi por país de destino;
- ranking Top 10 países por cabeças;
- ranking Top 10 por valor FOB;
- participação percentual por destino;
- HHI por ano para mostrar concentração de mercados;
- matriz país x ano.

### 3. Brasil por região e UF

- mapa do Brasil;
- barras por região;
- small multiples de UF por ano;
- exportações % do rebanho por região;
- tabela detalhada UF, cabeças, FOB, US$/cabeça, rebanho, % do rebanho.

### 4. Evolução histórica

- série 2020–2025;
- YoY cabeças;
- YoY FOB;
- CAGR do período;
- valor médio por cabeça;
- peso médio por cabeça.

### 5. 2026 YTD

Página visualmente separada com aviso `jan–ago/2026`.
Comparar preferencialmente com jan–ago dos anos anteriores, e não com anos completos.

## Segmentadores

- Ano
- Região
- UF
- País de destino
- Categoria bovina
- NCM
- Tipo de período (ano fechado / YTD)

## Design para portfólio

Sugestão visual: fundo claro, tipografia limpa e uma paleta curta inspirada no agro brasileiro. Priorizar legibilidade e narrativa; evitar excesso de velocímetros e gráficos 3D.

Título sugerido:

**Brazilian Live Cattle Exports | Trade, Geography & Herd Analytics**

Subtítulo:

**Comex Stat + IBGE/SIDRA | 2020–2026 YTD**

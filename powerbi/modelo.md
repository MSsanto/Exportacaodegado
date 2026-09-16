# Power BI — Modelo e Dashboard

## Objetivo visual

Criar um case de BI que conte uma história em três níveis:

1. **escala** — quanto o Brasil exporta e quanto isso vale;
2. **geografia** — de quais UFs/regiões sai e para quais países vai;
3. **contexto** — crescimento, concentração dos destinos e dimensão das exportações frente ao rebanho.

Título do relatório:

**Brazilian Live Cattle Exports | Trade, Geography & Herd Analytics**

Subtítulo:

**Comex Stat/MDIC + IBGE | 2020–2026 YTD**

## Arquivos de entrada

Obrigatórios:

- `data/processed/fato_exportacao_bovinos.csv`
- `data/processed/fato_rebanho_bovino.csv`

Para conferência/análises auxiliares:

- `data/processed/resumo_regional_anual.csv`
- `data/processed/resumo_destinos_anual.csv`
- arquivos gerados por `analysis/statistical_analysis.py`

As consultas prontas estão em `powerbi/power_query.md`.

## Modelo estrela

### `fato_exportacao_bovinos`

Granularidade: mês + país + UF + NCM.

Campos centrais:
- `data` — primeiro dia da competência mensal;
- `ano`, `mes`;
- `pais_destino`;
- `uf`, `regiao`;
- `ncm`, `categoria_bovina`;
- `cabecas_exportadas`;
- `valor_fob_usd`;
- `kg_liquido`.

### `fato_rebanho_bovino`

Granularidade: ano + UF.

O rebanho é **estoque anual**, não fluxo. Não relacionar diretamente as duas fatos.

### Dimensões

Criar a partir de `powerbi/dimensoes.dax`:

- `dCalendario`;
- `dUF`;
- `dPais`;
- `dNCM`.

Relacionamentos, sempre com filtro em uma direção (dimensão → fato):

- `dCalendario[Data]` 1:* `fato_exportacao_bovinos[data]`;
- `dUF[uf]` 1:* `fato_exportacao_bovinos[uf]`;
- `dUF[uf]` 1:* `fato_rebanho_bovino[uf]`;
- `dPais[pais_destino]` 1:* `fato_exportacao_bovinos[pais_destino]`;
- `dNCM[ncm]` 1:* `fato_exportacao_bovinos[ncm]`.

As medidas de rebanho usam `TREATAS` para transferir o ano selecionado do calendário à fato anual.

## Página 1 — Visão Geral

### Faixa superior

Segmentadores compactos:
- Ano;
- Região;
- Categoria bovina;
- País de destino.

### Cards

1. `Cabeças Exportadas`
2. `Valor FOB USD`
3. `Valor Médio USD por Cabeça`
4. `Peso Médio Kg por Cabeça`
5. `Rebanho Bovino`
6. `Exportações % do Rebanho`

Para 2025/2026, quando ainda não houver efetivo do mesmo ano no IBGE, o card de `% do rebanho` deve ficar em branco em vez de usar estoque de outro ano.

### Corpo

- **Linha:** cabeças exportadas por ano/mês;
- **Linha ou área separada:** valor FOB no tempo;
- **Barras horizontais:** cabeças por região;
- **Mapa do Brasil:** cabeças por UF;
- **Top 5 destinos:** barras por valor FOB.

Mensagem que a página deve responder: **qual é a dimensão do mercado e onde está concentrado?**

## Página 2 — Destinos Internacionais

### Visuais

- mapa-múndi: tamanho = `Valor FOB USD`, localização = país;
- Top 10 países por FOB;
- Top 10 países por cabeças;
- matriz `País × Ano` com FOB, cabeças e US$/cabeça;
- gráfico de participação dos cinco maiores destinos;
- linha do HHI anual, calculado no pipeline estatístico.

### Storytelling

Destacar que a concentração muda bastante ao longo do período. Em 2023, por exemplo, a Turquia respondeu por cerca de 59% do valor FOB do SH4 0102; em 2025 a participação caiu para aproximadamente 32%, com Marrocos, Iraque e Egito ganhando peso.

## Página 3 — Brasil por Região e UF

### Visuais

- mapa preenchido ou bolhas por UF;
- ranking de UFs por cabeças;
- barras empilhadas por região e ano;
- tabela detalhada com UF, região, cabeças, FOB e US$/cabeça;
- para anos com rebanho disponível: `Exportações % do Rebanho`.

### Destaque validado

Em 2025, o Norte respondeu por cerca de **61,9% das cabeças exportadas**. O Pará liderou com **598.087 cabeças** e aproximadamente **US$ 574,8 milhões**.

## Página 4 — Evolução Histórica

### Visuais

- linha 2020–2025 de cabeças;
- linha 2020–2025 de FOB;
- colunas de `Variação Cabeças YoY %`;
- colunas de `Variação FOB YoY %`;
- linha de `Valor Médio USD por Cabeça`;
- linha de `Peso Médio Kg por Cabeça`.

### KPIs de período

CAGR validado 2020–2025:
- cabeças: aproximadamente **26,1% a.a.**;
- valor FOB: aproximadamente **36,9% a.a.**.

O forte recuo de 2021 deve aparecer como quebra relevante da série, evitando representar a trajetória como crescimento linear.

## Página 5 — 2026 YTD

Página dedicada para não comparar período parcial com ano cheio.

### Cards

- 917.564 cabeças em jan–ago/2026;
- US$ 1,173 bi FOB;
- US$ 1.278,88/cabeça;
- +40,6% em cabeças vs jan–ago/2025;
- +88,6% em FOB vs jan–ago/2025.

### Visuais

- 2025 vs 2026 por mês, até agosto;
- destinos de 2026;
- UFs de origem em 2026;
- evolução mensal de US$/cabeça.

Use as medidas YTD de `powerbi/medidas.dax`; não compare 2026 YTD com o total de 2025.

## Tooltips

Criar uma página de tooltip para UF contendo:

- UF e região;
- cabeças;
- FOB;
- US$/cabeça;
- kg/cabeça;
- rebanho no ano, quando disponível;
- exportações % do rebanho, quando o ano de estoque coincidir.

Criar outra para país:

- cabeças;
- FOB;
- participação no FOB;
- ranking;
- US$/cabeça.

## Segmentadores

- Ano
- Mês/Ano
- Região
- UF
- País de destino
- Categoria bovina
- NCM
- Tipo de período (`Ano fechado` / `YTD`)

## Formatação

- FOB: moeda USD, unidades automáticas em mi/bi;
- cabeças e kg: separador de milhares, sem casas quando número absoluto;
- percentuais: 1 casa decimal;
- US$/cabeça: 2 casas;
- títulos dinâmicos usando `Texto Período Selecionado`.

## Design para portfólio

- fundo claro ou quase branco;
- grid consistente e bastante espaço em branco;
- uma cor de destaque para exportação e uma segunda para contexto/rebanho;
- evitar gráficos 3D, velocímetros e excesso de ícones;
- no máximo 5–6 visuais principais por página;
- colocar fonte e período no rodapé: `MDIC/Comex Stat + IBGE | atualização: ago/2026`.

O objetivo é parecer um produto de **Business Intelligence**, não apenas uma coleção de gráficos.

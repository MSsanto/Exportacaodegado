# Brazilian Live Cattle Exports — Data Analytics Portfolio

![Data pipeline](https://github.com/MSsanto/Exportacaodegado/actions/workflows/data-pipeline.yml/badge.svg)

Análise reproduzível das exportações brasileiras de animais vivos da espécie bovina, combinando **Comex Stat/MDIC**, **IBGE**, **Python**, **GitHub Actions** e **Power BI**.

O projeto responde perguntas de negócio e inteligência de mercado como:

- Quantas cabeças o Brasil exporta por ano?
- Quanto essas exportações movimentam em US$ FOB?
- Quais países compram mais?
- Quais UFs e regiões brasileiras mais exportam?
- Qual o valor médio por cabeça?
- Qual o tamanho do rebanho bovino por região?
- Qual a escala das exportações frente ao efetivo do rebanho?
- O mercado comprador está concentrado em poucos países?
- Como volume, valor e preço médio evoluíram nos últimos anos?

## Resultados validados

O pipeline foi executado com sucesso no GitHub Actions em **16/09/2026**.

| Período | Cabeças exportadas | Valor FOB | US$/cabeça |
|---|---:|---:|---:|
| 2020 | 329.007 | US$ 217,2 mi | 660,03 |
| 2021 | 62.297 | US$ 68,5 mi | 1.099,27 |
| 2022 | 194.891 | US$ 192,3 mi | 986,47 |
| 2023 | 582.328 | US$ 488,7 mi | 839,14 |
| 2024 | 1.000.887 | US$ 829,6 mi | 828,82 |
| 2025 | 1.050.390 | US$ 1,046 bi | 995,44 |
| 2026 jan–ago | 917.564 | US$ 1,173 bi | 1.278,88 |

Em 2026 jan–ago, as exportações cresceram **40,6% em cabeças** e **88,6% em valor FOB** em relação ao mesmo período de 2025.

Em 2025, o **Pará** liderou as exportações com **598.087 cabeças** e aproximadamente **US$ 574,8 milhões**. A região Norte respondeu por cerca de **61,9% das cabeças** exportadas no ano.

Os resultados detalhados estão em [`docs/resultados_validados.md`](docs/resultados_validados.md), e a série anual compacta está em [`data/published/resumo_anual.csv`](data/published/resumo_anual.csv).

## Stack

- Python
- pandas
- requests
- Comex Stat / dados abertos do MDIC
- API de Agregados do IBGE
- GitHub Actions
- Power BI
- DAX
- Git/GitHub

## Fontes oficiais

### Comex Stat / MDIC

Base oficial de comércio exterior do Brasil.

Recorte principal: SH4 `0102` — **Animais vivos da espécie bovina**.

O pipeline baixa os arquivos anuais oficiais detalhados por NCM e processa somente o SH4 0102 em chunks, evitando carregar os arquivos completos em memória.

Métricas:
- quantidade estatística;
- quilograma líquido;
- valor FOB em US$.

Dimensões:
- ano e mês;
- NCM;
- país de destino;
- UF do produto.

### IBGE

Pesquisa da Pecuária Municipal, tabela 3939 — **Efetivo dos rebanhos, por tipo de rebanho**.

A extração usa a API oficial de Agregados do IBGE.

Recorte:
- bovinos;
- Unidade da Federação;
- periodicidade anual.

No momento da validação, o último efetivo anual retornado para a série utilizada foi **2024**.

## Período

- `2020–2025`: anos completos para análise histórica.
- `2026`: YTD janeiro–agosto, exibido separadamente e comparado com janeiro–agosto de 2025.

## Sobre “quanto fica no Brasil”

O projeto **não** calcula `rebanho - exportações` como se fosse um saldo físico. Isso seria incorreto, porque o efetivo do rebanho é um estoque anual que já incorpora nascimentos, mortes, abates e movimentações.

Em vez disso, usamos:

`Exportações % do Rebanho = Cabeças Exportadas / Efetivo Bovino Anual`

Esse indicador mostra o tamanho relativo do fluxo exportador diante do estoque bovino.

## Estrutura

```text
Exportacaodegado/
├── .github/
│   └── workflows/
│       └── data-pipeline.yml
├── analysis/
│   └── statistical_analysis.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── published/
│       └── resumo_anual.csv
├── docs/
│   ├── metodologia.md
│   └── resultados_validados.md
├── powerbi/
│   ├── medidas.dax
│   └── modelo.md
├── src/
│   ├── config.py
│   ├── extract_comex.py
│   ├── extract_ibge.py
│   ├── run_pipeline.py
│   └── transform.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Como executar

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/run_pipeline.py
python analysis/statistical_analysis.py
```

Os arquivos tratados serão gerados em `data/processed/`.

O workflow `.github/workflows/data-pipeline.yml` executa automaticamente a coleta e validação, além de publicar os CSVs prontos para Power BI como artefato do GitHub Actions.

## Saídas analíticas

O pipeline gera bases para o Power BI com:

- exportações por mês, país, UF e NCM;
- rebanho bovino por UF;
- resumo regional anual;
- ranking anual de destinos;
- análise anual com YoY;
- participação regional;
- concentração de destinos via HHI.

## Indicadores estatísticos

- Cabeças exportadas
- Valor FOB em US$
- Quilogramas líquidos
- Valor médio por cabeça
- Peso médio por cabeça
- Variação anual (YoY)
- CAGR do período
- Participação regional
- Participação por destino
- HHI de concentração dos países compradores
- Exportações como % do rebanho

## Dashboard Power BI

O projeto prevê cinco páginas:

1. **Visão Geral**
2. **Destinos Internacionais**
3. **Brasil por Região e UF**
4. **Evolução Histórica**
5. **2026 YTD**

As medidas DAX estão em `powerbi/medidas.dax` e a especificação visual/modelagem em `powerbi/modelo.md`.

## Escopo NCM

A posição 0102 inclui subposições de bovinos domésticos, búfalos e outros bovinos. O pipeline preserva o NCM detalhado e cria a variável `categoria_bovina`, permitindo exibir tanto a visão ampla da posição 0102 quanto filtros específicos.

## Automação

O GitHub Actions:

1. instala o ambiente Python;
2. baixa dados oficiais do MDIC e IBGE;
3. executa o ETL;
4. valida se os datasets foram gerados e não estão vazios;
5. publica os CSVs processados como artefato;
6. executa novamente a cada atualização mensal programada.

## Próximas evoluções

- construir o arquivo `.pbix`;
- adicionar screenshots do dashboard ao repositório;
- publicar uma versão web integrada ao portfólio;
- adicionar comparação com exportação de carne bovina em uma fase separada.

## Autor

**Matheus Sergio Faria Santo**

Projeto de portfólio em Data Analytics / Business Intelligence.

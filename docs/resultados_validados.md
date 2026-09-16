# Resultados validados

Resultados gerados pela execução bem-sucedida do pipeline em 16/09/2026, usando dados oficiais do MDIC/Comex Stat e IBGE.

## Exportações anuais — SH4 0102

| Período | Cabeças | Valor FOB | US$/cabeça | Variação de cabeças | Variação FOB |
|---|---:|---:|---:|---:|---:|
| 2020 | 329.007 | US$ 217,2 mi | 660,03 | — | — |
| 2021 | 62.297 | US$ 68,5 mi | 1.099,27 | -81,1% | -68,5% |
| 2022 | 194.891 | US$ 192,3 mi | 986,47 | +212,8% | +180,7% |
| 2023 | 582.328 | US$ 488,7 mi | 839,14 | +198,8% | +154,2% |
| 2024 | 1.000.887 | US$ 829,6 mi | 828,82 | +71,9% | +69,8% |
| 2025 | 1.050.390 | US$ 1,046 bi | 995,44 | +5,0% | +26,0% |
| 2026 jan–ago | 917.564 | US$ 1,173 bi | 1.278,88 | +40,6% vs jan–ago/2025 | +88,6% vs jan–ago/2025 |

Entre 2020 e 2025, o CAGR foi de aproximadamente **26,1% em cabeças** e **36,9% em valor FOB**. O ano de 2021 é um ponto de forte contração e deve ser tratado como quebra relevante na série, não como tendência estrutural isolada.

## Destinos

Em 2025, os maiores destinos por valor FOB foram:

1. Turquia — US$ 334,9 mi (32,0%)
2. Marrocos — US$ 218,7 mi (20,9%)
3. Iraque — US$ 170,6 mi (16,3%)
4. Egito — US$ 130,6 mi (12,5%)
5. Líbano — US$ 89,4 mi (8,6%)

Em 2026 jan–ago, Turquia, Marrocos e Iraque continuaram liderando, somando a maior parte do valor exportado.

O HHI calculado sobre a participação dos países no valor FOB mostra concentração elevada em alguns anos, especialmente em 2023, quando a Turquia respondeu por cerca de 59% do valor exportado.

## Regiões e UFs

Em 2024, último ano com efetivo bovino disponível no conjunto consultado do IBGE:

- Norte: 635.381 cabeças exportadas, equivalentes a 0,98% do efetivo bovino regional;
- Sul: 262.186 cabeças, equivalentes a 1,07% do efetivo regional;
- Sudeste: 33.963 cabeças, 0,09% do efetivo;
- Centro-Oeste: 29.995 cabeças, 0,04% do efetivo;
- Nordeste: 2.328 cabeças, 0,006% do efetivo.

Em 2025, o Norte respondeu por 61,9% das cabeças exportadas e 60,8% do valor FOB. O Pará liderou com 598.087 cabeças e US$ 574,8 milhões.

## Interpretação de “quanto fica no Brasil”

O projeto não usa `rebanho - exportações` como saldo. O efetivo bovino do IBGE é uma fotografia anual e sofre efeito de nascimentos, mortes, abates, importações, exportações e outras movimentações. O indicador utilizado é **exportações como % do rebanho**, que mede a escala relativa do fluxo exportador frente ao estoque.

## Nota metodológica

A posição SH4 0102 inclui bovinos domésticos, búfalos e outros bovinos. O dataset preserva o NCM de 8 dígitos e a variável `categoria_bovina`, permitindo separar essas categorias no Power BI.

2026 é período parcial (jan–ago). Suas variações são calculadas contra jan–ago de 2025, e não contra o ano cheio de 2025.

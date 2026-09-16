# Metodologia

## Objetivo

Responder, com dados oficiais e metodologia reproduzível:

1. Quantas cabeças de animais vivos da espécie bovina o Brasil exporta?
2. Qual o valor FOB dessas exportações?
3. Quais são os principais países de destino?
4. Quais UFs e regiões brasileiras originam as exportações?
5. Qual é o tamanho do rebanho bovino brasileiro por UF/região?
6. Qual a razão entre cabeças exportadas e o efetivo anual do rebanho?
7. Como volume, valor, preço médio e concentração de destinos mudam ao longo do tempo?

## Fontes

### Comex Stat / MDIC

Fonte oficial das estatísticas brasileiras de comércio exterior.

Recorte: posição SH4 `0102` — animais vivos da espécie bovina.

Campos usados:
- ano e mês;
- NCM;
- país de destino;
- UF do produto;
- quantidade estatística;
- quilograma líquido;
- valor FOB em US$.

A UF utilizada pelo módulo de Dados Gerais do Comex Stat corresponde à UF do produto/estado produtor segundo a metodologia da Secex, e não necessariamente ao domicílio fiscal do exportador.

### IBGE / SIDRA

Pesquisa da Pecuária Municipal (PPM), tabela 3939 — efetivo dos rebanhos por tipo de rebanho.

Recorte:
- variável: efetivo dos rebanhos (cabeças);
- tipo de rebanho: bovino;
- nível territorial: Unidade da Federação;
- periodicidade: anual.

## Janela temporal

- Série principal: 2020–2025, anos fechados.
- 2026: apresentado apenas como YTD janeiro–agosto, sem comparação direta com anos completos.
- Rebanho PPM: somente anos anuais disponíveis e fechados.

## Definição de “quanto fica no Brasil”

Não é metodologicamente correto calcular `rebanho anual - exportações anuais` e chamar o resultado de “gado que ficou”. O efetivo do rebanho é uma fotografia anual que já incorpora nascimentos, mortes, abates, importações, exportações e outras movimentações.

Por isso, o dashboard usa:

`Exportações % do Rebanho = cabeças exportadas / efetivo bovino anual`

Esse indicador mede a escala relativa das exportações frente ao estoque, sem sugerir uma falsa identidade contábil.

## NCM e escopo bovino

O SH4 0102 inclui animais vivos da espécie bovina. Dentro dele existem subposições de bovinos domésticos, búfalos e outros bovinos. O dataset preserva o NCM de 8 dígitos e cria `categoria_bovina`, permitindo:

- visão ampla do SH4 0102;
- filtro específico para bovinos domésticos;
- identificação de búfalos e outros bovinos.

## Indicadores estatísticos

- cabeças exportadas;
- valor FOB (US$);
- kg líquido;
- valor médio FOB por cabeça;
- peso médio por cabeça;
- variação YoY de cabeças e valor;
- CAGR no período;
- participação por região;
- participação por país de destino;
- índice HHI para concentração de destinos;
- exportações como % do efetivo bovino.

## Limitações

1. 2026 é parcial.
2. Valor FOB não inclui frete e seguro internacionais.
3. Efetivo do rebanho é estoque anual; exportações são fluxo ao longo do ano.
4. A comparação `exportações / rebanho` é uma razão de escala, não uma equação de estoque.
5. Mudanças históricas da NCM exigem cautela em séries muito longas; o recorte 2020+ reduz esse problema.
6. O projeto não mede exportação de carne bovina; mede animais vivos da espécie bovina.

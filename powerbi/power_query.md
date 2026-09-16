# Power Query — importação dos datasets

O Power BI Desktop deve consumir os CSVs gerados pelo pipeline em `data/processed/`.

## 1. Parâmetro `BasePath`

Crie um parâmetro de texto chamado `BasePath` apontando para a pasta local do repositório, por exemplo:

```text
C:\Users\SEU_USUARIO\Documents\GitHub\Exportacaodegado
```

Assim, trocar de computador exige alterar apenas um parâmetro.

## 2. `fato_exportacao_bovinos`

Crie uma consulta em branco e cole no Editor Avançado:

```powerquery
let
    Fonte = Csv.Document(
        File.Contents(BasePath & "\\data\\processed\\fato_exportacao_bovinos.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    Cabecalhos = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(
        Cabecalhos,
        {
            {"ano", Int64.Type},
            {"mes", Int64.Type},
            {"pais_destino", type text},
            {"uf", type text},
            {"ncm", type text},
            {"valor_fob_usd", Currency.Type},
            {"kg_liquido", type number},
            {"cabecas_exportadas", type number},
            {"regiao", type text},
            {"categoria_bovina", type text},
            {"data", type date},
            {"valor_medio_usd_cabeca", Currency.Type},
            {"kg_medio_cabeca", type number},
            {"periodo_tipo", type text}
        },
        "pt-BR"
    )
in
    Tipos
```

## 3. `fato_rebanho_bovino`

```powerquery
let
    Fonte = Csv.Document(
        File.Contents(BasePath & "\\data\\processed\\fato_rebanho_bovino.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    Cabecalhos = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(
        Cabecalhos,
        {
            {"uf_nome", type text},
            {"ano", Int64.Type},
            {"rebanho_bovino_cabecas", type number},
            {"uf", type text},
            {"regiao", type text}
        },
        "pt-BR"
    )
in
    Tipos
```

## 4. Tabelas-resumo opcionais

As tabelas `resumo_regional_anual.csv` e `resumo_destinos_anual.csv` são úteis para conferência e prototipação, mas o dashboard principal deve preferir as duas fatos e as dimensões do modelo estrela. Isso reduz duplicação de lógica.

## 5. Dimensões e medidas

Depois de carregar as fatos:

1. crie as tabelas de `powerbi/dimensoes.dax`;
2. marque `dCalendario` como tabela de datas;
3. crie os relacionamentos indicados no arquivo;
4. adicione as medidas de `powerbi/medidas.dax`;
5. formate percentuais, moedas e milhares no painel de modelo.

## 6. Atualização

Para atualizar o `.pbix`:

```powershell
python src/run_pipeline.py
```

Depois use **Atualizar** no Power BI Desktop. O GitHub Actions também executa e valida o mesmo pipeline periodicamente; seus CSVs ficam disponíveis como artefato da execução.

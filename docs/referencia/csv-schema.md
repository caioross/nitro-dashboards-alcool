---
title: Referência — Schema do CSV
resumo: Colunas esperadas, reconhecimento por regex, normalização numérica, validações e exemplos.
atualizado_em: 2026-09-10
responsavel: docs-site-nitro
tags: [referencia, csv, schema, parsing]
---

# Referência — Schema do CSV

O parser é deliberadamente tolerante: não exige nomes de coluna exatos, autodetecta separador
e aceita decimais em pt-BR e en-US. Esta página descreve o que o painel entende.

## Sumário
- [Requisitos mínimos](#requisitos-mínimos)
- [Coluna de país](#coluna-de-país)
- [Colunas de métrica reconhecidas](#colunas-de-métrica-reconhecidas)
- [Colunas genéricas](#colunas-genéricas)
- [Separador e aspas](#separador-e-aspas)
- [Normalização numérica](#normalização-numérica)
- [Validações e erros](#validações-e-erros)
- [Exemplos](#exemplos)
- [Referências cruzadas](#referências-cruzadas)

## Requisitos mínimos

- Pelo menos **um cabeçalho + uma linha de dados** (`index.html:1187`).
- Pelo menos **uma coluna de país** e **uma coluna numérica** (`index.html:1196`, `1212`).

## Coluna de país

`buildDataset` detecta a coluna de país em duas etapas (`index.html:1192-1196`):

1. **Por nome** — regex `^(country|país|pais|nation|nação|nacao|territ...)` (case-insensitive).
2. **Por conteúdo** — se nenhuma casar, escolhe a primeira coluna cujas 20 primeiras linhas são
   todas texto não numérico.

Se nada casar, lança: *"Nenhuma coluna de país encontrada. Colunas lidas: ..."*.

## Colunas de métrica reconhecidas

Definidas em `COLDEFS` (`index.html:1179-1184`). A primeira coluna (fora a de país) que casa
a regex vira a métrica:

| key | Regex (case-insensitive) | Rótulo | Unidade |
|---|---|---|---|
| `beer` | `beer\|cerveja` | Cerveja | doses/pessoa/ano |
| `spirit` | `spirit\|destil\|liquor\|licor\|cacha\|vodka` | Destilados | doses/pessoa/ano |
| `wine` | `wine\|vinho` | Vinho | doses/pessoa/ano |
| `total` | `total.*(litre\|liter\|litro)\|pure_?alcohol\|alcoól puro\|litres` | Álcool puro | litros/pessoa/ano |

> [!NOTE]
> A métrica `total` recebe tratamento especial de formatação (1 casa decimal) em vários
> renderers, ex.: `fmt(v, m.key === 'total' ? 1 : 0)` (`index.html:1701`).

## Colunas genéricas

Qualquer outra coluna numérica vira uma métrica `x<i>` **se ao menos 60% das linhas forem
valores finitos** (`index.html:1205-1211`). Rótulo e nome curto = o próprio cabeçalho; unidade
vazia. Isso permite carregar planilhas com métricas arbitrárias.

## Separador e aspas

- **Separador**: autodetectado entre `,`, `;`, `\t`, `|` contando ocorrências no cabeçalho
  (`detectDelim`, `index.html:1140`).
- **Aspas**: RFC 4180 — campos entre aspas podem conter o separador e `""` representa uma aspa
  literal (`index.html:1156`).
- **BOM**: removido (`index.html:1150`).
- **Quebras de linha**: `\r\n` e `\r` normalizados para `\n`.

## Normalização numérica

`toNum` (`index.html:1166-1176`):

| Padrão de entrada | Regra | Exemplo |
|---|---|---|
| `1.234,56` | remove `.` de milhar, `,`→`.` | `1234.56` |
| `1,234.56` | remove `,` de milhar | `1234.56` |
| `4,9` | `,`→`.` | `4.9` |
| `4.9` | inalterado | `4.9` |
| vazio / não numérico | vira `NaN` | — |

## Validações e erros

| Mensagem | Causa | Fonte |
|---|---|---|
| "O arquivo precisa de um cabeçalho e ao menos uma linha de dados." | `rows.length < 2` | `index.html:1187` |
| "Nenhuma coluna de país encontrada. Colunas lidas: ..." | detecção de país falhou | `index.html:1196` |
| "Nenhuma coluna numérica encontrada. Colunas lidas: ..." | nenhuma métrica reconhecida/genérica | `index.html:1212` |
| "Nenhuma linha de dados válida encontrada." | todas as linhas vazias/duplicadas | `index.html:1231` |

Todas são capturadas por `ingest` e exibidas via `showErr` no intake (`index.html:1325-1326`).

## Exemplos

Formato canônico ([`Dados/drinks.csv`](../../Dados/drinks.csv), 193 países):

```csv
country,beer_servings,spirit_servings,wine_servings,total_litres_of_pure_alcohol
Afghanistan,0,0,0,0.0
Albania,89,132,54,4.9
Algeria,25,0,14,0.7
```

Variante pt-BR (também aceita):

```csv
país;cerveja;destilados;vinho;álcool_puro
Brasil;245;145;16;7,2
Portugal;194;67;339;11,0
```

## Referências cruzadas

- [Estruturas de dados](estruturas-de-dados.md)
- [Fluxo de dados](../arquitetura/fluxo-de-dados.md)
- [Funções internas](funcoes.md)
</content>

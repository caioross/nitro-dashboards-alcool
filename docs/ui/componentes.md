---
title: UI — Componentes
resumo: Cada componente visual do painel — KPIs, mapa, gráficos, filtros, chat e clima — com estado e eventos.
atualizado_em: 2026-09-10
responsavel: docs-site-nitro
tags: [ui, componentes, svg, interacao]
---

# UI — Componentes

Todos os componentes leem `filtered()`/`activeMetric()` e são repintados por `paint()`. Nenhum
usa framework — são funções que desenham SVG/DOM.

## Sumário
- [Barra superior](#barra-superior-header)
- [Intake (landing)](#intake-landing)
- [Rail de filtros](#rail-de-filtros)
- [KPIs](#kpis)
- [Mapa coroplético](#mapa-coroplético)
- [Matriz de correlação](#matriz-de-correlação)
- [Dispersão](#dispersão)
- [Ranking](#ranking)
- [Composição por continente](#composição-por-continente)
- [Histograma](#histograma)
- [r por continente](#r-por-continente)
- [Tabela analítica](#tabela-analítica)
- [Chat com IA](#chat-com-ia)
- [Widget de clima](#widget-de-clima)
- [Suporte](#suporte)
- [Referências cruzadas](#referências-cruzadas)

## Barra superior (header)

`index.html:661-697`. Contém logo, widget de clima (`#wx`), metadados do arquivo (`#fileMeta`),
"Exportar seleção" (`#btnExport`) e "Importar CSV" (`#btnPick`). O botão de export só aparece
após a primeira importação (`index.html:1341`).

## Intake (landing)

`index.html:699-726`. Dropzone (`#drop`), botões "Selecionar arquivo" e "Carregar amostra", e o
esquema de colunas de exemplo. Erros de importação aparecem em `#intakeErr` via `showErr`.

## Rail de filtros

`index.html:731-761`. Fonte de todas as mutações de filtro:

| Controle | ID | Evento | Efeito no ST |
|---|---|---|---|
| Segmento de bebida | `#segMetric` | click | `ST.metric` + `resetRange()` |
| Chips de continente | `#chipsCont` | click | alterna em `ST.conts` |
| Busca de país | `#qCountry` | input (debounce 140 ms) | `ST.q` |
| Faixa min/max | `#rngMin`/`#rngMax` | input | `ST.lo`/`ST.hi` |
| Limpar filtros | `#btnReset` | click | zera tudo |

## KPIs

`index.html:1482-1524`. 7 cards (`KPI_DEFS`): Países, Soma, Média, Mediana, Máximo, Mínimo,
Desvio padrão. Valores animados por `countUp`. Máx/Mín mostram quem (ou "N países empatados");
Desvio padrão mostra o CV (%).

## Mapa coroplético

`index.html:1526-1734`. Projeção Natural Earth I. Escala selecionável (quantil/linear/sqrt).

| Interação | Efeito |
|---|---|
| hover | tooltip com todas as métricas do país |
| clique | isola o país (preenche a busca) — `bindGeo` (`index.html:1678`) |
| `Ctrl/⌘ + roda` | zoom no ponto do cursor |
| arrastar | pan |
| `#zIn`/`#zOut`/`#zRst` | zoom in/out/reenquadrar |

Microestados sem geometria no atlas 110m viram pontos a partir de `CMETA[...].p`
(`index.html:1655-1668`). O subtítulo conta `drawn + dots` países georreferenciados.

## Matriz de correlação

`index.html:1736-1804`. Heatmap n×n (até 6 métricas) de Pearson, cor diverging. Clique numa
célula define o par X/Y da dispersão (`index.html:1779-1782`). Tooltip mostra r, r², n e p.

## Dispersão

`index.html:1806-1875`. Pontos por país (cor por continente), reta de regressão animada, caixa
com r, r² e p-valor. O subtítulo classifica a força (muito forte/forte/moderada/fraca/desprezível)
e imprime a equação da reta.

## Ranking

`index.html:1877-1912`. Top ou base 14 países na métrica ativa (`#rkTop`/`#rkBot`). Barras
animadas coloridas por continente; clique isola o país.

## Composição por continente

`index.html:1914-1975`. Barras 100% empilhadas de cerveja/destilados/vinho (média das doses),
reveladas por máscara de clip para nunca aparecerem separadas. Requer ao menos 2 dessas colunas.

## Histograma

`index.html:1977-2033`. Bins = √n (clampado 6–18), faixa sombreada ±1σ, linhas de média (μ) e
mediana (Md). Tooltip por classe mostra contagem e frequência (%).

## r por continente

`index.html:2035-2066`. r de Pearson do par X/Y por bloco geográfico (mínimo 4 países), com
barra diverging centrada em 0.

## Tabela analítica

`index.html:2068-2121`. Base ordenável por qualquer coluna (`ST.sortKey`/`sortDir`); a coluna
da métrica ativa ganha uma mini-barra proporcional. Hover mostra o mesmo tooltip do mapa.

## Chat com IA

`index.html:942-983` (markup) + `index.html:2396-2769` (lógica). Painel com chips de escopo
(`#aiScope`) que espelham os filtros ativos, log de mensagens, sugestões e campo de entrada
(Enter envia, Shift+Enter quebra linha). Ver [Integrações](../referencia/integracoes.md#gemini-chat).

## Widget de clima

`index.html:672-682` (markup) + `index.html:2289-2394` (lógica). Mostra temperatura, descrição,
mín/máx, sensação e umidade. Clicável quando precisa de cidade manual.
Ver [Integrações](../referencia/integracoes.md#openweathermap-clima).

## Suporte

`index.html:894-940` (markup) + `index.html:2172-2235` (lógica). Botão flutuante + modal com
formulário. Envia ao Supabase. Ver [ADR-0003](../arquitetura/decisoes/ADR-0003-suporte-supabase.md).

## Referências cruzadas

- [Design system](design-system.md)
- [Módulos](../arquitetura/modulos.md)
- [Funções internas](../referencia/funcoes.md)
- [Integrações](../referencia/integracoes.md)
</content>

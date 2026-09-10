---
title: Referência — Funções internas
resumo: API interna do index.html — assinatura, parâmetros, retorno e efeitos colaterais das funções principais.
atualizado_em: 2026-09-10
responsavel: docs-site-nitro
tags: [referencia, api, funcoes, javascript]
---

# Referência — Funções internas

Todas as funções vivem no `<script>` de `index.html`. Não há módulos ES nem exports; o
escopo é o próprio script (`'use strict'` em `index.html:1001`). Blocos de integração são
IIFEs, então algumas funções (chat, clima, suporte) não são acessíveis de fora.

## Sumário
- [Helpers DOM e formatação](#helpers-dom-e-formatação)
- [Estatística (objeto S)](#estatística-objeto-s)
- [Cores](#cores)
- [Animação](#animação)
- [Parsing de CSV](#parsing-de-csv)
- [Projeção e TopoJSON](#projeção-e-topojson)
- [Estado e filtragem](#estado-e-filtragem)
- [IO e ingestão](#io-e-ingestão)
- [Renderers](#renderers)
- [Ciclo de render](#ciclo-de-render)
- [Referências cruzadas](#referências-cruzadas)

## Helpers DOM e formatação

| Função | Assinatura | Retorno | Efeitos | Fonte |
|---|---|---|---|---|
| `$` | `(sel, root?)` | primeiro `Element` | — | `index.html:1004` |
| `$$` | `(sel, root?)` | `Element[]` | — | `index.html:1005` |
| `el` | `(tag, attrs?, parent?)` | nó SVG criado | anexa a `parent` se dado; chave `text` vira `textContent` | `index.html:1008` |
| `clear` | `(node)` | — | remove todos os filhos | `index.html:1017` |
| `fmt` | `(v, d?)` | `string` | `—` para não finito; usa `NF/NF1/NF2` | `index.html:1022` |
| `fmtR` | `(v)` | `string` | correlação com sinal `+`/`−` e vírgula decimal | `index.html:1029` |
| `clamp` | `(v, a, b)` | `number` | — | `index.html:1030` |
| `lerp` | `(a, b, t)` | `number` | — | `index.html:1031` |

## Estatística (objeto S)

Definido em `index.html:1034-1078`.

| Método | Assinatura | Retorno | Nota |
|---|---|---|---|
| `S.sum` | `(a)` | `number` | soma simples |
| `S.mean` | `(a)` | `number` | `NaN` se vazio |
| `S.median` | `(a)` | `number` | atalho para `quantile(a, .5)` |
| `S.quantile` | `(a, q)` | `number` | interpolação linear entre índices |
| `S.min` / `S.max` | `(a)` | `number` | `NaN` se vazio |
| `S.sd` | `(a)` | `number` | desvio padrão **amostral** (n−1); `NaN` se `n<2` |
| `S.pearson` | `(x, y)` | `number` | `NaN` se `n<3` ou denominador zero |
| `S.linreg` | `(x, y)` | `{slope, intercept}` | mínimos quadrados |
| `S.pValue` | `(r, n)` | `number` | p bicaudal via transformação z de Fisher; `NaN` se `n<4` |

Auxiliares: `erf` (Abramowitz & Stegun 7.1.26, `index.html:1079`), `normCdf` (`index.html:1085`),
`fmtP` (formata p com vírgula, ou `p < 0,0001`, `index.html:1086`).

```js
// exemplo real de uso — index.html:1840, 1866
const r = S.pearson(xs, ys);
const { slope, intercept } = S.linreg(xs, ys);
// caixa estatística mostra r, r² e p
fmtP(S.pValue(r, pts.length));
```

## Cores

| Função | Assinatura | Retorno | Fonte |
|---|---|---|---|
| `hex2rgb` | `(h)` | `[r,g,b]` | `index.html:1099` |
| `rgb2css` | `(c)` | `rgb(...)` | `index.html:1100` |
| `rampColor` | `(t)` | cor da rampa coroplética em `t∈[0,1]` | `index.html:1101` |
| `divColor` | `(r)` | cor diverging para `r∈[-1,1]` | `index.html:1107` |

## Animação

| Função | Assinatura | Efeitos | Fonte |
|---|---|---|---|
| `settle` | `(node, delay)` | adiciona `.done` após `delay+900ms` ou no `animationend` (failsafe) | `index.html:1116` |
| `animate` | `(dur, fn)` | chama `fn(progress)` com easeOutCubic; `fn(1)` direto se `document.hidden` | `index.html:1122` |
| `countUp` | `(node, to, dec)` | anima `textContent` numérico; valor final direto se oculto | `index.html:1131` |

## Parsing de CSV

| Função | Assinatura | Retorno | Lança | Fonte |
|---|---|---|---|---|
| `detectDelim` | `(head)` | `, ; \t \|` | — | `index.html:1140` |
| `parseCSV` | `(text)` | `string[][]` | — | `index.html:1149` |
| `toNum` | `(v)` | `number` ou `NaN` | — | `index.html:1166` |
| `buildDataset` | `(rows)` | `{data, metrics, matched}` | `Error` (sem cabeçalho/país/coluna numérica) | `index.html:1186` |

`COLDEFS` (`index.html:1179`) é a tabela de reconhecimento de colunas. Ver
[Schema do CSV](csv-schema.md).

## Projeção e TopoJSON

| Função | Assinatura | Retorno | Fonte |
|---|---|---|---|
| `decodeArcs` | `(topo)` | arcos absolutos `[[x,y],...]` | `index.html:1236` |
| `ringFrom` | `(idx, arcs)` | anel de pontos (índice `<0` = arco invertido `~i`) | `index.html:1243` |
| `topoFeatures` | `(topo)` | `[{id, polys}]` | `index.html:1251` |
| `neRaw` | `(lam, phi)` | `[x, y]` Natural Earth I (radianos) | `index.html:1260` |
| `projectRaw` | `(lon, lat)` | `[x, -y]` (graus → plano SVG) | `index.html:1268` |

## Estado e filtragem

| Função | Assinatura | Retorno | Fonte |
|---|---|---|---|
| `activeMetric` | `()` | métrica em foco (ou a primeira) | `index.html:1282` |
| `valOf` | `(d, key)` | valor da métrica no registro | `index.html:1283` |
| `filtered` | `()` | `data[]` após continentes+busca+faixa | `index.html:1285` |
| `seriesOf` | `(rows, key)` | valores finitos de uma métrica | `index.html:1295` |
| `showTip`/`hideTip`/`tipCountry` | tooltip | — | `index.html:1299-1316` |

## IO e ingestão

| Função | Assinatura | Efeitos | Fonte |
|---|---|---|---|
| `showErr` | `(msg)` | mostra erro no intake (retriga animação) | `index.html:1321` |
| `ingest` | `(text, fileName, size)` | popula `ST`, alterna telas, chama `buildControls`/`buildMapOnce`/`renderAll(true)` | `index.html:1323` |
| `readFile` | `(f)` | `FileReader` → `ingest` | `index.html:1353` |

## Renderers

Todos leem `filtered()`/`activeMetric()` e desenham em SVG; nenhum recebe dados por parâmetro
(exceto `renderKPIs`, que recebe `rows` e `first`).

| Função | Painel | Fonte |
|---|---|---|
| `renderKPIs(rows, first)` | 7 cards de KPI | `index.html:1492` |
| `renderMap()` | mapa coroplético | `index.html:1602` |
| `renderCorr()` | matriz de correlação | `index.html:1737` |
| `renderScatter()` | dispersão + regressão | `index.html:1807` |
| `renderRank()` | ranking | `index.html:1878` |
| `renderCont()` | composição por continente | `index.html:1915` |
| `renderHist()` | histograma | `index.html:1978` |
| `renderRCont()` | r por continente | `index.html:2036` |
| `renderTable()` | tabela analítica | `index.html:2069` |

Suporte do mapa: `buildMapOnce`, `fitMap`, `applyZoom`, `scaleFn`, `pathOf`, `unwrapRing`,
`subpath`, `bindGeo`, `renderLegend` (`index.html:1527-1704`).

## Ciclo de render

| Função | Assinatura | Papel | Fonte |
|---|---|---|---|
| `renderAll` | `(first?)` | agendador (coalesce via rAF; desvio se `document.hidden`) | `index.html:2125` |
| `paint` | `(first?)` | corpo síncrono: chama os 9 renderers + `refreshAIScope` | `index.html:2137` |

> [!TIP]
> Toda mutação de `ST` deve terminar chamando `renderAll()`. Ver
> [ADR-0002](../arquitetura/decisoes/ADR-0002-render-scheduler.md).

## Referências cruzadas

- [Módulos](../arquitetura/modulos.md)
- [Estruturas de dados](estruturas-de-dados.md)
- [Fluxo de dados](../arquitetura/fluxo-de-dados.md)
- [Componentes](../ui/componentes.md)
</content>

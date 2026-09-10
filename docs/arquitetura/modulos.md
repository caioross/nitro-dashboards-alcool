---
title: Arquitetura — Inventário de módulos
resumo: Cada bloco de JavaScript do index.html, sua responsabilidade, entradas e saídas.
atualizado_em: 2026-09-10
responsavel: docs-site-nitro
tags: [arquitetura, modulos, javascript, inventario]
---

# Arquitetura — Inventário de módulos

O `index.html` é um único `<script>` (`index.html:987-2776`) dividido em blocos por banners
de comentário. Este é o inventário de cada bloco.

## Sumário
- [Como localizar um bloco](#como-localizar-um-bloco)
- [Blocos](#blocos)
- [Grafo de dependências](#grafo-de-dependências)
- [Referências cruzadas](#referências-cruzadas)

## Como localizar um bloco

```bash
grep -n "^/\* =\|^<!-- =" Dashboards/index.html
```

## Blocos

### UTIL — helpers (`index.html:1003-1137`)
- **DOM**: `$`, `$$`, `el` (cria nós SVG), `clear`.
- **Formatação**: `NF/NF1/NF2` (`Intl.NumberFormat('pt-BR')`), `fmt`, `fmtR`, `clamp`, `lerp`.
- **Estatística `S`**: `sum`, `mean`, `median`, `quantile`, `min`, `max`, `sd` (amostral n−1),
  `pearson`, `linreg`, `pValue` (z de Fisher). Funções auxiliares `erf`, `normCdf`, `fmtP`.
- **Cores**: `CONT_COLOR`, `CONT_ORDER`, `RAMP` (coroplético), diverging (`divColor`), `rampColor`.
- **Animações**: `settle` (failsafe de entrada), `animate` (easeOutCubic com desvio por
  `document.hidden`), `countUp`.

### CSV PARSING (`index.html:1139-1233`)
`detectDelim`, `parseCSV`, `toNum`, `COLDEFS`, `buildDataset`. Entrada: texto do arquivo.
Saída: `{data, metrics, matched}`. Ver [Fluxo de dados](fluxo-de-dados.md).

### TOPOJSON + PROJEÇÃO (`index.html:1235-1268`)
- `decodeArcs`: desfaz o delta-encoding e aplica `scale`/`translate` do TopoJSON.
- `ringFrom`: reconstrói um anel a partir de índices de arco (índice negativo = arco invertido, `~i`).
- `topoFeatures`: expande `objects.countries.geometries` em features com `polys`.
- `neRaw` / `projectRaw`: projeção **Natural Earth I** (mesma formulação do D3), com y negado.

### ESTADO (`index.html:1270-1316`)
`ST` (objeto global), `activeMetric`, `valOf`, `filtered`, `seriesOf` e o tooltip
(`tip`, `showTip`, `hideTip`, `tipCountry`). Ver [Estruturas de dados](../referencia/estruturas-de-dados.md).

### INTAKE / IO (`index.html:1318-1398`)
`ingest`, `readFile`, listeners de arquivo/drag-and-drop, botão de amostra e exportação de CSV
da seleção. Efeito colateral: alterna `#intake`/`#dash`, revela `#btnAI` e `#btnExport`.

### CONTROLES (`index.html:1400-1481`)
`buildControls` (segmento de métricas, chips de continente, selects de eixo), `resetRange`,
`paintRange`, `onRange`, busca com debounce de 140 ms, reset e troca de escala do mapa.

### KPIs (`index.html:1482-1524`)
`KPI_DEFS` (7 cards: Países, Soma, Média, Mediana, Máximo, Mínimo, Desvio padrão) e `renderKPIs`,
que usa `countUp` para animar os valores e resolve o rótulo de "quem" no Máx/Mín.

### MAPA (`index.html:1526-1734`)
`buildMapOnce` (uma vez), `unwrapRing`, `subpath`, `pathOf`, `fitMap`, `applyZoom`, `scaleFn`
(quantil/linear/sqrt), `renderMap`, `bindGeo`, `renderLegend` e o IIFE de zoom/pan
(`mapInteractions`). Ver [Componentes](../ui/componentes.md#mapa-coroplético).

### MATRIZ DE CORRELAÇÃO (`index.html:1736-1804`)
`renderCorr`: heatmap n×n de Pearson (até 6 métricas), clique numa célula seleciona o par X/Y
da dispersão. Escala de cor diverging.

### DISPERSÃO (`index.html:1806-1875`)
`renderScatter`: pontos por país, reta de regressão animada, caixa com r, r², p-valor e a
equação. Classifica a força da correlação no subtítulo.

### RANKING (`index.html:1877-1912`)
`renderRank`: top/base 14 países na métrica ativa, barras animadas coloridas por continente.

### COMPOSIÇÃO POR CONTINENTE (`index.html:1914-1975`)
`renderCont`: barras 100% empilhadas (cerveja/destilados/vinho) reveladas por máscara de clip.

### HISTOGRAMA (`index.html:1977-2033`)
`renderHist`: bins = √n (clampado 6–18), faixa ±1σ, linhas de média (μ) e mediana (Md).

### r POR CONTINENTE (`index.html:2035-2066`)
`renderRCont`: r de Pearson do par X/Y por bloco geográfico (mínimo 4 países), barra diverging.

### TABELA (`index.html:2068-2121`)
`renderTable`: base analítica ordenável por qualquer coluna, mini-barra na coluna da métrica ativa.

### RENDER (`index.html:2123-2170`)
`renderAll` (agendador), `paint` (corpo), listeners de `visibilitychange`, `resize` e teclado
(`Esc` limpa filtros, `Ctrl/⌘+O` abre arquivo).

### SUPORTE — Supabase (`index.html:2172-2235`)
IIFE do modal de suporte; envia `POST` para `support_messages` no Supabase com a publishable key.
Ver [ADR-0003](decisoes/ADR-0003-suporte-supabase.md).

### CHAVES (.env) + CLIMA (`index.html:2237-2394`)
Objeto `ENV` (`load`/`parse`/`get`/`setLocal`), `ENV_READY`, `WX` e o IIFE do widget de clima
(OpenWeatherMap com cache de 15 min). Ver [Integrações](../referencia/integracoes.md).

### CHAT COM IA — Gemini (`index.html:2396-2769`)
IIFE do chat: `snapshot` (contexto), `SYSTEM` (prompt), `md` (markdown→HTML seguro), `ask`
(fetch SSE com fallback de modelos), UI e handlers.

### Boot (`index.html:2771-2775`)
Injeta os logos base64 nos `<img>`.

## Grafo de dependências

```mermaid
flowchart TB
  UTIL --> CSV
  UTIL --> RENDERERS
  CSV --> ESTADO
  TOPO[TOPOJSON+PROJEÇÃO] --> MAPA
  ESTADO --> RENDERERS[KPIs/MAPA/CORR/SCATTER/RANK/CONT/HIST/RCONT/TABELA]
  ESTADO --> CHAT
  IO --> ESTADO
  ENV --> CLIMA
  ENV --> CHAT
  CLIMA -.WX.last.-> CHAT
```

## Referências cruzadas

- [Visão geral](visao-geral.md)
- [Fluxo de dados](fluxo-de-dados.md)
- [Funções internas](../referencia/funcoes.md)
- [Componentes](../ui/componentes.md)
</content>

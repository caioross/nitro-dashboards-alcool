---
title: Referência — Estruturas de dados
resumo: Shape do dataset, do estado global ST, das métricas e dos metadados embutidos, com invariantes.
atualizado_em: 2026-09-10
responsavel: docs-site-nitro
tags: [referencia, dados, estado, tipos, invariantes]
---

# Referência — Estruturas de dados

## Sumário
- [Registro de país (data[])](#registro-de-país-data)
- [Métrica (metrics[])](#métrica-metrics)
- [Estado global ST](#estado-global-st)
- [Metadados embutidos (CMETA)](#metadados-embutidos-cmeta)
- [WORLD (TopoJSON)](#world-topojson)
- [Invariantes](#invariantes)
- [Referências cruzadas](#referências-cruzadas)

## Registro de país (data[])

Cada linha válida do CSV vira um registro (`index.html:1220-1228`):

```js
{
  country: 'Albania',        // string, nome como veio no CSV (trim)
  continent: 'Europa',       // de CMETA; 'Não classificado' se não casar
  iso3: 'ALB',               // de CMETA; null se não casar
  id: 8,                     // id ISO-numérico (chave do TopoJSON); null se não casar
  pt: null,                  // centroide [lon,lat] p/ microestados sem geometria; senão null
  v: {                       // valores por métrica, indexados por metric.key
    beer: 89, spirit: 132, wine: 54, total: 4.9
  }
}
```

| Campo | Tipo | Origem | Nota |
|---|---|---|---|
| `country` | `string` | coluna de país do CSV | chave de deduplicação |
| `continent` | `string` | `CMETA[name].c` | fallback `'Não classificado'` |
| `iso3` | `string \| null` | `CMETA[name].i` | usado na busca textual |
| `id` | `number \| null` | `CMETA[name].n` | casa com `g.id` do TopoJSON |
| `pt` | `[lon,lat] \| null` | `CMETA[name].p` | microestados desenhados como pontos |
| `v` | `Record<string,number>` | colunas numéricas | pode conter `NaN` |

## Métrica (metrics[])

Produzida por `buildDataset` a partir de `COLDEFS` + colunas genéricas (`index.html:1199-1211`):

```js
{ key: 'beer', col: 1, header: 'beer_servings',
  label: 'Cerveja', short: 'Cerveja', unit: 'doses/pessoa/ano' }
```

| Campo | Tipo | Nota |
|---|---|---|
| `key` | `string` | `beer`/`spirit`/`wine`/`total` ou `x<i>` para genéricas |
| `col` | `number` | índice da coluna no CSV |
| `header` | `string` | nome original da coluna |
| `label` / `short` | `string` | rótulos exibidos |
| `unit` | `string` | unidade; `''` para métricas genéricas |

> [!NOTE]
> O painel não pode assumir as 4 colunas do `drinks.csv`. Qualquer coluna numérica vira métrica.
> Ver [Schema do CSV](csv-schema.md).

## Estado global ST

Objeto único de estado (`index.html:1271-1280`):

```js
const ST = {
  data: [], metrics: [], metric: null,      // dataset + métrica em foco
  conts: new Set(), q: '',                   // filtros: continentes, busca
  lo: 0, hi: 1, loRaw: 0, hiRaw: 1,          // faixa min/max (valor e limites brutos)
  scale: 'quantile', rankTop: true,          // escala do mapa; topo/base do ranking
  px: 'beer', py: 'total',                   // eixos X/Y da dispersão
  sortKey: null, sortDir: -1,                // ordenação da tabela
  feats: null, geoIndex: null,               // geometria do mapa (cache)
  zoom: { k: 1, x: 0, y: 0 }, fitK: 1, fitX: 0, fitY: 0,  // transformações do mapa
  file: null                                 // {name, size, n, matched}
};
```

| Grupo | Campos | Quem escreve |
|---|---|---|
| Dataset | `data`, `metrics`, `metric` | `ingest` (`index.html:1328-1330`) |
| Filtros | `conts`, `q`, `lo/hi`, `loRaw/hiRaw` | `buildControls`, `onRange`, busca, reset |
| Visual | `scale`, `rankTop`, `px/py`, `sortKey/sortDir` | controles e cliques nos painéis |
| Mapa | `feats`, `bounds`, `fitK/fitX/fitY`, `zoom` | `buildMapOnce`, `fitMap`, zoom/pan |
| Meta | `file` | `ingest` |

## Metadados embutidos (CMETA)

Mapa de nome de país → metadados (`index.html:993`). Formato por entrada:

```js
CMETA['Albania'] = { c: 'Europa', i: 'ALB', n: 8, p: null };
// c=continente, i=ISO3, n=ISO-numérico (id TopoJSON), p=centroide [lon,lat] ou ausente
```

Casamento tolerante em `buildDataset`: tenta `CMETA[name]` e depois
`CMETA[name.replace(/^the\s+/i,'')]` (`index.html:1219`).

## WORLD (TopoJSON)

Atlas Natural Earth 110m embutido (`index.html:992`), consumido por `topoFeatures`
(`index.html:1251`). Estrutura relevante:

- `transform`: `{scale:[sx,sy], translate:[tx,ty]}` para desfazer o delta-encoding.
- `arcs`: arcos quantizados e delta-encodados.
- `objects.countries.geometries`: cada um com `id` (ISO-numérico), `type` e `arcs`.

## Invariantes

- **`v[key]` pode ser `NaN`** — todo consumo passa por `isFinite`/`seriesOf`.
- **Valores geométricos animados são clampados** com `Math.max(0, …)`: o SVG lança exceção em
  `r`/`width`/`height` negativos (ex.: `index.html:1854`, `1905`, `2015`).
- **Nomes de país são únicos** em `data` (dedupe por `seen`, `index.html:1214`).
- **`ST.metric`, `ST.px`, `ST.py` sempre apontam para uma métrica existente** — definidos em
  `ingest` com fallback (`index.html:1330-1332`).
- **Toda mutação de `ST` deve terminar em `renderAll()`**.

## Referências cruzadas

- [Schema do CSV](csv-schema.md)
- [Funções internas](funcoes.md)
- [Fluxo de dados](../arquitetura/fluxo-de-dados.md)
</content>

---
title: Guia — Desenvolvimento
resumo: Convenções de código, como validar o JS, e receitas para adicionar KPI, gráfico ou métrica.
atualizado_em: 2026-09-10
responsavel: docs-site-nitro
tags: [guia, desenvolvimento, convencoes, receitas]
---

# Guia — Desenvolvimento

## Sumário
- [Editando o arquivo único](#editando-o-arquivo-único)
- [Validando o JavaScript](#validando-o-javascript)
- [Convenções de código](#convenções-de-código)
- [Receita: adicionar um KPI](#receita-adicionar-um-kpi)
- [Receita: adicionar um gráfico](#receita-adicionar-um-gráfico)
- [Receita: mexer no parser](#receita-mexer-no-parser)
- [Armadilhas](#armadilhas)
- [Commits](#commits)
- [Referências cruzadas](#referências-cruzadas)

## Editando o arquivo único

`index.html` é editado no lugar. Localize a seção pelo banner antes de mexer:

```bash
grep -n "^/\* =\|^<!-- =" Dashboards/index.html
```

> [!WARNING]
> Não abrir/reformatar as linhas gigantes de dado embutido `NITRO_LOGO_W/D`, `NITRO_MARK`,
> `WORLD`, `CMETA` (`index.html:989-993`). Um editor que faça wrap pode corromper o arquivo.

## Validando o JavaScript

`node --check` não aceita HTML. Extraia o `<script>` antes:

```bash
sed -n '/^<script>$/,/^<\/script>$/p' Dashboards/index.html | sed '1d;$d' > "$TMPDIR/_check.js" \
  && node --check "$TMPDIR/_check.js"
```

A validação real, porém, é **importar um CSV e conferir os KPIs** no navegador — não apenas
checar sintaxe.

## Convenções de código

| Convenção | Regra | Exemplo |
|---|---|---|
| Idioma | UI e mensagens em pt-BR | `showErr('Não foi possível ler...')` |
| Números | sempre via `fmt`/`NF*` (`Intl.NumberFormat('pt-BR')`) | `fmt(v, 1)` |
| SVG | criado por `el(tag, attrs, parent)` | `el('rect', {x, y, width}, svg)` |
| Estado | mutar `ST` e terminar com `renderAll()` | ver [ADR-0002](../arquitetura/decisoes/ADR-0002-render-scheduler.md) |
| Métricas | nunca assumir 4 colunas fixas — iterar `ST.metrics` | `ST.metrics.map(...)` |
| Geometria animada | clampar com `Math.max(0, …)` | `r: Math.max(0, 4.4 * p)` |
| Sem dependências | proibido `<script src>`/`<link>` de libs | ver [ADR-0001](../arquitetura/decisoes/ADR-0001-arquivo-unico.md) |

## Receita: adicionar um KPI

1. Adicione uma entrada em `KPI_DEFS` (`index.html:1483-1491`):

```js
{ k: 'Amplitude', f: v => S.max(v) - S.min(v), d: 2 }
```

2. `renderKPIs` (`index.html:1492`) já itera `KPI_DEFS` e cria/atualiza os cards. Ajuste o
   `grid-template-columns:repeat(7,1fr)` do `.kpis` (`index.html:258`) e os breakpoints
   (`index.html:514`, `519`) se mudar a contagem.

## Receita: adicionar um gráfico

1. Adicione o markup do painel dentro de `.grid` (`index.html:765-874`), com `<svg id="meuSvg">`.
2. Escreva `renderMeu()` no padrão dos demais renderers: leia `filtered()`/`activeMetric()`,
   `clear(svg)`, defina `viewBox`, desenhe com `el(...)`.
3. Chame `renderMeu()` dentro de `paint()` (`index.html:2137-2154`).
4. Se depende do par X/Y, chame também em `s.onchange` (`index.html:1436`) e na seleção da
   matriz (`index.html:1779-1782`).

## Receita: mexer no parser

Ao tocar em `parseCSV`/`toNum`/`buildDataset`, teste com:

- um CSV separado por `;`;
- cabeçalhos em português;
- vírgula decimal (`4,9`);
- uma coluna numérica extra (deve virar métrica genérica).

Ver [Schema do CSV](../referencia/csv-schema.md).

## Armadilhas

> [!WARNING]
> - Nada de `background-attachment: fixed` nem `backdrop-filter` pesado — causavam conteúdo em
>   branco ao rolar (`CLAUDE.md`). A ambiência é `body::before` fixa em `z-index:0` (`index.html:52-59`).
> - Não recolocar a lógica de render dentro do `requestAnimationFrame` sem o desvio por
>   `document.hidden` — já deixou o painel em branco para sempre.
> - Ao contar países no mapa, use o contador `drawn` (`index.html:1640-1643`), não `byId.size`.

## Commits

> [!NOTE]
> Toda mensagem de commit e título/descrição de PR deste repositório seguem o padrão
> `commit-fofinho` (diminutivo, tom fofinho apocalíptico, muitos emojis). Antes de `git commit`
> ou `gh pr create`, invoque a skill `commit-fofinho`. Ver `CLAUDE.md` → "Padrão de commit".

## Referências cruzadas

- [Módulos](../arquitetura/modulos.md)
- [Funções internas](../referencia/funcoes.md)
- [Componentes](../ui/componentes.md)
- [Design system](../ui/design-system.md)
</content>

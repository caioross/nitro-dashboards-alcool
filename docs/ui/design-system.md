---
title: UI — Design system
resumo: Tokens de cor, tipografia, raios, sombras, escalas de cor de dados e breakpoints responsivos.
atualizado_em: 2026-09-10
responsavel: docs-site-nitro
tags: [ui, design-system, tokens, cores, tipografia, responsivo]
---

# UI — Design system

Todos os tokens vivem em `:root` (`index.html:18-42`). A marca vem do brand book da Nitro.

## Sumário
- [Paleta de marca](#paleta-de-marca)
- [Tons de interface](#tons-de-interface)
- [Escalas de cor de dados](#escalas-de-cor-de-dados)
- [Cores de continente](#cores-de-continente)
- [Tipografia](#tipografia)
- [Raios, sombras e easing](#raios-sombras-e-easing)
- [Layout e breakpoints](#layout-e-breakpoints)
- [Ambiência de fundo](#ambiência-de-fundo)
- [Referências cruzadas](#referências-cruzadas)

## Paleta de marca

| Token | Valor | Nome |
|---|---|---|
| `--admiral` | `#003663` | Admiral Blue |
| `--white` | `#FFFFFF` | Pure White |
| `--chartreuse` | `#94C356` | Chartreuse Green |
| `--citron` | `#B9DA00` | Citron Yellow |

## Tons de interface

| Token | Valor | Uso |
|---|---|---|
| `--navy-950 … --navy-700` | `#01111d` → `#0d3a59` | fundos e superfícies |
| `--ink` | `#EAF3FA` | texto primário |
| `--ink-2` | `#9FBBD2` | texto secundário |
| `--ink-3` | `#6B8CA6` | texto terciário / eixos |
| `--line` / `--line-2` | rgba branco/chartreuse | bordas |
| `--glow` | `rgba(148,195,86,.30)` | brilho de foco |

## Escalas de cor de dados

Definidas no bloco de cores do JS (`index.html:1088-1111`):

| Escala | Definição | Uso |
|---|---|---|
| `RAMP` (sequencial) | `#0a2f4d → #12557a → #1d7f7e → #4da268 → #94C356 → #B9DA00` | mapa, histograma (`rampColor`) |
| Diverging | `#2F86C9` (neg) · `#12354f` (mid) · `#B9DA00` (pos) | matriz e r por continente (`divColor`) |

## Cores de continente

`CONT_COLOR` (`index.html:1089-1093`), na ordem `CONT_ORDER` (`index.html:1094`):

| Continente | Cor |
|---|---|
| África | `#B9DA00` |
| Ásia | `#94C356` |
| Europa | `#3D8FD1` |
| América do Norte | `#E0B84A` |
| América do Sul | `#35D3A3` |
| Oceania | `#6FE3E8` |
| Não classificado | `#7C93A6` |

## Tipografia

| Token | Valor |
|---|---|
| `--font` | `'Poppins','Segoe UI',system-ui,-apple-system,sans-serif` |
| `--mono` | `'SFMono-Regular',Consolas,'Roboto Mono',monospace` |

- Rótulos (`.eyebrow`, `index.html:72-75`): 10px, peso 600, `letter-spacing:.22em`, caixa alta
  ("Wide-Set Tech Typography").
- Números (`.num`, `index.html:76`): `font-variant-numeric:tabular-nums`.
- Poppins vem do Google Fonts (`index.html:10`), com fallback de sistema.

## Raios, sombras e easing

| Token | Valor |
|---|---|
| `--r-lg` / `--r-md` / `--r-sm` | `16px` / `12px` / `8px` |
| `--shadow` | `0 18px 44px -22px rgba(0,0,0,.85)` |
| `--ease` | `cubic-bezier(.22,.61,.36,1)` |
| `--ease-out` | `cubic-bezier(.16,1,.3,1)` |

## Layout e breakpoints

- KPIs: grid de 7 colunas (`index.html:258`).
- Painéis: grid de 12 colunas (`index.html:277`); cada painel ocupa spans (`.c-map`, `.c-corr`, …).

| Largura | Reorganização | Fonte |
|---|---|---|
| ≤ 1560 px | `.c-cont`=7, `.c-hist`=5, `.c-rcont`=12; KPI menor | `index.html:509-512` |
| ≤ 1250 px | KPIs → 4 col; mapa=12, corr=5, scatter=7, rank=5; oculta `.wx-side` | `index.html:513-517`, `550` |
| ≤ 1050 px | KPIs → 2 col; todos os painéis span 12; rail sticky | `index.html:518-525` |
| ≤ 900 px | oculta o widget de clima | `index.html:551` |
| ≤ 640 px | oculta rótulo do FAB; ajusta chat | `index.html:455`, `568` |

## Ambiência de fundo

> [!WARNING]
> A ambiência é uma camada `body::before` fixa em `z-index:0` (`index.html:52-59`); `#intake`
> e `#dash` ficam em `z-index:1`. Não usar `background-attachment: fixed` nem `backdrop-filter`
> pesado — causavam conteúdo em branco ao rolar.

O bloco `@media (prefers-reduced-motion: reduce)` (`index.html:504-507`) neutraliza durações e
força o estado final visível.

## Referências cruzadas

- [Componentes](componentes.md)
- [Visão geral](../arquitetura/visao-geral.md)
- [Desenvolvimento](../guias/desenvolvimento.md)
</content>

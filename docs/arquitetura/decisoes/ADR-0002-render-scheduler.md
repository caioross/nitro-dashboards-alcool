---
title: ADR-0002 — Agendador de render com desvio para aba oculta
resumo: Por que renderAll usa requestAnimationFrame mas chama paint direto quando document.hidden.
atualizado_em: 2026-09-10
responsavel: docs-site-nitro
tags: [adr, render, requestAnimationFrame, animacao]
---

# ADR-0002 — Agendador de render com desvio para aba oculta

- **Status**: Aceito
- **Data**: registro documental em 2026-09-10.

## Contexto

Todo repintar do painel passa por `renderAll` → `paint` (`index.html:2125-2154`). Coalescer
múltiplas mutações de estado num único frame evita repintar 9 painéis várias vezes por
interação. O caminho natural para isso é `requestAnimationFrame` (rAF).

Porém, o navegador **suspende o rAF em abas ocultas** (`document.hidden`). Além disso, as
animações de entrada usam `.enter{opacity:0}` (`index.html:506` e CSS relacionado): se o
relógio de animação congela, o elemento fica invisível para sempre.

## Decisão

1. `renderAll(first)` coalesce chamadas via rAF, mas **desvia para `paint` direto quando
   `document.hidden`** (`index.html:2126-2135`). Isso evita a flag `rafPending` presa em `true`,
   que já causou o painel ficar em branco permanentemente.
2. Failsafes de animação:
   - `settle(node, delay)` força a classe `.done` após `delay+900ms` mesmo sem `animationend`
     (`index.html:1116-1120`).
   - A regra CSS `.enter.done{...!important}` garante o estado final visível.
   - `animate()` e `countUp()` fazem curto-circuito com `fn(1)` / valor final quando
     `document.hidden` (`index.html:1123`, `index.html:1135`).
   - Bloco `@media (prefers-reduced-motion: reduce)` neutraliza durações (`index.html:504-507`).
3. Re-render no `visibilitychange` ao voltar para a aba (`index.html:2156-2158`).

## Consequências

**Positivas**
- Nunca deixa o painel invisível, mesmo com aba em segundo plano ou motion reduzido.
- Coalescência mantém o custo de render baixo por interação.

**Negativas**
- Regra frágil: qualquer refatoração que volte a lógica de render para dentro do rAF sem o
  desvio por `document.hidden` reintroduz o bug do painel em branco.

> [!WARNING]
> Não recolocar a lógica de `paint` dentro do `requestAnimationFrame` sem preservar o desvio
> por `document.hidden`. Ver `CLAUDE.md` → "Arquitetura do runtime".

## Referências

- [Fluxo de dados](../fluxo-de-dados.md#etapa-5--ciclo-de-render)
- [Funções internas](../../referencia/funcoes.md)
</content>

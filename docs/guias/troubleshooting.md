---
title: Guia — Troubleshooting
resumo: Sintoma → causa → correção para os problemas conhecidos do painel.
atualizado_em: 2026-09-10
responsavel: docs-site-nitro
tags: [guia, troubleshooting, suporte, erros]
---

# Guia — Troubleshooting

Tabela de diagnóstico. Muitos "problemas" são comportamentos conhecidos e esperados.

## Sumário
- [Importação e dados](#importação-e-dados)
- [file:// e CORS](#file-e-cors)
- [Chat com IA](#chat-com-ia)
- [Clima](#clima)
- [Suporte](#suporte)
- [Render e animação](#render-e-animação)
- [Mapa](#mapa)
- [Referências cruzadas](#referências-cruzadas)

## Importação e dados

| Sintoma | Causa | Correção |
|---|---|---|
| "Nenhuma coluna de país encontrada" | cabeçalho não casa a regex nem há coluna 100% texto | renomeie a coluna para `country`/`país` ou garanta texto puro |
| "Nenhuma coluna numérica encontrada" | nenhuma coluna passou no reconhecimento nem no limiar de 60% | verifique decimais/separador; ver [Schema do CSV](../referencia/csv-schema.md) |
| Valores errados (milhar vira decimal) | ambiguidade pt-BR/en-US | confira o padrão em `toNum` (`index.html:1166`) |
| País sem cor no mapa | nome não casou `CMETA` → sem `id` | o país entra na tabela/ranking, mas não no mapa |

## file:// e CORS

| Sintoma | Causa | Correção |
|---|---|---|
| Botão "Carregar ../Dados/drinks.csv" falha | `fetch` bloqueado por `file://` (CORS) | arraste o arquivo ou sirva por HTTP (`index.html:1371`) |
| `.env` não é lido / chat pede a chave | `fetch` do `.env` bloqueado por `file://` | sirva a raiz por HTTP; ou informe a chave na UI (`index.html:2269`) |

> [!NOTE]
> Nenhum dos dois é bug. Servir por HTTP resolve ambos. Ver
> [Primeiros passos](primeiros-passos.md#servir-por-http-recomendado).

## Chat com IA

| Sintoma | Causa | Correção |
|---|---|---|
| "Nenhuma chave do Gemini disponível" | `.env` não lido e sem chave em `localStorage` | informe a chave em `#aiKeyAsk` ou sirva por HTTP |
| "A chave do Gemini foi rejeitada" | 401/403 na API | chave inválida/sem permissão; gere outra |
| "Todos os modelos falharam" | 429/5xx/404 em toda a cadeia | quota estourada ou modelos indisponíveis; verifique `MODELS` (`index.html:2404`) |
| Resposta vazia e fallback percorre tudo | `maxOutputTokens` apertado (modelo gasta no raciocínio) | mantenha 8192 (`index.html:2622`) |
| Resposta chega mas não aparece | parser de SSE não normalizou CRLF | ver `index.html:2667-2672` — não regredir |

## Clima

| Sintoma | Causa | Correção |
|---|---|---|
| Widget não aparece | sem `OPENWEATHER_API_KEY` | preencha o `.env` e sirva por HTTP (`index.html:2376`) |
| "Chave do clima ausente" | idem | idem |
| "Clima indisponível" / pede cidade | geolocalização negada ou sem HTTPS | clique no widget e digite a cidade (`index.html:2337`) |
| Widget some | largura < 900 px | comportamento responsivo (`index.html:551`) |

## Suporte

| Sintoma | Causa | Correção |
|---|---|---|
| "Não consegui registrar o chamado agora" | falha de rede ou RLS bloqueando | confira conectividade e a policy de `support_messages` |
| Nada é enviado (esperado?) | **desatualizado**: hoje envia ao Supabase | ver [ADR-0003](../arquitetura/decisoes/ADR-0003-suporte-supabase.md) |

## Render e animação

| Sintoma | Causa | Correção |
|---|---|---|
| Painel fica em branco para sempre | flag `rafPending` presa (lógica no rAF sem desvio) | garantir desvio por `document.hidden` (`index.html:2126`) |
| Elementos invisíveis (opacity 0) | animação de entrada congelada em aba oculta | failsafes `settle`/`.enter.done`/`prefers-reduced-motion` (`index.html:1116`) |
| Conteúdo em branco ao rolar | `background-attachment: fixed`/`backdrop-filter` pesado | não usar; ambiência é `body::before` (`index.html:52`) |

## Mapa

| Sintoma | Causa | Correção |
|---|---|---|
| Roda do mouse não dá zoom | por design: só `Ctrl/⌘ + roda` amplia | roda pura rola a página (`index.html:1711`) |
| País vira faixa atravessando o mapa | anel cruzando o antimeridiano sem unwrap | `unwrapRing`/`subpath` tratam isso (`index.html:1542`) |
| Exceção de SVG (`r`/`width` negativo) | valor geométrico animado não clampado | usar `Math.max(0, …)` |

## Referências cruzadas

- [Primeiros passos](primeiros-passos.md)
- [Integrações](../referencia/integracoes.md)
- [Runbook](../operacao/runbook.md)
- [ADR-0002 — Render scheduler](../arquitetura/decisoes/ADR-0002-render-scheduler.md)
</content>

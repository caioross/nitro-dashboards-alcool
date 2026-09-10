---
title: Operação — Segurança
resumo: Tratamento de chaves, superfícies de risco e recomendações de hardening do painel.
atualizado_em: 2026-09-10
responsavel: docs-site-nitro
tags: [operacao, seguranca, chaves, risco]
---

# Operação — Segurança

> [!NOTE]
> O painel é, por premissa, **interno**. Várias decisões aceitam expor chaves ao cliente porque
> o público é a equipe de engenharia. Para uso público, aplique o hardening desta página.

## Sumário
- [Modelo de ameaça](#modelo-de-ameaça)
- [Superfícies de risco](#superfícies-de-risco)
- [Tratamento de chaves](#tratamento-de-chaves)
- [Recomendações de hardening](#recomendações-de-hardening)
- [Checklist de segurança](#checklist-de-segurança)
- [Referências cruzadas](#referências-cruzadas)

## Modelo de ameaça

- **Dados**: o CSV é processado 100% no navegador; nada é enviado a servidores (exceto o resumo
  estatístico que o usuário decide mandar ao Gemini no chat, e o formulário de suporte).
- **Segredos**: as chaves de API chegam ao cliente. Um usuário do painel pode lê-las no fonte.

## Superfícies de risco

| Superfície | Risco | Mitigação atual |
|---|---|---|
| `GEMINI_API_KEY` no `.env` servido | leitura no cliente | painel interno; proxy para uso público |
| `OPENWEATHER_API_KEY` no `.env` | leitura no cliente | idem |
| `SUPA_KEY` hardcoded (`index.html:2176`) | leitura no cliente | RLS insert-only na tabela |
| Formulário de suporte | spam/abuso | sem rate limit no cliente; considerar no Supabase |
| Chat → Gemini | envio do recorte de dados a terceiro | é o resumo de `filtered()`, decidido pelo usuário |
| Injeção via markdown do chat | XSS | `md()` escapa HTML antes de renderizar (`index.html:2523`) |

## Tratamento de chaves

- O `.env` fica fora do versionamento (`.gitignore:29`) e é lido por `fetch` em runtime
  (`index.html:2258-2272`) — logo, **exposto ao navegador**.
- Fallback: `localStorage` (`nitro.GEMINI_API_KEY`) preenchido pela UI do chat.
- A publishable key do Supabase é intencionalmente pública; sua segurança depende **inteiramente**
  da policy de RLS estar correta.

> [!WARNING]
> Nunca faça commit do `.env`. Nunca cole valores de chave em documentação, issues ou logs.
> Esta documentação registra apenas os **nomes** das variáveis.

## Recomendações de hardening

Para expor o painel fora da rede interna:

1. **Proxy para LLM/clima**: mover `GEMINI_API_KEY` e `OPENWEATHER_API_KEY` para um backend que
   assine as chamadas; o cliente fala só com o proxy.
2. **RLS do Supabase**: confirmar `support_messages` como INSERT-only para a role anônima; sem
   SELECT/UPDATE/DELETE. Considerar rate limiting/captcha.
3. **HTTPS**: obrigatório (geolocalização exige contexto seguro).
4. **CSP**: opcionalmente restringir `connect-src`/`img-src`/`style-src`.

## Checklist de segurança

- [ ] `.env` fora do host público (ou chaves atrás de proxy).
- [ ] RLS de `support_messages` validada insert-only.
- [ ] HTTPS ativo.
- [ ] Revisar se `SUPA_URL`/`SUPA_KEY` apontam para o projeto correto.
- [ ] Confirmar que `md()` continua escapando HTML após qualquer edição no chat.

## Referências cruzadas

- [Deploy](../guias/deploy.md)
- [Integrações](../referencia/integracoes.md)
- [Configuração](../referencia/configuracao.md)
- [ADR-0003 — Suporte no Supabase](../arquitetura/decisoes/ADR-0003-suporte-supabase.md)
</content>

---
title: ADR-0003 — Formulário de suporte grava no Supabase
resumo: O modal de suporte deixou de ser maquete e passou a gravar chamados no Supabase via publishable key com RLS de insert-only.
atualizado_em: 2026-09-10
responsavel: docs-site-nitro
tags: [adr, supabase, suporte, seguranca]
---

# ADR-0003 — Formulário de suporte grava no Supabase

- **Status**: Aceito
- **Data**: registro documental em 2026-09-10.

## Contexto

O `README.md` e o `CLAUDE.md` descrevem o modal de suporte como uma **maquete** que "valida e
mostra confirmação, mas não envia nada". O código atual **contradiz** essa descrição: o
formulário faz `POST` real para uma tabela no Supabase.

> [!WARNING]
> Divergência de documentação: `README.md:142` e `CLAUDE.md:147` afirmam que o suporte não
> envia nada. O código em `index.html:2199-2234` envia. Esta documentação segue o código.

## Decisão

O IIFE de suporte (`index.html:2172-2235`) envia o payload do formulário para o endpoint REST
do Supabase:

```js
// index.html:2175-2176
const SUPA_URL = 'https://<projeto>.supabase.co';
const SUPA_KEY = 'sb_publishable_...';   // publishable key (client-side)
```

```js
// index.html:2213-2222
fetch(SUPA_URL + '/rest/v1/support_messages', {
  method: 'POST',
  headers: {
    'apikey': SUPA_KEY,
    'Authorization': 'Bearer ' + SUPA_KEY,
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal'
  },
  body: JSON.stringify(payload)   // {name, email, topic, message}
});
```

- **Tabela**: `public.support_messages`.
- **Campos enviados**: `name`, `email`, `topic`, `message`. O `created_at` fica por conta do
  default do banco (`index.html:2207`).
- **Segurança da decisão**: segundo o comentário no código (`index.html:2172-2174`), a política
  de RLS da tabela permite **apenas INSERT** — a publishable key não consegue ler os chamados de
  ninguém. É por isso que se aceita expor a chave no cliente.

## Consequências

**Positivas**
- Chamados reais chegam ao banco sem backend próprio.
- Falha de rede é tratada com mensagem amigável e o botão volta a habilitar (`index.html:2227-2233`).

**Negativas / riscos**
- A publishable key vive em texto claro no HTML. A proteção depende **inteiramente** da RLS da
  tabela estar correta (insert-only). Se a RLS for afrouxada, a chave passa a ser um vazamento.
- Sem rate limiting no cliente: o endpoint pode receber spam. Considerar proteção no Supabase.

> [!TIP]
> Antes de qualquer deploy público, confirmar a policy de RLS de `support_messages` (INSERT
> apenas, sem SELECT/UPDATE/DELETE para a role anônima). Ver [Segurança](../../operacao/seguranca.md).

## Alternativas descartadas

| Alternativa | Motivo |
|---|---|
| Manter como maquete | Não registra chamados; perde a função. |
| Backend próprio / proxy | Adiciona infraestrutura; excessivo para um painel interno. |

## Referências

- [Integrações](../../referencia/integracoes.md#supabase-formulário-de-suporte)
- [Segurança](../../operacao/seguranca.md)
</content>

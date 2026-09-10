---
title: Guia — Deploy
resumo: Como publicar o painel, o que carregar junto e o hardening mínimo antes de expor.
atualizado_em: 2026-09-10
responsavel: docs-site-nitro
tags: [guia, deploy, publicacao, hardening]
---

# Guia — Deploy

## Sumário
- [O que publicar](#o-que-publicar)
- [Como publicar](#como-publicar)
- [Chaves e .env em produção](#chaves-e-env-em-produção)
- [Hardening antes de expor](#hardening-antes-de-expor)
- [Checklist de deploy](#checklist-de-deploy)
- [Referências cruzadas](#referências-cruzadas)

## O que publicar

Como o app é um arquivo único, o deploy é essencialmente servir arquivos estáticos:

| Arquivo | Publicar? | Motivo |
|---|---|---|
| `Dashboards/index.html` | Sim | o entregável |
| `Dados/drinks.csv` | Opcional | habilita o botão "Carregar amostra" via HTTP |
| `.env` | **Depende** | ver seção de chaves abaixo |
| `Referencias/`, `Jornal/`, `.claude/` | Não | material interno/de processo |

## Como publicar

Qualquer host de estáticos serve. Exemplos:

```bash
# teste local pela raiz do repo (para o .env ser alcançável)
python -m http.server 8000
# http://localhost:8000/Dashboards/index.html
```

Para produção: coloque o conteúdo atrás de um servidor/CDN estático (Nginx, S3+CloudFront,
GitHub Pages etc.). Mantenha a estrutura de pastas se quiser que `../.env` e
`../Dados/drinks.csv` continuem resolvendo.

## Chaves e .env em produção

> [!WARNING]
> As chaves do `.env` chegam ao navegador em **texto claro** — `ENV.load` faz `fetch` do
> arquivo e o expõe ao cliente (`index.html:2258-2272`). O mesmo vale para a publishable key
> do Supabase, que é hardcoded (`index.html:2176`).

Para um painel **interno**, isso é aceitável (é a premissa do projeto). Para uso **público**:

- Não publique o `.env`. Ponha as chamadas ao Gemini e ao OpenWeather **atrás de um proxy** que
  guarde as chaves no servidor.
- Confirme que a policy de RLS de `support_messages` é insert-only (ver
  [ADR-0003](../arquitetura/decisoes/ADR-0003-suporte-supabase.md)).

Ver [Segurança](../operacao/seguranca.md).

## Hardening antes de expor

| Item | Ação |
|---|---|
| Chaves de LLM/clima | mover para proxy server-side |
| Supabase RLS | validar insert-only; considerar rate limiting |
| CORS/CSP | opcionalmente restringir origens no host |
| HTTPS | obrigatório para geolocalização do clima funcionar |

## Checklist de deploy

- [ ] `index.html` servido por HTTPS.
- [ ] Se público: `.env` fora do host; chamadas de LLM/clima via proxy.
- [ ] RLS de `support_messages` confirmada insert-only.
- [ ] `Dados/drinks.csv` presente se quiser o botão de amostra.
- [ ] Smoke test: importar CSV, trocar filtros, abrir chat e clima.

## Referências cruzadas

- [Primeiros passos](primeiros-passos.md)
- [Segurança](../operacao/seguranca.md)
- [Configuração](../referencia/configuracao.md)
- [Runbook](../operacao/runbook.md)
</content>

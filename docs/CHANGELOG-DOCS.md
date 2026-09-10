---
title: Changelog da documentação
resumo: Histórico das execuções do agente docs-site-nitro.
atualizado_em: 2026-09-10
responsavel: docs-site-nitro
tags: [changelog, historico, docs]
---

# Changelog da documentação

Histórico das execuções automáticas do agente `docs-site-nitro`. Entrada mais recente no topo.

## 2026-09-10 — execução automática (bootstrap)

Primeira execução: a pasta `docs/` não existia. Skill
`anthropic-skills:code-documentation-doc-generate` invocada e aplicada.

**Arquivos criados:**
- `docs/README.md` (índice mestre)
- `docs/arquitetura/visao-geral.md`
- `docs/arquitetura/fluxo-de-dados.md`
- `docs/arquitetura/modulos.md`
- `docs/arquitetura/decisoes/ADR-0001-arquivo-unico.md`
- `docs/arquitetura/decisoes/ADR-0002-render-scheduler.md`
- `docs/arquitetura/decisoes/ADR-0003-suporte-supabase.md`
- `docs/referencia/funcoes.md`
- `docs/referencia/estruturas-de-dados.md`
- `docs/referencia/csv-schema.md`
- `docs/referencia/configuracao.md`
- `docs/referencia/integracoes.md`
- `docs/guias/primeiros-passos.md`
- `docs/guias/desenvolvimento.md`
- `docs/guias/deploy.md`
- `docs/guias/troubleshooting.md`
- `docs/ui/componentes.md`
- `docs/ui/design-system.md`
- `docs/operacao/runbook.md`
- `docs/operacao/seguranca.md`
- `docs/CHANGELOG-DOCS.md`

**Arquivos atualizados:**
- `README.md` (raiz): adicionado link para `docs/README.md`.

**Melhorias/descobertas aplicadas:**
- Toda a documentação foi construída por análise direta de `Dashboards/index.html` (~2.778 linhas),
  com referências de linha rastreáveis.
- **Divergência relevante detectada e documentada**: o modal de "Suporte" deixou de ser maquete
  e agora grava chamados no Supabase (`index.html:2172-2235`), contradizendo `README.md:142` e
  `CLAUDE.md:147`. Registrada em `ADR-0003` e sinalizada com callout em Integrações, Segurança e
  Troubleshooting.
- Mapeada a superfície de segredos: `GEMINI_API_KEY`/`OPENWEATHER_API_KEY` (via `.env`) e a
  `SUPA_KEY` hardcoded, com recomendações de hardening.
- Diagramas Mermaid para pipeline de dados, ciclo de render, fallback de modelos do Gemini e
  fluxo do clima.

**Pendências para a próxima execução:**
- Reconciliar `README.md`/`CLAUDE.md` com o comportamento real do suporte (Supabase) — hoje só a
  documentação em `docs/` reflete o código; os arquivos da raiz seguem dizendo "maquete". Como o
  agente não deve editar fora de `docs/` (exceto o link), fica a recomendação para o time.
- Confirmar com o time a policy de RLS de `support_messages` (assumida insert-only pelo comentário
  do código, `index.html:2172-2174`) — marcar como verificado quando confirmado.
- Documentar o diretório `Jornal/` (edições, `estado.json`, skills `jornal-*`) caso passe a fazer
  parte do escopo do site; hoje parece um processo editorial separado.
- Extrair exemplos reais de resposta do chat e de payload do Gemini se houver captura disponível.
</content>

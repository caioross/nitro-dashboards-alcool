---
title: Guia — Primeiros passos
resumo: Como abrir o painel, servir por HTTP, carregar dados e habilitar as integrações opcionais.
atualizado_em: 2026-09-10
responsavel: docs-site-nitro
tags: [guia, setup, primeiros-passos]
---

# Guia — Primeiros passos

## Sumário
- [Abrir por file://](#abrir-por-file)
- [Servir por HTTP](#servir-por-http-recomendado)
- [Carregar dados](#carregar-dados)
- [Habilitar as integrações](#habilitar-as-integrações-opcionais)
- [Checklist de validação](#checklist-de-validação)
- [Referências cruzadas](#referências-cruzadas)

## Abrir por file://

O modo mais simples: duplo clique em `Dashboards/index.html`. Funciona para tudo, **exceto**:

- o botão "Carregar ../Dados/drinks.csv" (usa `fetch`, bloqueado por CORS);
- a leitura automática do `.env` (também `fetch`).

Nesses casos, arraste o CSV e informe a chave do Gemini pela interface.

## Servir por HTTP (recomendado)

Serve a **raiz do repositório** para que o `.env` seja encontrado:

```bash
cd C:/Users/integral/Desktop/claude_nitro/Dashboards_alcohol
python -m http.server 8000
# abra http://localhost:8000/Dashboards/index.html
```

> [!TIP]
> Servir pela raiz (e não por `Dashboards/`) é o que permite ao `ENV.load` alcançar `.env` via
> `../.env` (`index.html:2261`). Ver [Configuração](../referencia/configuracao.md).

## Carregar dados

Três formas (todas convergem para `ingest`):

1. **Arrastar** um `.csv` para a dropzone (funciona em `file://`).
2. **Selecionar arquivo** (botão) ou atalho `Ctrl/⌘ + O`.
3. **Carregar amostra** — botão "Carregar ../Dados/drinks.csv" (só via HTTP).

O formato aceito é tolerante (separador, aspas, pt-BR/en-US). Ver
[Schema do CSV](../referencia/csv-schema.md).

## Habilitar as integrações opcionais

```bash
cp .env.example .env
# edite .env e preencha as chaves
```

```dotenv
GEMINI_API_KEY=...
OPENWEATHER_API_KEY=...
```

| Recurso | Aparece em | Depende de |
|---|---|---|
| Chat com IA | botão inferior central | `GEMINI_API_KEY` |
| Clima | barra superior | `OPENWEATHER_API_KEY` + geolocalização |

Sem servir por HTTP, informe a chave do Gemini na própria interface (ela fica só no
`localStorage`). Ver [Integrações](../referencia/integracoes.md).

## Checklist de validação

- [ ] O painel abre e mostra o intake (landing).
- [ ] Arrastar `Dados/drinks.csv` popula 7 KPIs, o mapa e todos os gráficos.
- [ ] Trocar de métrica/continente/faixa repinta na hora, sem botão "Aplicar".
- [ ] Servindo por HTTP com `.env` preenchido: o widget de clima aparece e o chat responde.

> [!NOTE]
> A verificação de verdade é importar um CSV e conferir os KPIs — não apenas olhar a tela.
> Ver `CLAUDE.md` → "Como editar".

## Referências cruzadas

- [Desenvolvimento](desenvolvimento.md)
- [Troubleshooting](troubleshooting.md)
- [Configuração](../referencia/configuracao.md)
- [Schema do CSV](../referencia/csv-schema.md)
</content>

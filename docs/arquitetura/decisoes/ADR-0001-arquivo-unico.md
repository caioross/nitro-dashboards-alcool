---
title: ADR-0001 — App de arquivo único, zero dependências
resumo: Decisão de entregar todo o dashboard em um único index.html sem build nem bibliotecas.
atualizado_em: 2026-09-10
responsavel: docs-site-nitro
tags: [adr, arquitetura, single-file]
---

# ADR-0001 — App de arquivo único, zero dependências

- **Status**: Aceito
- **Data**: registro documental em 2026-09-10 (decisão anterior ao início da documentação)
- **Contexto**: painel interno da Nitro, público técnico.

## Contexto

O entregável precisa abrir por duplo clique (`file://`), sem servidor, sem instalação e sem
build step. O público é a equipe de engenharia interna, que quer "abrir e subir a planilha".

## Decisão

Todo o produto vive em `Dashboards/index.html`: HTML, CSS e JavaScript inline. Nenhuma
biblioteca é carregada — mapa, projeção cartográfica (Natural Earth I), escalas, estatística
(Pearson, regressão, quantis, p-valor) e animações são implementados à mão. A única exceção de
rede sempre presente é a folha do Google Fonts (`index.html:10`), com fallback de fonte de
sistema.

Os únicos dados embutidos são metadados de referência (`index.html:989-993`): logos base64
(`NITRO_LOGO_W/D`, `NITRO_MARK`), o atlas mundial (`WORLD`, TopoJSON Natural Earth 110m) e
`CMETA` (ISO3/ISO-numérico/continente/centroide por país).

## Consequências

**Positivas**
- Portabilidade total: abre por `file://`, sem toolchain.
- Superfície de supply-chain mínima: sem `node_modules`.
- Determinístico: nada muda entre execuções por atualização de dependência.

**Negativas / trade-offs**
- Reimplementação manual de coisas que D3/Chart.js dariam de graça (projeção, decodificador
  TopoJSON, escalas). Ver [Módulos](../modulos.md).
- Arquivo grande (~2.778 linhas) com 5 linhas gigantes de dado embutido que **não devem ser
  reformatadas** (`index.html:989-993`).
- `fetch` do `.env` e do CSV de amostra falha por `file://` (CORS) — mitigado servindo por HTTP.
  Ver [Troubleshooting](../../guias/troubleshooting.md).
- `node --check` não valida HTML; é preciso extrair o `<script>` para checar sintaxe. Ver
  [Desenvolvimento](../../guias/desenvolvimento.md).

## Alternativas descartadas

| Alternativa | Motivo da recusa |
|---|---|
| SPA com bundler (Vite/Webpack) | Exige build e servidor; quebra o "abre por duplo clique". |
| D3 via CDN | Adiciona `<script src>` e dependência de rede; viola o princípio de arquivo único. |

## Referências

- [Visão geral](../visao-geral.md)
- [`CLAUDE.md`](../../../CLAUDE.md) — regras não-negociáveis.
</content>

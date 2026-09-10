---
title: Operação — Runbook
resumo: Operação do dia a dia — subir o painel, verificar integrações, regenerar dados embutidos e responder a incidentes.
atualizado_em: 2026-09-10
responsavel: docs-site-nitro
tags: [operacao, runbook, incidentes]
---

# Operação — Runbook

## Sumário
- [Subir o painel](#subir-o-painel)
- [Verificação de saúde](#verificação-de-saúde)
- [Rotina: trocar a amostra de dados](#rotina-trocar-a-amostra-de-dados)
- [Rotina: regenerar dados embutidos](#rotina-regenerar-dados-embutidos)
- [Incidentes comuns](#incidentes-comuns)
- [Referências cruzadas](#referências-cruzadas)

## Subir o painel

```bash
cd C:/Users/integral/Desktop/claude_nitro/Dashboards_alcohol
python -m http.server 8000
# http://localhost:8000/Dashboards/index.html
```

Servir pela **raiz** garante que o `.env` seja alcançável. Ver
[Deploy](../guias/deploy.md).

## Verificação de saúde

| Verificação | Esperado |
|---|---|
| Abrir a URL | intake (landing) aparece |
| Arrastar `Dados/drinks.csv` | 7 KPIs + mapa + gráficos preenchidos |
| Trocar métrica/faixa | repinta na hora |
| Chat (`.env` com Gemini) | responde e mostra o modelo usado no rodapé |
| Clima (`.env` com OpenWeather, HTTPS) | widget na barra superior |
| Suporte | enviar registra chamado (ver Supabase) |

## Rotina: trocar a amostra de dados

Substitua `Dados/drinks.csv` mantendo um schema compatível (ver
[Schema do CSV](../referencia/csv-schema.md)). Nenhuma mudança de código é necessária: o parser
reconhece colunas por regex e cria métricas genéricas para o resto.

## Rotina: regenerar dados embutidos

> [!WARNING]
> `WORLD` e `CMETA` (`index.html:992-993`) foram gerados por um script Python de build (Natural
> Earth 110m + `country_converter`) que **não faz parte do repositório**. Só reprocessar se for
> trocar o atlas ou os países — o normal é não tocar nessas linhas. Os logos vieram das imagens
> do PDF do brand book.

## Incidentes comuns

| Incidente | Ação imediata | Referência |
|---|---|---|
| Painel em branco | recarregar; se persistir, verificar regressão no rAF | [ADR-0002](../arquitetura/decisoes/ADR-0002-render-scheduler.md) |
| Chat sempre falha | checar quota/validade da `GEMINI_API_KEY` e a lista `MODELS` | [Integrações](../referencia/integracoes.md#gemini-chat) |
| Clima não aparece | confirmar `OPENWEATHER_API_KEY` e HTTPS | [Troubleshooting](../guias/troubleshooting.md#clima) |
| Suporte não grava | checar conectividade e RLS de `support_messages` | [ADR-0003](../arquitetura/decisoes/ADR-0003-suporte-supabase.md) |
| CSV rejeitado | validar cabeçalho/decimais/separador | [Schema do CSV](../referencia/csv-schema.md) |

## Referências cruzadas

- [Deploy](../guias/deploy.md)
- [Troubleshooting](../guias/troubleshooting.md)
- [Segurança](seguranca.md)
- [Configuração](../referencia/configuracao.md)
</content>

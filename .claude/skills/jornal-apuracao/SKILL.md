---
name: jornal-apuracao
description: Apura a atividade do repositório no GitHub (issues abertas e fechadas, PRs, merges, discussions, commits, releases e o backlog parado) e fecha a "pauta" do dia num JSON. Use SEMPRE antes de escrever uma edição do Diário da Nitro, e também quando o Caio pedir "o que andou acontecendo", "resumo do repo" ou "o que rolou hoje".
---

# Apuração — o repórter do Diário da Nitro

Esta skill é a **primeira metade** do jornal: sai a campo, coleta tudo e volta com a
pauta. Quem escreve é a outra ([`jornal-edicao`](../jornal-edicao/SKILL.md)).

Não escreva matéria aqui. O produto desta skill é um arquivo: `Jornal/pauta-mais-recente.json`.

## Como apurar

Um comando só, da raiz do projeto:

```bash
python .claude/skills/jornal-apuracao/apurar.py
```

Sem argumentos ele apura **da última edição até agora**, lendo o corte em `Jornal/estado.json`.
É o que garante que nenhuma notícia caia no vão entre duas edições nem saia repetida.
Na primeira edição da história, a janela é de 24 h.

Variações que às vezes fazem falta:

```bash
python .claude/skills/jornal-apuracao/apurar.py --desde 2026-09-01T00:00:00Z   # edição especial / retroativa
python .claude/skills/jornal-apuracao/apurar.py --saida Jornal/pautas/teste.json
```

Pré-requisito: `gh auth status` precisa responder autenticado. Se não estiver, **pare** e
avise o Caio — não invente números para preencher a edição.

## O que volta na pauta

`Jornal/pauta-mais-recente.json`, em português, com estas seções:

| campo | o que é |
|---|---|
| `janela` | `desde` / `até` em ISO-8601 UTC — o período coberto por esta edição |
| `edicaoNumero` | número da próxima edição (último + 1, lido de `estado.json`) |
| `issuesAbertas` | criadas na janela: título, **corpo**, autor, rótulos, link |
| `issuesFechadas` | fechadas na janela, com `motivo` e os últimos comentários da `conversa` |
| `prsAbertos` / `prsMergeados` / `prsFechadosSemMerge` | com corpo, `linhas` (+/−/arquivos) e `resolve` (issues que a PR fecha) |
| `discussions` | as movimentadas na janela, com corpo, categoria e `comentariosNovos` |
| `commits`, `releases` | mensagem, autor, horário, link |
| `estoque` | a foto do acervo: backlog aberto, `maisVelhasParadas`, `prsEsperando` (com dias parados) |
| `placar` | os números já somados, prontos para o quadro "Os números do dia" |
| `diaVazio` | `true` quando nada se mexeu — a edição muda de tom (veja a skill de edição) |

Dois campos merecem atenção porque **viram matéria**:

- **`issuesFechadas[].motivo`** — `COMPLETED` é problema resolvido; `NOT_PLANNED` é problema
  descartado. Jornal que soma os dois num número só está mentindo para o leitor.
- **`estoque.maisVelhasParadas` / `prsEsperando`** — o que ninguém tocou. É daqui que sai a
  cobrança do "Radar" e da "Mesa do Dono". A ausência de notícia também é notícia.

## Depois de apurar

Leia o JSON inteiro antes de escrever uma linha. Você precisa dos **corpos** das issues e PRs,
não só das contagens: sem eles a edição vira uma lista de títulos, que é exatamente o que o
Caio já não consegue digerir.

Então siga para `jornal-edicao`.

## Notas de manutenção

- O script não depende de `jq` — monta o JSON em Python. Só precisa de `gh` e Python 3.8+.
- Falha de uma coleta isolada (rede, permissão) vira `[aviso]` no stderr e a seção volta vazia;
  a edição sai mesmo assim, capenga mas honesta. Falha do `gh` inteiro aborta.
- Corpos são cortados em 2400 caracteres com marca `[... cortado, +N caracteres]`. Se precisar
  do texto inteiro de uma issue específica, busque com `gh issue view N --repo <repo>`.
- O repositório padrão é `caioross/nitro-dashboards-alcool`; sobreponha com `--repo` ou a
  variável de ambiente `JORNAL_REPO`.

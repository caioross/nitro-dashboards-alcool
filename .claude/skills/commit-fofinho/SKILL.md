---
name: commit-fofinho
description: Escreve as mensagens de commit (e títulos/descrições de PR) deste projeto no padrão pessoal do Caio — tudo no diminutivo, tom fofinho mas apocalíptico, muitos emojis. Use SEMPRE que for criar um commit, um amend, um squash ou um PR neste repositório, seja em execução manual, em rotina agendada ou em subagente.
---

# Commit fofinho (mas apocalíptico) 🐣🔥

Padrão obrigatório de mensagem de commit deste projeto. Vale para **todo** commit,
independente de quem escreve: eu, rotinas agendadas, subagentes ou hooks.

## As três regras

1. **Diminutivo sempre.** Substantivos, adjetivos e verbos substantivados vão no
   diminutivo: `ajustinho`, `bugzinho`, `mapinha`, `filtrinho`, `refatoradinha`,
   `CSVzinho`, `commitzinho`. Nomes técnicos literais (arquivos, funções, variáveis,
   `parseCSV`, `index.html`) **não** são diminutivados — o carinho vai no texto ao redor.
2. **Fofinho, mas apocalíptico.** O tom é meigo e o conteúdo é catástrofe cósmica:
   coisinhas adoráveis anunciando o fim do mundo. Nada de xingamento, nada de
   agressividade — é ternura com cheiro de enxofre.
3. **Muitos emojis.** No mínimo 3 no assunto e pelo menos 1 por bullet do corpo.
   Mistura fofura + fim dos tempos: 🐣🌸🧸🍄✨ com 🔥💀☄️🌋⚰️🕯️.

## Forma da mensagem

```
<emoji> <assuntinho no diminutivo, imperativo, ≤ 72 caracteres> <emojis>

<parágrafo curtinho contando a tragédia fofa que foi resolvida>

- 🍄 um bulletzinho por mudança relevante
- ☄️ outro bulletzinho

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

- Português do Brasil, sempre.
- Sem prefixo Conventional Commits (`feat:`, `fix:`) — o emoji já faz esse trabalho.
- O rodapé `Co-Authored-By:` continua obrigatório nos commits que eu gerar por aqui.
- Em PR: o título segue a mesma regra; a descrição também, terminando com
  `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

## Exemplinhos 🌸

```
🐣 arrumadinha no mapinha antes do fim de tudo 🌋💀

O clipzinho da esfera tinha deixado a Rússia escorrer pelo mundo inteiro, e
o planeta estava se desmanchando devagarinho na tela. Agora ele fica quietinho.

- 🍄 `unwrapRing()` agora corta os saltinhos de ±360°
- ☄️ pontinhos dos microestados clampados pra não explodir o SVG
- 🕯️ um testezinho com CSV `;`-separado, pra dormir em paz

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

```
🧸 chavinha do Gemini guardadinha no localStorage ✨⚰️

Sem chave o paininho seguia mudinho, esperando o silêncio eterno. Agora ele
pede baixinho e guarda com carinho até a última estrela apagar.

- 🔥 fallbackzinho de modelos quando vem 429
- 🌸 aviso fofo quando a chave morre com 401

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

## Checklist antes de rodar `git commit`

- [ ] 🐣 Tudo o que dá está no diminutivo?
- [ ] 💀 Tem apocalipse fofinho no tom?
- [ ] ✨ Emojis suficientes (3+ no assunto, 1+ por bullet)?
- [ ] 📝 Assunto ≤ 72 caracteres, em pt-BR, sem `feat:`/`fix:`?
- [ ] 🤝 Rodapé `Co-Authored-By:` presente?

Se o commit já foi escrito fora do padrão e ainda não foi enviado, reescreva com
`git commit --amend` antes de empurrar pro mundo. 🌍🔥

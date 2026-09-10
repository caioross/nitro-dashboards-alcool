---
name: jornal-edicao
description: Escreve e diagrama uma edição do "Diário da Nitro" a partir da pauta apurada — manchete, capa, os números do dia, a mesa do dono, opinião, voz da comunidade e radar — grava em Jornal/edicoes/ e fecha o estado. Use depois de `jornal-apuracao`, sempre que for produzir o jornal diário ou uma edição avulsa.
---

# Edição — a redação do Diário da Nitro

Segunda metade do jornal. A pauta já está fechada por
[`jornal-apuracao`](../jornal-apuracao/SKILL.md); aqui ela vira **jornal**.

O leitor é uma pessoa só: o Caio, dono do projeto, que não conseguiu acompanhar o dia e
tem dez minutos. Ele não quer o log do GitHub — ele já tem o GitHub. Ele quer saber
**o que mudou, o que isso significa e o que depende dele.**

## Ritual

1. **Leia a pauta inteira**: `Jornal/pauta-mais-recente.json`. Os corpos das issues e PRs,
   não só as contagens — é de lá que sai a matéria.
2. **Escolha a capa** antes de escrever qualquer coisa (critério abaixo).
3. **Escreva** copiando `modelo.html` desta pasta e trocando os `{{MARCADORES}}`.
   Grave em `Jornal/edicoes/AAAA-MM-DD.html` (a data do dia da edição).
4. **Feche**: `python .claude/skills/jornal-edicao/publicar.py Jornal/edicoes/AAAA-MM-DD.html`
   Ele recusa a edição se sobrou marcador — o que é bom, é a revisão antes da impressora.

## Como escolher a capa

Manda a **consequência**, não o tamanho do diff. Nesta ordem:

1. Algo que já morde o usuário ou o dinheiro (segurança, dado errado na tela, promessa falsa).
2. Algo que mudou de estado de forma irreversível hoje (mergeado **e** aplicado, com prova).
3. O padrão que se repete — três issues pequenas que contam a mesma história valem mais
   capa do que uma PR grande de refatoração.
4. Dia fraco de merge: a capa pode ser uma **discussion**, uma issue bem argumentada ou o
   que está travado há semanas. Represamento é notícia.

Se a capa não couber numa frase que um estranho entenda, não é a capa certa.

## As sete regras da casa

1. **Nenhum número que não esteja na pauta.** Nem arredondado, nem "cerca de". Se um dado
   não foi apurado, a frase muda — o número não.
2. **"Mergeado" não é "corrigido em produção".** Só escreva que algo está resolvido para o
   usuário se a pauta mostrar prova disso. Na dúvida: "mergeado hoje; ainda não há prova
   em produção nesta apuração".
3. **Título com verbo, sem jargão.** "A tela de importação promete privacidade que o chat
   não cumpre" — não "Fix XSS em innerHTML (#2)".
4. **Toda matéria termina no bolso do leitor.** O bloco `📌 Por que importa para você` traduz
   em consequência: o que o usuário sentia antes, o que sente agora. Nunca repita o título.
5. **Diga a issue e a PR.** Sempre `(#123 → PR #124)` no fim do parágrafo, com link.
6. **Issue descartada não é issue resolvida.** `motivo: NOT_PLANNED` na pauta vira uma frase
   própria — "descartada", não somada às resolvidas.
7. **Dia fraco sai fraco.** Nunca encha linguiça, nunca invente relevância. Uma edição de
   três parágrafos que diz "hoje foi dia de manutenção, e aqui está a única coisa que
   importa" vale mais que seis seções infladas — e preserva a confiança no dia em que o
   jornal gritar de verdade.

## Voz

Jornal de verdade, escrito por quem conhece o código e respeita o leitor. Frase curta.
Português direto, sem "otimizamos a experiência". Pode ser seco e pode ser irônico, desde
que o alvo seja o problema e nunca a pessoa. A redação **cobra**, inclusive a si mesma:
quando uma PR da própria frota está parada há duas semanas, isso vai para o jornal com
o número de dias.

Não use "nós entregamos". Use o que aconteceu: "a issue nasceu às 11h16 e a correção
entrou às 23h11 do mesmo dia".

## As seções

| seção | quando entra | o que é |
|---|---|---|
| **Clima do projeto** | sempre | 2–4 frases no topo. O dia inteiro para quem só lê isso. Diga a qualidade do dia, não só o volume. |
| **Capa** | sempre | Chapéu + título + linha-fina + 3 a 6 parágrafos + 📌. |
| **Os números do dia** | sempre | Do `placar` da pauta. Pares de células; a nota de rodapé explica o **saldo** (fechou X, abriu Y) e o que ele diz do backlog. |
| **Matérias** | 1 a 3 | Os outros assuntos com peso próprio. Mesma anatomia da capa, menores. |
| **Bastidores** | quando houver | Um parágrafo curto por correção silenciosa: refatoração, dependência, teste, doc. Sem drama. |
| **🖋 A mesa do dono** | **sempre** | Só o que exige credencial dele, painel de terceiro ou dinheiro. Com passo a passo e um comando de conferência. Se hoje não há nada: diga "hoje sua mesa está limpa" — e é uma boa notícia. |
| **Opinião** | quando houver tese | Coluna assinada por uma persona da redação (ex.: *Duda, especialista de UI/UX*; *Nando, relações com criadores*). Uma tese que atravessa vários fatos do dia. Assine sempre. |
| **A voz da comunidade** | quando houver discussion | Cite o texto real de uma discussion (`comentariosNovos` na pauta), entre aspas, e responda com honestidade — inclusive quando a resposta é "não dá para fazer agora, e eis o porquê". |
| **Radar · em trânsito** | sempre | O que está aberto e o que espera. Puxe de `estoque.maisVelhasParadas` e `estoque.prsEsperando`, com os dias parados. |

Seção opcional sem assunto: **apague a `<section>` inteira**. Não deixe um título órfão.

## Dia vazio (`diaVazio: true` na pauta)

Não force. Publique assim:

- **Clima**: diga que não houve movimento no repositório na janela e desde quando.
- **Números**: publique os zeros — zero é informação.
- **Radar** e **Mesa do dono**: estes ficam, e ganham o espaço. Um dia sem commit é o
  melhor dia para olhar o que está parado há três semanas.
- Apague capa, matérias, bastidores, opinião e voz.

## Diagramação

`modelo.html` é o único gabarito. Não invente CSS novo por edição — a marca é a mesma
todo dia e a familiaridade é o que torna o jornal rápido de ler.

- Marca Nitro: Admiral Blue `#003663`, Chartreuse `#94C356`, Citron `#B9DA00`, Poppins.
  Rótulos em caixa alta com tracking largo; números tabulares.
- O corpo das matérias é serifado (Georgia) de propósito: é o que dá a textura de jornal
  e sustenta a leitura longa. Título, rótulo e número seguem Poppins, que é a marca.
- No fim de `modelo.html` há um comentário com os **pedaços reutilizáveis** (matéria, linha
  de números, item da mesa, linha do radar). Copie de lá em vez de recriar a marcação.
- O HTML é autocontido, sem `<script>` e sem rede — abre por `file://` e sobrevive a ser
  colado num e-mail.

## Onde as edições ficam

```
Jornal/
  estado.json                     número da última edição + corte da janela
  pauta-mais-recente.json         pauta da edição em produção
  edicoes/
    2026-09-09.html               A EDIÇÃO
    2026-09-09.pauta.json         a apuração que a originou, arquivada
```

## Depois de publicar

Mostre ao Caio, na conversa:

- o número e o caminho da edição;
- o **clima do projeto**, em texto, para ele ler sem abrir nada;
- a **mesa do dono** — os itens que dependem dele hoje;
- e mande o arquivo com `SendUserFile` (`display: "render"`), para abrir na hora.

## Manutenção

- Envio por e-mail está **desligado** hoje (não há conector de e-mail nem SMTP configurado):
  a rotina salva e avisa. Para ligar depois, o caminho mais curto é uma App Password do
  Gmail no `.env` e um envio SMTP do HTML já pronto — o jornal não muda em nada.
- `publicar.py` avança `estado.json`. Se uma edição sair errada e você regravar o arquivo,
  rode `publicar.py` de novo: o número vem da pauta, então não pula.

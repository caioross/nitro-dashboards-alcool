# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## O que é este projeto

Dashboard de consumo de bebidas alcoólicas para a **Nitro** (divisão da "Deixa Comigo Bebidas").
O entregável é **um único arquivo**: `Dashboards/index.html` (~213 KB), sem build step, sem
dependências de runtime e sem chamadas de rede além da folha de estilo do Google Fonts (Poppins,
com fallback de sistema). Abre por `file://`.

```
Dados/drinks.csv                              amostra (193 países × 4 métricas)
.env                                          chaves de API (gitignored; .env.example versionado)
Dashboards/index.html                         O ENTREGÁVEL — editar aqui
Referencias/nitro_brand_book_by_pomelli.pdf   brandbook (fonte da paleta/logo)
```

## Regras não-negociáveis

- **Nada de dado mocado.** Todo número exibido vem do CSV que o usuário importa em runtime.
  Os únicos dados embutidos são *metadados de referência*: logos base64, o TopoJSON do mundo e
  `CMETA` (ISO3 / ISO-numérico / continente por país).
- **Mínimo de interações.** O público é técnico e quer abrir e subir a planilha. Não introduzir
  botão "Aplicar"/"Gerar": qualquer filtro repinta imediatamente.
- **Arquivo único.** Não adicionar `<script src>`/`<link>` para bibliotecas (D3, Chart.js etc.).
  Mapa, escalas, projeção, estatística e animações são todos implementados à mão.
- **Marca** (extraída do brandbook): Admiral Blue `#003663`, Pure White `#FFFFFF`,
  Chartreuse `#94C356`, Citron `#B9DA00`, tipografia **Poppins**. Rótulos em caixa alta com
  tracking largo ("Wide-Set Tech Typography"), números tabulares.
- **UI em pt-BR**, formatação via `Intl.NumberFormat('pt-BR')`.

## Como editar

`index.html` é editado **no lugar**. É um arquivo grande mas cortado em seções comentadas —
localize pelo banner antes de mexer:

```bash
grep -n "^/\* =\|^<!-- =" Dashboards/index.html
```

Layout aproximado (as linhas se deslocam conforme edições):

| faixa | conteúdo |
|---|---|
| `<style>` … `</style>` | tokens `:root`, HEADER, INTAKE, DASHBOARD (inclui os breakpoints) |
| markup | INTAKE (landing/dropzone) → DASHBOARD → SUPORTE (modal) → `#tip` |
| `NITRO_LOGO_W/D`, `NITRO_MARK`, `WORLD`, `CMETA` | 3 linhas gigantes de dado embutido — **não** abrir/reformatar |
| `<script>` restante | UTIL → CSV PARSING → TOPOJSON+PROJEÇÃO → ESTADO → TOOLTIP → INTAKE/IO → CONTROLES → KPIs → MAPA → MATRIZ → DISPERSÃO → RANKING → CONTINENTE → HISTOGRAMA → r POR CONTINENTE → TABELA → RENDER → CHAVES(.env) → CLIMA → CHAT IA → boot |

Para validar o JS depois de editar (o `node --check` não aceita HTML — extraia o script):

```bash
sed -n '/^<script>$/,/^<\/script>$/p' Dashboards/index.html | sed '1d;$d' > "$TMPDIR/_check.js" && node --check "$TMPDIR/_check.js"
```

Para ver no navegador use `preview_start` apontando para o arquivo; a checagem de fato é
importar um CSV e conferir os KPIs, não só olhar a tela.

## Arquitetura do runtime

**Pipeline:** `readFile` → `parseCSV` → `buildDataset` → `ST` (estado global) → `renderAll` → `paint`.

- **`parseCSV`** é deliberadamente tolerante: remove BOM, autodetecta separador (`, ; \t |`),
  respeita aspas RFC, e `toNum` normaliza decimal pt-BR e en-US. Se você mexer aqui, teste com
  um CSV `;`-separado, cabeçalhos em português e vírgula decimal.
- **`buildDataset`/`COLDEFS`** casa colunas por regex (cerveja / destilados / vinho / álcool puro,
  PT e EN). Colunas numéricas não reconhecidas viram métricas genéricas automaticamente — o painel
  não pode assumir as 4 colunas do `drinks.csv`.
- **`ST`** guarda dataset, métrica ativa, filtros (continentes, busca de país, faixa min/max),
  par X/Y da dispersão e o zoom do mapa. Toda mutação deve terminar chamando `renderAll()`.
- **`renderAll(first)` é o agendador; `paint(first)` é o corpo síncrono.** `requestAnimationFrame`
  fica suspenso em aba oculta — por isso `renderAll` chama `paint` direto quando `document.hidden`.
  Nunca voltar a colocar a lógica de render dentro do rAF sem esse desvio: já causou o painel
  ficar em branco para sempre (flag `rafPending` presa em `true`).
- **Animações precisam de failsafe.** `.enter{opacity:0}` + relógio de animação congelado deixa
  painel invisível: por isso existem `settle()`, a regra `.enter.done{...!important}`, os
  curto-circuitos por `document.hidden` em `animate()`/`countUp()`, o bloco
  `prefers-reduced-motion` e o re-render no `visibilitychange`.

### Mapa (o pedaço mais delicado)

- Projeção **Natural Earth I** (`neRaw`, mesma formulação do D3) com **y negado** em `projectRaw`
  — SVG cresce para baixo, a projeção cresce para o norte.
- Decodificador **TopoJSON** próprio: arcos quantizados delta-encodados; índice de arco negativo
  significa arco invertido (`~i`).
- `unwrapRing()` remove os saltos de ±360° e `pathOf()` emite subpaths deslocados; sem isso
  Rússia (643), Fiji (242) e Antártida (010) viram faixas atravessando o mapa. O grupo de países
  é recortado por um `clipPath` de esfera.
- **Todo valor geométrico animado precisa ser clampado** (`Math.max(0, …)`): o SVG lança exceção
  em `r`/`width`/`height` negativos, e a interpolação passa por valores intermediários.
- 29 microestados não existem no atlas 110m — vêm de `CMETA[...].p` (centroide) e são desenhados
  como pontos. Ao contar países no mapa use o contador `drawn` (incrementado só quando a geometria
  casa com uma linha do dado), não `byId.size + dots`.
- Zoom do mapa exige **Ctrl/⌘ + roda**; roda pura rola a página. Foi decisão de UX, não bug.

### Armadilhas de CSS já resolvidas

- Nada de `background-attachment: fixed` nem `backdrop-filter` pesado: causavam conteúdo em branco
  ao rolar. A ambiência é uma camada `body::before` fixa em `z-index:0`, com `#intake`/`#dash` em
  `z-index:1`.
- Breakpoints em 1560 / 1250 / 1050 px reorganizam os spans do grid de 12 colunas e os 7 cards de KPI.


## Integrações externas (Gemini e OpenWeatherMap)

São as **únicas** chamadas de rede além do Google Fonts, e ambas são opcionais: sem chave,
o painel se comporta como antes.

- **Chaves.** Vivem no `.env` da raiz (gitignored). O objeto `ENV` faz `fetch` de
  `.env`, `../.env` e `../../.env` no load — funciona servindo por HTTP, falha em
  `file://` por CORS. O fallback é o `localStorage` (`nitro.GEMINI_API_KEY`), preenchido
  pelo bloco `#aiKeyAsk` do próprio chat. **Não criar `config.js`.**
- **Chat (`#aiPanel`).** `snapshot()` monta o contexto a partir de `filtered()` — logo,
  mexer nos filtros muda o que o modelo enxerga, e é isso que garante o requisito de
  "respeitar os filtros". Os chips de `#aiScope` são repintados por `refreshAIScope()`,
  chamada no fim de `paint()`. Ao mudar `ST`, nada precisa ser feito aqui.
- **Fallback de modelos.** `MODELS` é percorrido em ordem; 429/5xx/404/400 e resposta
  vazia caem para o próximo. 401/403 abortam e pedem a chave de novo. Ao trocar a lista,
  confira o que a chave enxerga em `GET /v1beta/models` — o Google retira modelos antigos
  com frequência e o 404 traz a sugestão do substituto.
- **`maxOutputTokens` precisa de folga.** Os modelos com raciocínio gastam tokens antes
  de emitir texto; com o limite apertado o stream volta sem `parts[].text` e o fallback
  percorre a lista inteira à toa. Está em 8192.
- **O SSE do Gemini usa CRLF.** Os eventos vêm separados por `

` e o último pode
  não ter delimitador. O parser normaliza `
` → `
` e consome o resto do buffer no
  fim do stream — sem isso a resposta chega íntegra e é descartada silenciosamente.
- **Clima (`#wx`).** Geolocalização → OpenWeather; permissão negada cai para cidade
  digitada (`nitro.wxCity`). Cache de 15 min em `nitro.wx`. Some abaixo de 900 px.

## Regenerar os dados embutidos

`WORLD` e `CMETA` foram gerados por um script Python de build (Natural Earth 110m +
`country_converter`) que grava as constantes como linhas `const … = …;`. Ele não faz parte do
repositório — só rode algo assim se precisar trocar o atlas ou reprocessar os países; o normal é
não tocar nessas linhas. Os logos vieram das imagens extraídas do PDF do brandbook.

## Comportamento conhecido (não "consertar" sem pensar)

- O botão *"Carregar ../Dados/drinks.csv"* usa `fetch`, então **falha por `file://`** (CORS). O
  painel mostra a mensagem certa e o usuário arrasta o arquivo ou usa "Selecionar arquivo". Servir
  por HTTP faz o botão funcionar.
- O modal "Suporte" é uma maquete: valida e mostra confirmação, **não envia nada** para lugar nenhum.
- Pelo mesmo motivo do CORS, o `.env` **não é lido em `file://`** — o chat pede a chave na
  interface. Não é bug; servir por HTTP resolve.
- Capturas de tela do painel de browser às vezes pegam frames no meio da animação. Confirme o
  estado por consulta ao DOM antes de concluir que quebrou.

## Padrão de commit (obrigatório) 🐣💀

**Toda** mensagem de commit e todo título/descrição de PR deste repositório seguem o
padrão pessoal do dono do projeto: diminutivo, tom fofinho mas apocalíptico, muitos emojis.

Antes de rodar `git commit`, `git commit --amend` ou `gh pr create`, invoque a skill
`commit-fofinho` (`.claude/skills/commit-fofinho/SKILL.md`) e escreva a mensagem por ela.
Isso vale para execução interativa, rotinas agendadas, hooks e subagentes — **sem exceção**.
Se você é um subagente que vai commitar, leia a skill antes de escrever a mensagem.

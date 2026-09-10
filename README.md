# Nitro · Dashboard de Consumo de Bebidas Alcoólicas

Dashboard interativo de consumo de bebidas alcoólicas por país, feito para a **Nitro**
(divisão da *Deixa Comigo Bebidas*).

O entregável é **um único arquivo**: [`Dashboards/index.html`](Dashboards/index.html) —
sem build step, sem dependências de runtime e sem chamadas de rede além da folha de estilo
do Google Fonts (Poppins, com fallback de sistema). Abre direto por `file://`.

> **Documentação técnica de engenharia:** [`docs/README.md`](docs/README.md) — arquitetura,
> referência de API interna, schema do CSV, integrações, guias e operação.

---

## Como usar

1. Abra `Dashboards/index.html` no navegador (duplo clique já funciona).
2. Arraste um CSV para a área de importação — ou clique em **Selecionar arquivo**.
3. Os KPIs, o mapa e todos os gráficos repintam imediatamente. Qualquer filtro
   (continente, busca de país, faixa mín/máx, par X/Y da dispersão) reage na hora,
   sem botão "Aplicar".

> O botão *"Carregar ../Dados/drinks.csv"* usa `fetch` e **falha por `file://`** (CORS).
> Isso é esperado: arraste o arquivo ou use "Selecionar arquivo". Servindo por HTTP o
> botão passa a funcionar.

### Servindo por HTTP (opcional)

```bash
cd Dashboards
python -m http.server 8000
# abra http://localhost:8000
```

---

## Integrações opcionais (chaves no `.env`)

Duas funcionalidades dependem de API externa e são **opcionais** — sem chave, o painel
funciona exatamente como antes.

| Recurso | Onde aparece | API |
|---|---|---|
| **Conversar com os dados** | botão na parte inferior central | Google Gemini |
| **Previsão do tempo** | barra superior | OpenWeatherMap |

### Configurando

```bash
cp .env.example .env   # e preencha as duas chaves
```

```dotenv
GEMINI_API_KEY=...
OPENWEATHER_API_KEY=...
```

O `.env` fica **fora do versionamento** (`.gitignore`) e é lido em runtime pelo próprio
`index.html` — não existe `config.js` nem build step.

> **`file://` não lê o `.env`.** O navegador bloqueia `fetch` de arquivo local (mesma
> limitação do botão *"Carregar ../Dados/drinks.csv"*). Sirva a **raiz do repositório**
> por HTTP para o `.env` ser encontrado:
>
> ```bash
> python -m http.server 8000
> # abra http://localhost:8000/Dashboards/index.html
> ```
>
> Sem isso, o painel pede a chave do Gemini na própria interface e a guarda apenas no
> `localStorage` do navegador.

### Chat com IA

- O contexto enviado ao modelo é montado a partir de `filtered()` — ou seja, **respeita
  os filtros ativos**: métrica em foco, continentes, busca de país e faixa mín/máx.
  Os chips no topo do painel mostram exatamente o recorte que foi enviado.
- Vai estatística descritiva, correlações de Pearson, agregado por continente e o
  ranking da seleção. Nenhum número é inventado: tudo sai do CSV importado.
- **Fallback de modelos**: quota estourada (429), indisponibilidade (5xx) ou modelo
  retirado (404) fazem cair automaticamente para o próximo da cadeia —
  `gemini-3.8-flash` → `gemini-3.5-flash` → `gemini-flash-latest` →
  `gemini-3.5-flash-lite` → `gemini-2.5-flash`. O rodapé do chat mostra qual respondeu.

### Clima

- Usa `navigator.geolocation`; negada a permissão (ou sem HTTPS/localhost), o widget
  vira clicável e aceita a cidade digitada.
- Cache de 15 min em `localStorage` para não queimar o limite gratuito a cada F5.

---

## Formato do CSV

O parser é tolerante: remove BOM, autodetecta separador (`, ; \t |`), respeita aspas RFC
e normaliza decimal pt-BR (vírgula) e en-US (ponto). As colunas são casadas por regex
(cerveja / destilados / vinho / álcool puro, em PT e EN); colunas numéricas não
reconhecidas viram métricas genéricas automaticamente.

Exemplo mínimo ([`Dados/drinks.csv`](Dados/drinks.csv), 193 países):

```csv
country,beer_servings,spirit_servings,wine_servings,total_litres_of_pure_alcohol
Afghanistan,0,0,0,0.0
Albania,89,132,54,4.9
Algeria,25,0,14,0.7
```

Cabeçalhos em português e `;` como separador também funcionam.

---

## Estrutura do repositório

```
Dados/drinks.csv        Amostra de dados (193 países × 4 métricas)
Dashboards/index.html   O ENTREGÁVEL — dashboard completo em um arquivo
.env.example            Modelo das chaves de API (copie para .env)
CLAUDE.md               Guia de arquitetura e regras de manutenção
```

O brand book da Nitro (`Referencias/`) **não** faz parte do repositório —
fica apenas na cópia local.

---

## Princípios de design

- **Nada de dado mocado.** Todo número exibido vem do CSV importado em runtime. Os únicos
  dados embutidos são metadados de referência: logos, o TopoJSON do mundo e o mapa
  ISO3 / ISO-numérico / continente por país.
- **Arquivo único.** Mapa, projeção (Natural Earth I), escalas, estatística e animações
  são todos implementados à mão — sem D3, Chart.js ou qualquer `<script src>`.
- **Mínimo de interações.** O público é técnico: abrir, subir a planilha, ler.
- **Marca Nitro:** Admiral Blue `#003663`, Pure White `#FFFFFF`, Chartreuse `#94C356`,
  Citron `#B9DA00`; tipografia Poppins; rótulos em caixa alta com tracking largo;
  números tabulares.
- **UI em pt-BR**, formatação via `Intl.NumberFormat('pt-BR')`.

---

## Notas

- Zoom do mapa exige **Ctrl / ⌘ + roda do mouse** (roda pura rola a página) — decisão de UX.
- O modal "Suporte" é uma maquete: valida e mostra confirmação, mas não envia nada.
- As chaves do `.env` chegam ao navegador em texto claro — é um painel interno.
  Para uso público, ponha as chamadas ao Gemini e ao OpenWeather atrás de um proxy.
- Detalhes de arquitetura do runtime, do decodificador de TopoJSON e das armadilhas de
  CSS já resolvidas estão em [`CLAUDE.md`](CLAUDE.md).

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apurar.py - A apuracao do Diario da Nitro.

Varre o repositorio no GitHub e devolve TUDO que aconteceu na janela do dia
num unico JSON (a "pauta"), pronto para a skill `jornal-edicao` transformar
em materia.

Uso:
    python apurar.py                       # janela = desde o corte da ultima edicao
    python apurar.py --desde 2026-09-09T00:00:00Z
    python apurar.py --repo dono/repo --saida caminho/pauta.json

Depende so de `gh` autenticado (gh auth status) e Python 3.8+.
Nao usa jq: o JSON e montado aqui.
"""

import argparse
import io
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Windows: garante UTF-8 na saida, senao acentos/emoji explodem em cp1252.
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

REPO_PADRAO = "caioross/nitro-dashboards-alcool"
LIMITE_CORPO = 2400  # corta corpos gigantes; a manchete nao precisa do anexo inteiro


# --------------------------------------------------------------------------- #
# infraestrutura
# --------------------------------------------------------------------------- #

def gh(*args, entrada=None):
    """Roda `gh` e devolve stdout. Erro de rede/permissao vira excecao clara."""
    cmd = ["gh", *args]
    try:
        r = subprocess.run(
            cmd, input=entrada, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=120,
        )
    except FileNotFoundError:
        raise SystemExit("gh nao encontrado no PATH. Instale o GitHub CLI.")
    except subprocess.TimeoutExpired:
        raise SystemExit(f"gh travou (>120s): {' '.join(cmd[:3])}")
    if r.returncode != 0:
        raise RuntimeError(f"gh falhou ({r.returncode}): {' '.join(cmd[:4])}\n{r.stderr.strip()}")
    return r.stdout


def gh_json(*args, entrada=None, padrao=None):
    """gh + json.loads, tolerante: se a chamada falhar a edicao nao morre por isso."""
    try:
        saida = gh(*args, entrada=entrada).strip()
    except RuntimeError as e:
        print(f"[aviso] {e}", file=sys.stderr)
        return padrao if padrao is not None else []
    if not saida:
        return padrao if padrao is not None else []
    try:
        return json.loads(saida)
    except json.JSONDecodeError:
        print(f"[aviso] resposta nao-JSON de: {' '.join(args[:3])}", file=sys.stderr)
        return padrao if padrao is not None else []


def corta(texto, limite=LIMITE_CORPO):
    if not texto:
        return ""
    texto = texto.replace("\r\n", "\n").strip()
    if len(texto) <= limite:
        return texto
    return texto[:limite].rstrip() + f"\n\n[... cortado, +{len(texto) - limite} caracteres]"


def login(obj):
    """Extrai o login de um autor, seja dict do gh CLI ou do GraphQL."""
    if not obj:
        return "(desconhecido)"
    if isinstance(obj, str):
        return obj
    return obj.get("login") or obj.get("name") or "(desconhecido)"


# --------------------------------------------------------------------------- #
# coleta
# --------------------------------------------------------------------------- #

def coletar_issues_abertas(repo, desde):
    dados = gh_json(
        "issue", "list", "--repo", repo, "--state", "all",
        "--search", f"created:>={desde}", "--limit", "60",
        "--json", "number,title,body,author,createdAt,state,labels,url,comments",
    )
    return [{
        "numero": i["number"],
        "titulo": i["title"],
        "corpo": corta(i.get("body")),
        "autor": login(i.get("author")),
        "criadaEm": i["createdAt"],
        "estado": i["state"],
        "rotulos": [l["name"] for l in i.get("labels") or []],
        "url": i["url"],
        "qtdComentarios": len(i.get("comments") or []),
    } for i in dados]


def coletar_issues_fechadas(repo, desde):
    dados = gh_json(
        "issue", "list", "--repo", repo, "--state", "closed",
        "--search", f"closed:>={desde}", "--limit", "60",
        "--json", "number,title,body,author,createdAt,closedAt,stateReason,labels,url,comments",
    )
    return [{
        "numero": i["number"],
        "titulo": i["title"],
        "corpo": corta(i.get("body")),
        "autor": login(i.get("author")),
        "criadaEm": i["createdAt"],
        "fechadaEm": i.get("closedAt"),
        # COMPLETED = resolvida de fato; NOT_PLANNED = descartada. A diferenca e materia.
        "motivo": i.get("stateReason") or "COMPLETED",
        "rotulos": [l["name"] for l in i.get("labels") or []],
        "url": i["url"],
        "conversa": [{
            "autor": login(c.get("author")),
            "quando": c.get("createdAt"),
            "texto": corta(c.get("body"), 1200),
        } for c in (i.get("comments") or [])[-4:]],
    } for i in dados]


def coletar_prs(repo, desde, estado, qualificador):
    dados = gh_json(
        "pr", "list", "--repo", repo, "--state", estado,
        "--search", f"{qualificador}:>={desde}", "--limit", "60",
        "--json", ("number,title,body,author,createdAt,mergedAt,closedAt,isDraft,"
                   "additions,deletions,changedFiles,labels,url,closingIssuesReferences"),
    )
    return [{
        "numero": p["number"],
        "titulo": p["title"],
        "corpo": corta(p.get("body")),
        "autor": login(p.get("author")),
        "criadoEm": p.get("createdAt"),
        "mergeadoEm": p.get("mergedAt"),
        "fechadoEm": p.get("closedAt"),
        "rascunho": p.get("isDraft", False),
        "linhas": {"mais": p.get("additions", 0), "menos": p.get("deletions", 0),
                   "arquivos": p.get("changedFiles", 0)},
        "rotulos": [l["name"] for l in p.get("labels") or []],
        "resolve": [f"#{r['number']}" for r in p.get("closingIssuesReferences") or []],
        "url": p["url"],
    } for p in dados]


QUERY_DISCUSSIONS = """
query($o:String!, $r:String!) {
  repository(owner:$o, name:$r) {
    discussions(first:30, orderBy:{field:UPDATED_AT, direction:DESC}) {
      nodes {
        number title bodyText url createdAt updatedAt
        category { name }
        author { login }
        answer { id }
        comments(last:8) {
          totalCount
          nodes { author { login } bodyText createdAt }
        }
      }
    }
  }
}
"""


def coletar_discussions(repo, desde):
    dono, nome = repo.split("/", 1)
    bruto = gh_json("api", "graphql", "-f", f"query={QUERY_DISCUSSIONS}",
                    "-F", f"o={dono}", "-F", f"r={nome}", padrao={})
    nos = (((bruto or {}).get("data") or {}).get("repository") or {}).get("discussions", {}).get("nodes") or []
    saida = []
    for d in nos:
        # so entra na edicao o que se mexeu na janela
        if (d.get("updatedAt") or "") < desde:
            continue
        comentarios = [{
            "autor": login(c.get("author")),
            "quando": c.get("createdAt"),
            "texto": corta(c.get("bodyText"), 1500),
        } for c in (d.get("comments") or {}).get("nodes") or []
            if (c.get("createdAt") or "") >= desde]
        saida.append({
            "numero": d["number"],
            "titulo": d["title"],
            "corpo": corta(d.get("bodyText")),
            "categoria": (d.get("category") or {}).get("name", "?"),
            "autor": login(d.get("author")),
            "criadaEm": d.get("createdAt"),
            "atualizadaEm": d.get("updatedAt"),
            "nova": (d.get("createdAt") or "") >= desde,
            "respondida": bool(d.get("answer")),
            "qtdComentarios": (d.get("comments") or {}).get("totalCount", 0),
            "comentariosNovos": comentarios,
            "url": d["url"],
        })
    return saida


def coletar_commits(repo, desde):
    dados = gh_json("api", f"repos/{repo}/commits?since={desde}&per_page=100", padrao=[])
    if not isinstance(dados, list):
        return []
    return [{
        "sha": c["sha"][:7],
        "mensagem": (c.get("commit", {}).get("message") or "").split("\n")[0],
        "autor": login(c.get("author")) if c.get("author") else
                 c.get("commit", {}).get("author", {}).get("name", "?"),
        "quando": c.get("commit", {}).get("author", {}).get("date"),
        "url": c.get("html_url"),
    } for c in dados]


def coletar_releases(repo, desde):
    dados = gh_json("api", f"repos/{repo}/releases?per_page=10", padrao=[])
    if not isinstance(dados, list):
        return []
    return [{
        "tag": r.get("tag_name"),
        "nome": r.get("name"),
        "notas": corta(r.get("body"), 1500),
        "publicadaEm": r.get("published_at"),
        "url": r.get("html_url"),
    } for r in dados if (r.get("published_at") or "") >= desde]


def coletar_estoque(repo):
    """A foto do acervo: o que esta parado, nao so o que se mexeu hoje."""
    abertas = gh_json("issue", "list", "--repo", repo, "--state", "open", "--limit", "200",
                      "--json", "number,title,createdAt,labels,url")
    prs = gh_json("pr", "list", "--repo", repo, "--state", "open", "--limit", "100",
                  "--json", "number,title,createdAt,isDraft,url")
    disc = gh_json("api", f"repos/{repo}", padrao={})

    def idade(iso):
        try:
            n = datetime.fromisoformat(iso.replace("Z", "+00:00"))
            return (datetime.now(timezone.utc) - n).days
        except Exception:
            return 0

    mais_velhas = sorted(abertas, key=lambda i: i.get("createdAt") or "")[:5]
    return {
        "issuesAbertas": len(abertas),
        "prsAbertos": len(prs),
        "prsRascunho": sum(1 for p in prs if p.get("isDraft")),
        "estrelas": (disc or {}).get("stargazers_count", 0),
        "maisVelhasParadas": [{
            "numero": i["number"], "titulo": i["title"],
            "diasParada": idade(i.get("createdAt") or ""), "url": i["url"],
        } for i in mais_velhas],
        "prsEsperando": [{
            "numero": p["number"], "titulo": p["title"],
            "rascunho": p.get("isDraft", False),
            "diasAberto": idade(p.get("createdAt") or ""), "url": p["url"],
        } for p in prs],
    }


# --------------------------------------------------------------------------- #
# janela e estado
# --------------------------------------------------------------------------- #

def ler_estado(raiz):
    f = raiz / "estado.json"
    if f.exists():
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print("[aviso] estado.json ilegivel; recomecando do zero.", file=sys.stderr)
    return {}


def definir_janela(estado, desde_arg):
    """
    A janela vai do corte da ultima edicao ate agora - assim nenhuma noticia
    cai no vao entre duas edicoes (nem sai repetida).
    Primeira edicao da historia: ultimas 24h.
    """
    agora = datetime.now(timezone.utc).replace(microsecond=0)
    if desde_arg:
        desde = desde_arg
    elif estado.get("ultimoCorte"):
        desde = estado["ultimoCorte"]
    else:
        desde = (agora - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return desde, agora.strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------- #

def main():
    ap = argparse.ArgumentParser(description="Apura a atividade do repo para o Diario da Nitro.")
    ap.add_argument("--repo", default=os.environ.get("JORNAL_REPO", REPO_PADRAO))
    ap.add_argument("--raiz", default=os.environ.get("JORNAL_RAIZ", "Jornal"),
                    help="pasta do jornal (onde vivem estado.json e edicoes/)")
    ap.add_argument("--desde", help="ISO8601 UTC; sobrepoe o corte da ultima edicao")
    ap.add_argument("--saida", help="onde gravar a pauta (padrao: <raiz>/pauta-mais-recente.json)")
    args = ap.parse_args()

    raiz = Path(args.raiz).resolve()
    raiz.mkdir(parents=True, exist_ok=True)

    estado = ler_estado(raiz)
    desde, ate = definir_janela(estado, args.desde)

    print(f"[apuracao] {args.repo}", file=sys.stderr)
    print(f"[apuracao] janela: {desde} -> {ate}", file=sys.stderr)

    pauta = {
        "repo": args.repo,
        "janela": {"desde": desde, "ate": ate},
        "edicaoNumero": int(estado.get("ultimaEdicao", 0)) + 1,
        "geradaEm": datetime.now().astimezone().isoformat(timespec="seconds"),
        "issuesAbertas": coletar_issues_abertas(args.repo, desde),
        "issuesFechadas": coletar_issues_fechadas(args.repo, desde),
        "prsAbertos": coletar_prs(args.repo, desde, "all", "created"),
        "prsMergeados": coletar_prs(args.repo, desde, "merged", "merged"),
        "prsFechadosSemMerge": [p for p in coletar_prs(args.repo, desde, "closed", "closed")
                                if not p.get("mergeadoEm")],
        "discussions": coletar_discussions(args.repo, desde),
        "commits": coletar_commits(args.repo, desde),
        "releases": coletar_releases(args.repo, desde),
        "estoque": coletar_estoque(args.repo),
    }

    pauta["placar"] = {
        "issuesAbertas": len(pauta["issuesAbertas"]),
        "issuesFechadas": len(pauta["issuesFechadas"]),
        "issuesResolvidas": sum(1 for i in pauta["issuesFechadas"] if i["motivo"] == "COMPLETED"),
        "issuesDescartadas": sum(1 for i in pauta["issuesFechadas"] if i["motivo"] != "COMPLETED"),
        "prsAbertos": len(pauta["prsAbertos"]),
        "prsMergeados": len(pauta["prsMergeados"]),
        "prsFechadosSemMerge": len(pauta["prsFechadosSemMerge"]),
        "discussionsNovas": sum(1 for d in pauta["discussions"] if d["nova"]),
        "discussionsMovimentadas": len(pauta["discussions"]),
        "commits": len(pauta["commits"]),
        "releases": len(pauta["releases"]),
        "linhasMais": sum(p["linhas"]["mais"] for p in pauta["prsMergeados"]),
        "linhasMenos": sum(p["linhas"]["menos"] for p in pauta["prsMergeados"]),
        "backlogAberto": pauta["estoque"]["issuesAbertas"],
        "saldoDoDia": len(pauta["issuesFechadas"]) - len(pauta["issuesAbertas"]),
    }
    pauta["diaVazio"] = not any((
        pauta["placar"]["issuesAbertas"], pauta["placar"]["issuesFechadas"],
        pauta["placar"]["prsAbertos"], pauta["placar"]["prsMergeados"],
        pauta["placar"]["discussionsMovimentadas"], pauta["placar"]["commits"],
    ))

    saida = Path(args.saida) if args.saida else raiz / "pauta-mais-recente.json"
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(json.dumps(pauta, ensure_ascii=False, indent=2), encoding="utf-8")

    p = pauta["placar"]
    print(f"""
PAUTA FECHADA -> {saida}
  issues abertas ....... {p['issuesAbertas']}
  issues fechadas ...... {p['issuesFechadas']} ({p['issuesResolvidas']} resolvidas, {p['issuesDescartadas']} descartadas)
  PRs abertos .......... {p['prsAbertos']}
  PRs mergeados ........ {p['prsMergeados']}  (+{p['linhasMais']}/-{p['linhasMenos']})
  discussions ativas ... {p['discussionsMovimentadas']} ({p['discussionsNovas']} novas)
  commits .............. {p['commits']}
  releases ............. {p['releases']}
  backlog aberto ....... {p['backlogAberto']}
  dia vazio? ........... {'SIM' if pauta['diaVazio'] else 'nao'}
""".rstrip())


if __name__ == "__main__":
    main()

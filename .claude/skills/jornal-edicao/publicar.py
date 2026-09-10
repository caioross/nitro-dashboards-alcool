#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
publicar.py - Fecha a edicao do Diario da Nitro.

Confere se a edicao esta publicavel, arquiva a pauta ao lado dela e avanca o
estado (numero da proxima edicao + corte da janela, para a apuracao de amanha
comecar exatamente onde esta parou).

Uso, da raiz do projeto:
    python .claude/skills/jornal-edicao/publicar.py Jornal/edicoes/2026-09-09.html

Ele RECUSA publicar se:
  - sobrou marcador {{ASSIM}} no HTML;
  - o arquivo esta suspeito de vazio;
  - falta o <title> ou o colofao.
Recusa e proposital: edicao com buraco e pior que edicao atrasada.
"""

import argparse
import io
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def falhar(msg):
    print(f"\n  RECUSADO: {msg}\n", file=sys.stderr)
    raise SystemExit(1)


def main():
    ap = argparse.ArgumentParser(description="Fecha e arquiva uma edicao do Diario da Nitro.")
    ap.add_argument("edicao", help="caminho do HTML da edicao")
    ap.add_argument("--raiz", default="Jornal")
    ap.add_argument("--pauta", help="pauta usada (padrao: <raiz>/pauta-mais-recente.json)")
    args = ap.parse_args()

    raiz = Path(args.raiz).resolve()
    edicao = Path(args.edicao).resolve()
    pauta_f = Path(args.pauta).resolve() if args.pauta else raiz / "pauta-mais-recente.json"

    if not edicao.exists():
        falhar(f"nao achei a edicao em {edicao}")

    html = edicao.read_text(encoding="utf-8")

    # --- revisao antes de rodar a impressora ---------------------------------
    sobraram = sorted(set(re.findall(r"\{\{[A-Z_0-9]+\}\}", html)))
    if sobraram:
        falhar("marcadores nao preenchidos no HTML: " + ", ".join(sobraram))
    if len(html) < 3000:
        falhar(f"edicao com apenas {len(html)} caracteres — parece truncada")
    if "<title>" not in html:
        falhar("falta o <title> (e o assunto do e-mail sai dele)")
    if "colofao" not in html:
        falhar("falta o colofao no rodape — o modelo nao foi seguido")

    # --- estado --------------------------------------------------------------
    estado_f = raiz / "estado.json"
    estado = {}
    if estado_f.exists():
        try:
            estado = json.loads(estado_f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print("[aviso] estado.json ilegivel; recriando.", file=sys.stderr)

    numero = int(estado.get("ultimaEdicao", 0)) + 1
    corte = datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    janela = None

    # arquiva a pauta ao lado da edicao: da para reabrir a apuracao meses depois
    if pauta_f.exists():
        try:
            p = json.loads(pauta_f.read_text(encoding="utf-8"))
            numero = int(p.get("edicaoNumero", numero))
            janela = p.get("janela")
            if janela and janela.get("ate"):
                corte = janela["ate"]
        except json.JSONDecodeError:
            print("[aviso] pauta ilegivel; usando contagem do estado.", file=sys.stderr)
        shutil.copyfile(pauta_f, edicao.with_suffix(".pauta.json"))

    estado["ultimaEdicao"] = numero
    estado["ultimoCorte"] = corte
    estado.setdefault("historico", []).append({
        "numero": numero,
        "arquivo": str(edicao.relative_to(raiz.parent)) if raiz.parent in edicao.parents else str(edicao),
        "publicadaEm": datetime.now().astimezone().isoformat(timespec="seconds"),
        "janela": janela,
        "bytes": len(html.encode("utf-8")),
    })
    estado["historico"] = estado["historico"][-400:]  # ~1 ano de edicoes

    estado_f.parent.mkdir(parents=True, exist_ok=True)
    estado_f.write_text(json.dumps(estado, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"""
EDICAO Nº {numero} PUBLICADA
  arquivo ......... {edicao}
  tamanho ......... {len(html.encode('utf-8')) / 1024:.1f} KB
  pauta arquivada . {edicao.with_suffix('.pauta.json').name}
  proximo corte ... {corte}
""".rstrip())


if __name__ == "__main__":
    main()

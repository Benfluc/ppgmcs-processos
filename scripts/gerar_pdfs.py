#!/usr/bin/env python3
"""Gera um PDF para cada processo a partir dos arquivos Markdown em processos/.

A fonte oficial é sempre o arquivo .md. Os PDFs em pdf/ são cópias para impressão
e distribuição e devem ser gerados de novo após cada alteração.

Uso:
    npm install                        # instala o Mermaid (uma vez)
    python3 scripts/gerar_pdfs.py      # gera todos os PDFs
    python3 scripts/gerar_pdfs.py 04   # gera só o processo 04

Requisitos: Python 3.9+, Pandoc, Node.js/npm e Google Chrome ou Chromium.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROC_DIR = ROOT / "processos"
PDF_DIR = ROOT / "pdf"
CSS = ROOT / "scripts" / "estilo-pdf.css"
MERMAID = ROOT / "node_modules" / "mermaid" / "dist" / "mermaid.min.js"

PAGINA = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>{titulo}</title>
<style>{css}
@page {{ @bottom-left {{ content: "PPGMCS/Unimontes · {titulo_curto}"; }}
         @bottom-right {{ content: "Página " counter(page) " de " counter(pages); }} }}
</style></head>
<body>
<header class="topo"><div><div class="inst-1">Universidade Estadual de Montes Claros – Unimontes</div>
<div class="inst-2">Programa de Pós-Graduação em Modelagem Computacional e Sistemas</div></div></header>
{corpo}
<script>{mermaid}</script>
<script>
mermaid.initialize({{ startOnLoad: false, theme: "base", flowchart: {{ htmlLabels: true, curve: "basis", nodeSpacing: 22, rankSpacing: 26, padding: 10, wrappingWidth: 360, useMaxWidth: true }},
  themeVariables: {{ fontFamily: "Inter, DejaVu Sans, sans-serif", fontSize: "14px", lineColor: "#6B7280", edgeLabelBackground: "#FFFFFF" }} }});
mermaid.run({{ querySelector: ".mermaid" }});
</script>
</body></html>"""


def chrome() -> str:
    for c in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        if shutil.which(c):
            return shutil.which(c)
    sys.exit("Chrome/Chromium não encontrado no PATH.")


def md_para_html(md: Path) -> tuple[str, str]:
    corpo = subprocess.run(
        ["pandoc", str(md), "-f", "gfm", "-t", "html5"],
        check=True, capture_output=True, text=True,
    ).stdout
    # Blocos ```mermaid viram <div class="mermaid"> para renderização no navegador.
    corpo = re.sub(
        r'<pre class="mermaid"><code>(.*?)</code></pre>',
        r'<div class="mermaid">\1</div>', corpo, flags=re.S,
    )
    titulo = re.search(r"<h1[^>]*>(.*?)</h1>", corpo, flags=re.S)
    titulo = re.sub(r"<[^>]+>", "", titulo.group(1)) if titulo else md.stem
    return titulo, corpo


def main() -> None:
    if not MERMAID.exists():
        sys.exit("Mermaid não encontrado. Rode `npm install` na raiz do repositório.")
    filtro = sys.argv[1] if len(sys.argv) > 1 else ""
    css = CSS.read_text(encoding="utf-8")
    mermaid_js = MERMAID.read_text(encoding="utf-8")
    PDF_DIR.mkdir(exist_ok=True)
    for md in sorted(PROC_DIR.glob("*.md")):
        if filtro and not md.name.startswith(filtro):
            continue
        titulo, corpo = md_para_html(md)
        html = PAGINA.format(
            titulo=titulo, titulo_curto=titulo.replace('"', "'"), css=css,
            corpo=corpo, mermaid=mermaid_js,
        )
        with tempfile.TemporaryDirectory() as tmp:
            h = Path(tmp) / f"{md.stem}.html"
            h.write_text(html, encoding="utf-8")
            subprocess.run(
                [chrome(), "--headless=new", "--no-sandbox", "--disable-gpu",
                 "--no-pdf-header-footer", "--virtual-time-budget=20000",
                 f"--print-to-pdf={PDF_DIR / (md.stem + '.pdf')}", h.as_uri()],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
        print(f"ok  pdf/{md.stem}.pdf")


if __name__ == "__main__":
    main()

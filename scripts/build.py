#!/usr/bin/env python3
"""Gera fluxogramas (SVG) e PDFs a partir dos arquivos YAML em processos/.

Uso:
    python scripts/build.py            # gera todos
    python scripts/build.py 03         # gera só o processo cujo arquivo começa com 03

Requisitos: Python 3.9+, PyYAML, Jinja2, Graphviz (dot) e Google Chrome/Chromium.
"""
from __future__ import annotations

import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent.parent
PROC_DIR = ROOT / "processos"
FLOW_DIR = ROOT / "fluxogramas"
PDF_DIR = ROOT / "pdf"
TPL_DIR = ROOT / "templates"

# Papéis (atores) e cores usadas no fluxograma e na legenda.
ATORES = {
    "candidato":   ("Candidato(a)",          "#E8F1FB", "#2F6DB5"),
    "discente":    ("Discente",              "#E8F1FB", "#2F6DB5"),
    "orientador":  ("Orientador(a)",         "#E9F6EE", "#2E8B57"),
    "secretaria":  ("Secretaria do PPGMCS",  "#FFF4E0", "#C27C0E"),
    "coordenacao": ("Coordenação",           "#F3ECFA", "#7B4FB0"),
    "colegiado":   ("Colegiado do PPGMCS",   "#F3ECFA", "#7B4FB0"),
    "comissao":    ("Comissão de Seleção",   "#FDECEC", "#B83A3A"),
    "banca":       ("Banca Examinadora",     "#FDECEC", "#B83A3A"),
    "docente":     ("Docente responsável",   "#E9F6EE", "#2E8B57"),
    "prpg":        ("PRPG / Secretaria Geral", "#EEF0F3", "#4A5565"),
}


def md_inline(text: str) -> str:
    """Converte **negrito** e *itálico* simples para HTML, escapando o resto."""
    if text is None:
        return ""
    t = html.escape(str(text))
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    return t


def wrap(text: str, width: int = 26) -> str:
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return lines


def dot_escape(s: str) -> str:
    return html.escape(s, quote=True)


def build_dot(proc: dict) -> str:
    etapas = proc["etapas"]
    out = [
        "digraph G {",
        '  graph [rankdir=TB, splines=ortho, nodesep=0.35, ranksep=0.32, '
        'bgcolor="transparent", fontname="Inter", pad=0.1];',
        '  node  [fontname="Inter", fontsize=10, penwidth=1.3, margin="0.12,0.06"];',
        '  edge  [fontname="Inter", fontsize=9, color="#6B7280", arrowsize=0.7, penwidth=1.1];',
    ]
    for e in etapas:
        ator = e.get("ator", "discente")
        nome, fill, stroke = ATORES[ator]
        tipo = e.get("tipo", "tarefa")
        linhas = wrap(e["texto"], 24 if tipo == "decisao" else 28)
        if tipo == "decisao":
            lbl = "<" + "<BR/>".join(dot_escape(l) for l in linhas) + ">"
            out.append(
                f'  {e["id"]} [shape=diamond, style=filled, fillcolor="{fill}", '
                f'color="{stroke}", label={lbl}, fontsize=9.5];'
            )
        elif tipo in ("inicio", "fim"):
            lbl = "<" + "<BR/>".join(dot_escape(l) for l in linhas) + ">"
            out.append(
                f'  {e["id"]} [shape=box, style="rounded,filled,bold", fillcolor="{stroke}", '
                f'color="{stroke}", fontcolor="white", label={lbl}];'
            )
        else:
            corpo = "<BR/>".join(dot_escape(l) for l in linhas)
            lbl = (
                f'<<FONT POINT-SIZE="8" COLOR="{stroke}"><B>{dot_escape(nome.upper())}</B></FONT>'
                f"<BR/>{corpo}>"
            )
            out.append(
                f'  {e["id"]} [shape=box, style="rounded,filled", fillcolor="{fill}", '
                f'color="{stroke}", label={lbl}];'
            )
    for e in etapas:
        para = e.get("para")
        if not para:
            continue
        if isinstance(para, dict):
            for rotulo, alvo in para.items():
                out.append(f'  {e["id"]} -> {alvo} [xlabel=" {dot_escape(str(rotulo))} ", fontcolor="#374151"];')
        else:
            for alvo in ([para] if isinstance(para, str) else para):
                out.append(f'  {e["id"]} -> {alvo};')
    out.append("}")
    return "\n".join(out)


def render_svg(dot_src: str, dst: Path) -> str:
    dst.with_suffix(".dot").write_text(dot_src, encoding="utf-8")
    subprocess.run(["dot", "-Tsvg", "-o", str(dst), str(dst.with_suffix(".dot"))], check=True)
    svg = dst.read_text(encoding="utf-8")
    svg = svg[svg.index("<svg"):]
    # Remove largura/altura fixas para o SVG escalar no layout.
    # Escala uniforme (1,3x o tamanho natural), limitada pela página via CSS.
    m = re.search(r'<svg width="([\d.]+)pt" height="([\d.]+)pt"', svg)
    if m:
        w, h = float(m.group(1)) * 1.3, float(m.group(2)) * 1.3
        svg = svg.replace(m.group(0), f'<svg style="width:{w:.0f}pt;aspect-ratio:{w:.0f}/{h:.0f}"', 1)
    return svg


def find_chrome() -> str:
    for c in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        p = shutil.which(c)
        if p:
            return p
    sys.exit("Chrome/Chromium não encontrado no PATH.")


def html_to_pdf(html_path: Path, pdf_path: Path) -> None:
    subprocess.run(
        [find_chrome(), "--headless=new", "--no-sandbox", "--disable-gpu",
         "--no-pdf-header-footer", f"--print-to-pdf={pdf_path}", html_path.as_uri()],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def main() -> None:
    filtro = sys.argv[1] if len(sys.argv) > 1 else ""
    meta = yaml.safe_load((PROC_DIR / "_meta.yaml").read_text(encoding="utf-8"))
    env = Environment(loader=FileSystemLoader(TPL_DIR), autoescape=False)
    env.filters["md"] = md_inline
    tpl = env.get_template("processo.html")
    css = (TPL_DIR / "estilo.css").read_text(encoding="utf-8")

    FLOW_DIR.mkdir(exist_ok=True)
    PDF_DIR.mkdir(exist_ok=True)
    arquivos = sorted(p for p in PROC_DIR.glob("*.yaml") if not p.name.startswith("_"))
    for arq in arquivos:
        if filtro and not arq.name.startswith(filtro):
            continue
        proc = yaml.safe_load(arq.read_text(encoding="utf-8"))
        nome = arq.stem
        svg = render_svg(build_dot(proc), FLOW_DIR / f"{nome}.svg")
        atores_usados = []
        for e in proc["etapas"]:
            a = e.get("ator")
            if a and a not in atores_usados and e.get("tipo", "tarefa") not in ("inicio", "fim"):
                atores_usados.append(a)
        legenda = [ATORES[a] for a in atores_usados]
        doc = tpl.render(p=proc, meta=meta, svg=svg, css=css, legenda=legenda, ATORES=ATORES)
        with tempfile.TemporaryDirectory() as tmp:
            h = Path(tmp) / f"{nome}.html"
            h.write_text(doc, encoding="utf-8")
            html_to_pdf(h, PDF_DIR / f"{nome}.pdf")
        print(f"ok  {nome}.pdf")


if __name__ == "__main__":
    main()

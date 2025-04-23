import json
import re
import shutil
import subprocess
from pathlib import Path
from PyPDF2 import PdfMerger
from core.config import (
    DATA_DIR, PDF_DIR, IMAGE_DIR,
    COMPILED_LATEX_DIR, COMPILED_PDF_DIR, WORKSHEET_TITLE, WORKSHEET_AUTHOR
)
from utils.helpers import normalize_image_name
from utils.latex_utils import compile_latex


def generate_toc_tex(toc_tex_path: Path):
    COMPILED_LATEX_DIR.mkdir(parents=True, exist_ok=True)

    latex_content = r"""\documentclass[12pt]{{article}}
\usepackage[a4paper,margin=1in]{{geometry}}
\usepackage{{graphicx}}
\usepackage{{hyperref}}
\usepackage{{pdfpages}}

\title{{{{{title}}}}}
\author{{{{{author}}}}}
\date{{\today}}

\hypersetup{{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,      
    urlcolor=blue,
    pdftitle={{{{{title}}}}},
    pdfauthor={{{{{author}}}}},
    pdfkeywords={{latex, pdf, table of contents}},
    pdfcreator={{LaTeX}},
    pdfproducer={{pdflatex}}
}}

\begin{{document}}

\maketitle
\tableofcontents
\newpage
""".format(title=WORKSHEET_TITLE, author=WORKSHEET_AUTHOR)

    for json_file in sorted(DATA_DIR.glob("*.json")):
        figure_id = json_file.stem
        pdf_file = PDF_DIR / f"{figure_id}.pdf"
        image_file = IMAGE_DIR / normalize_image_name(figure_id)

        if not pdf_file.exists() or not image_file.exists():
            continue

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            name = data.get("name", figure_id)

        latex_content += f"""
\\phantomsection
\\hypertarget{{{figure_id}}}{{}}  % Anchor
\\addcontentsline{{toc}}{{section}}{{{name}}}
\\includepdf[pages=-]{{{pdf_file.as_posix()}}}
\\newpage
"""

    latex_content += r"\end{document}"
    toc_tex_path.write_text(latex_content, encoding="utf-8")

def merge_pdfs(with_toc=False, output_name="historical_figures.pdf"):
    COMPILED_PDF_DIR.mkdir(parents=True, exist_ok=True)
    COMPILED_LATEX_DIR.mkdir(parents=True, exist_ok=True)

    # Modify output name if TOC mode and default name is used
    if with_toc and output_name == "historical_figures.pdf":
        output_name = "historical_figures_with_toc.pdf"

    output_path = COMPILED_PDF_DIR / output_name

    if with_toc:
        tex_path = COMPILED_LATEX_DIR / output_name.replace(".pdf", ".tex")
        generate_toc_tex(tex_path)
        if compile_latex(tex_path, output_path):
            print(f"[✓] PDF with TOC created: {output_path}")
        else:
            print("[!] Failed to build TOC-based PDF.")
        return

    # Otherwise: flat merge
    from PyPDF2 import PdfMerger
    merger = PdfMerger()

    for pdf in sorted(PDF_DIR.glob("*.pdf")):
        if pdf.name.startswith("historical_figures") or pdf.name == output_name:
            continue
        merger.append(str(pdf))

    merger.write(str(output_path))
    merger.close()
    print(f"[✓] Flat merged PDF saved to: {output_path}")
import os
import json
import subprocess
from pathlib import Path
import re
import shutil

# --- Config ---
DATA_DIR = Path("data")
LATEX_DIR = Path("output/latex")
PDF_DIR = Path("output/pdf")
IMAGE_DIR = Path("images")
MASTER_LATEX_PATH = Path("output/latex/historical_figures_toc.tex")
FINAL_PDF_PATH = Path("output/historical_figures_toc.pdf")  # Specify the final PDF output path

# --- Helper function to normalize figure names ---
def normalize_image_name(figure_id: str) -> str:
    # Remove anything in brackets (e.g. "(something)")
    cleaned = re.sub(r"\(.*?\)", "", figure_id)
    # Remove anything after an en dash or em dash
    cleaned = re.split(r"–|—", cleaned)[0]
    # Remove trailing hyphens or whitespace
    cleaned = cleaned.strip("- ").replace("_", "-")
    # Collapse double hyphens if any
    cleaned = re.sub(r"-{2,}", "-", cleaned)
    return cleaned + ".jpg"

# --- LaTeX content structure ---
latex_content = """
\\documentclass[12pt]{article}
\\usepackage[a4paper,margin=1in]{geometry}
\\usepackage{graphicx}
\\usepackage{hyperref}
\\usepackage{pdfpages}

\\title{Historical Figures}
\\author{Bridges Homeschool Academy}
\\date{\\today}

\\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,      
    urlcolor=blue,
    pdftitle={Historical Figures},
    pdfauthor={Bridges Homeschool Academy},
    pdfkeywords={latex, pdf, table of contents},
    pdfcreator={LaTeX},
    pdfproducer={pdflatex}
}

\\begin{document}

\\maketitle

% Table of contents
\\tableofcontents
\\newpage
"""

# Initialize list for missing files
missing_files = []

# --- Iterate through each JSON file and generate LaTeX content ---
for json_file in sorted(DATA_DIR.glob("*.json")):
    figure_id = json_file.stem
    image_name = normalize_image_name(figure_id)
    image_path = IMAGE_DIR / image_name
    tex_path = LATEX_DIR / f"{figure_id}.tex"
    compiled_pdf = PDF_DIR / f"{figure_id}.pdf"

    if not image_path.exists() or not compiled_pdf.exists():
        print(f"[!] Skipping {figure_id}: Missing image or PDF")
        missing_files.append(figure_id)
        continue

    # Extract name from the JSON
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        name = data.get("name", "Unknown Name")  # Fallback to "Unknown Name" if no name is found

    # Add phantom section before the PDF to create a linkable anchor and add it to the ToC
    latex_content += f"""
\\phantomsection
\\hypertarget{{{figure_id}}}{{}}  % Invisible target for link
\\addcontentsline{{toc}}{{section}}{{{name}}}
\\includepdf[pages=-,link=true]{{{compiled_pdf.as_posix()}}}
\\newpage
"""

# --- Finalize LaTeX document ---
latex_content += """
\\end{document}
"""

# --- Write combined LaTeX document ---
LATEX_DIR.mkdir(parents=True, exist_ok=True)
MASTER_LATEX_PATH.write_text(latex_content, encoding="utf-8")
print(f"Master LaTeX document written to: {MASTER_LATEX_PATH}")

# --- Compile the LaTeX document using lualatex ---
try:
    subprocess.run(
        ["lualatex", "-interaction=nonstopmode", "-output-directory", str(LATEX_DIR), str(MASTER_LATEX_PATH)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print("[✓] PDF generated.")
    # Move the compiled PDF to the final destination
    if (LATEX_DIR / f"historical_figures_toc.pdf").exists():
        shutil.move(str(LATEX_DIR / "historical_figures_toc.pdf"), str(FINAL_PDF_PATH))
        print(f"[✓] Combined PDF moved to: {FINAL_PDF_PATH}")
    else:
        print(f"[!] Compilation succeeded but PDF not found: {LATEX_DIR / 'historical_figures_toc.pdf'}")
except subprocess.CalledProcessError as e:
    print(f"[!] Error during LaTeX compilation: {e.stderr.decode()}")

# --- Output the list of missing files ---
if missing_files:
    print("\n[✘] Missing images or PDFs for the following figures:")
    for missing in missing_files:
        print(f"- {missing}")
else:
    print("\n[✓] All images and PDFs found and processed successfully.")

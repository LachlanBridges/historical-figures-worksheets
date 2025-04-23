from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Worksheet title and author
WORKSHEET_TITLE = os.getenv("WORKSHEET_TITLE", "Historical Figures")
WORKSHEET_AUTHOR = os.getenv("WORKSHEET_AUTHOR", "Bridges Homeschool Academy")

# Base folders
TEMPLATE_DIR = Path("templates")
DATA_DIR = Path("data")
IMAGE_DIR = Path("images")
LATEX_DIR = Path("output/latex")
PDF_DIR = Path("output/pdf")

# Structured output for compiled variants (e.g. TOC, solutions)
COMPILED_LATEX_DIR = LATEX_DIR / "compiled"
COMPILED_PDF_DIR = PDF_DIR / "compiled"

# Make sure these directories exist
COMPILED_LATEX_DIR.mkdir(parents=True, exist_ok=True)
COMPILED_PDF_DIR.mkdir(parents=True, exist_ok=True)

# Template & control files
TEMPLATE_NAME = "worksheet.tex.j2"
FIGURES_FILE = Path("figures.txt")

# Example output files
MERGED_PDF_FILE = PDF_DIR / "historical_figures.pdf"  # simple merge
# For compiled variants, define filenames in the script (e.g. with_toc.pdf)

# Wikipedia config
WIKI_EMAIL = os.getenv("WIKI_EMAIL_ADDRESS", "no-email@example.com")
WIKI_USER_AGENT = f"historical-figures-script/1.0 ({WIKI_EMAIL})"

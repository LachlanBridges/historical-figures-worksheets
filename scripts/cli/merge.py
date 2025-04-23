import argparse
from core.merger import merge_pdfs

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--with-toc", action="store_true", help="Include table of contents in merged PDF")
    parser.add_argument("--filename", type=str, default="historical_figures.pdf", help="Output PDF name")
    args = parser.parse_args()

    merge_pdfs(with_toc=args.with_toc, output_name=args.filename)

from pathlib import Path
from PyPDF2 import PdfMerger

INPUT_DIR = Path("output/pdf")
OUTPUT_FILE = Path("output/historical_figures.pdf")

def merge_pdfs():
    merger = PdfMerger()
    pdf_files = sorted(INPUT_DIR.glob("*.pdf"))

    if not pdf_files:
        print("[!] No PDF files found to merge.")
        return

    for pdf in pdf_files:
        print(f"[+] Adding: {pdf.name}")
        merger.append(str(pdf))

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    merger.write(str(OUTPUT_FILE))
    merger.close()
    print(f"[✓] Combined PDF saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    merge_pdfs()

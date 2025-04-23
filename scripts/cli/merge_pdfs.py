from pathlib import Path
from PyPDF2 import PdfMerger

from core.config import PDF_DIR, MERGED_PDF_FILE

def merge_pdfs():
    merger = PdfMerger()
    pdf_files = sorted(PDF_DIR.glob("*.pdf"))

    if not pdf_files:
        print("[!] No PDF files found to merge.")
        return

    for pdf in pdf_files:
        print(f"[+] Adding: {pdf.name}")
        merger.append(str(pdf))

    MERGED_PDF_FILE.parent.mkdir(parents=True, exist_ok=True)
    merger.write(str(MERGED_PDF_FILE))
    merger.close()
    print(f"[✓] Combined PDF saved to: {MERGED_PDF_FILE}")
    
def run():
    merge_pdfs()
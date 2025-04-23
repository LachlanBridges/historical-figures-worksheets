from pathlib import Path

from core.config import FIGURES_FILE

def sort_figures():
    if not FIGURES_FILE.exists():
        print(f"[!] {FIGURES_FILE} not found.")
        return

    with open(FIGURES_FILE, "r", encoding="utf-8") as f:
        names = [line.strip() for line in f if line.strip()]

    names.sort(key=lambda name: name.lower())

    with open(FIGURES_FILE, "w", encoding="utf-8") as f:
        for name in names:
            f.write(name + "\n")

    print(f"[✓] Sorted {len(names)} names in {FIGURES_FILE}")

def run():
    sort_figures()

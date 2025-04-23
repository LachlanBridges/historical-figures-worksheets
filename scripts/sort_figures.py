from pathlib import Path

FIGURES_FILE = Path("figures.txt")

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

if __name__ == "__main__":
    sort_figures()

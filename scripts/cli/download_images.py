import argparse
from core.downloader import download_images_from_list
from core.config import FIGURES_FILE

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, help="Text file with figure names (one per line)")
    args = parser.parse_args()

    if args.file:
        path = FIGURES_FILE if args.file == "figures.txt" else args.file
        with open(path, "r", encoding="utf-8") as f:
            names = [line.strip() for line in f if line.strip()]
    else:
        print("[!] Please provide --file with figure names.")
        return

    missing = download_images_from_list(names)

    if missing:
        print("\n[✘] Missing images for the following figures:")
        for name in missing:
            print(f"- {name}")
    else:
        print("\n[✓] All images downloaded successfully.")

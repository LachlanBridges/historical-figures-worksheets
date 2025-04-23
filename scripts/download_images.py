import os
import requests
import wikipediaapi
from pathlib import Path

FIGURE_LIST = Path("figures.txt")
OUTPUT_DIR = Path("images")
OUTPUT_DIR.mkdir(exist_ok=True)

wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="historical-figures-script/1.0 (lachlanjbridges@gmail.com)"
)
def slugify(name):
    return name.strip().lower().replace(" ", "-")

def get_image_url(title):
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "titles": title,
        "pithumbsize": 600,  # pixel width
        "redirects": 1        # FOLLOW REDIRECTS!
    }

    print(f"Fetching image for: {title}")
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    pages = DATA.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        if "thumbnail" in page:
            return page["thumbnail"]["source"]
    
    print(f"[!] No thumbnail found for: {title}")
    return None


def download_image(url, output_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://en.wikipedia.org/",
        "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"[✓] Saved image: {output_path}")
    except Exception as e:
        print(f"[!] Failed to download from: {url}")
        print(f"    Reason: {e}")

def main():
    if not FIGURE_LIST.exists():
        print(f"[!] {FIGURE_LIST} not found.")
        return

    with open(FIGURE_LIST, "r", encoding="utf-8") as f:
        names = [line.strip() for line in f if line.strip()]

    missing = []

    for name in names:
        filename = f"{slugify(name)}.jpg"
        output_path = OUTPUT_DIR / filename

        if output_path.exists():
            print(f"[→] Skipping {name}, already exists.")
            continue

        print(f"[*] Searching for: {name}")
        page = wiki.page(name)
        if not page.exists():
            print(f"[!] Wikipedia page not found for: {name}")
            missing.append(name)
            continue

        img_url = get_image_url(name)
        if not img_url:
            print(f"[!] No image found for: {name}")
            missing.append(name)
            continue

        download_image(img_url, output_path)

    if missing:
        print("\n[✘] Missing images for the following figures:")
        for name in missing:
            print(f"- {name}")
    else:
        print("\n[✓] All images downloaded successfully.")


if __name__ == "__main__":
    main()

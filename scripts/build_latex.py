import os
import json
import argparse
from jinja2 import Environment, FileSystemLoader
import subprocess
from pathlib import Path
import shutil
import re

# --- Config ---
TEMPLATE_DIR = Path("templates")
DATA_DIR = Path("data")
LATEX_DIR = Path("output/latex")
PDF_DIR = Path("output/pdf")
IMAGE_DIR = Path("images")
TEMPLATE_NAME = "worksheet.tex.j2"

# --- Jinja2 setup ---
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=False)
template = env.get_template(TEMPLATE_NAME)

skipped_due_to_missing_image = []

def sort_questions(questions):
    def total_length(q):
        # Max length among question and its options
        return max([len(q["q"])] + [len(opt) for opt in q.get("options", [])])
    
    sorted_qs = sorted(questions, key=total_length)
    return sorted_qs[:2] + sorted_qs[2:]

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

def build_latex(json_path: Path, render: bool = True, force: bool = False):
    figure_id = json_path.stem
    image_name = normalize_image_name(figure_id)
    image_path = IMAGE_DIR / image_name
    tex_path = LATEX_DIR / f"{figure_id}.tex"
    compiled_pdf = LATEX_DIR / f"{figure_id}.pdf"
    final_pdf = PDF_DIR / f"{figure_id}.pdf"

    if not image_path.exists():
        print(f"[→] Skipping {figure_id}: missing image {image_path}")
        skipped_due_to_missing_image.append(figure_id)
        return

    if final_pdf.exists() and not force:
        print(f"[→] Skipping {figure_id}: PDF already exists.")
        return

    if render:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            data["image"] = image_name
            if "questions" in data:
                data["questions"] = sort_questions(data["questions"])

        rendered = template.render(**data)
        LATEX_DIR.mkdir(parents=True, exist_ok=True)
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        print(f"[+] LaTeX file written: {tex_path}")
    else:
        if not tex_path.exists():
            print(f"[!] Cannot compile: {tex_path} does not exist.")
            return

    PDF_DIR.mkdir(parents=True, exist_ok=True)

    try:
        subprocess.run(
            ["lualatex", "-interaction=nonstopmode", "-output-directory", str(LATEX_DIR), str(tex_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )
        if compiled_pdf.exists():
            shutil.move(str(compiled_pdf), str(final_pdf))
            print(f"[✓] PDF moved to: {final_pdf}")
        else:
            print(f"[!] Compilation succeeded but PDF not found: {compiled_pdf}")
    except subprocess.CalledProcessError:
        print(f"[!] Failed to compile {tex_path}")

def build_all(render: bool = True, force: bool = False):
    json_files = sorted(DATA_DIR.glob("*.json"))
    for json_path in json_files:
        build_latex(json_path, render=render, force=force)

    if skipped_due_to_missing_image:
        print("\n--- Skipped due to missing image ---")
        for name in skipped_due_to_missing_image:
            print(f"- {name}")
        print(f"Total skipped: {len(skipped_due_to_missing_image)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path", type=Path, nargs="?", help="Path to a specific JSON file")
    parser.add_argument("--no-render", action="store_true", help="Compile existing .tex without regenerating it")
    parser.add_argument("--force", action="store_true", help="Rebuild even if PDF already exists")
    parser.add_argument("--all", action="store_true", help="Process all .json files in the data/ folder")
    args = parser.parse_args()

    if args.all:
        build_all(render=not args.no_render, force=args.force)
    elif args.json_path:
        build_latex(args.json_path, render=not args.no_render, force=args.force)
    else:
        print("Usage:\n  build_latex.py <file.json>\n  build_latex.py --all\n  build_latex.py --all --no-render [--force]")

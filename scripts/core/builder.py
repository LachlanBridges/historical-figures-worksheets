import json
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from core.config import IMAGE_DIR, LATEX_DIR, PDF_DIR, TEMPLATE_DIR, TEMPLATE_NAME, DATA_DIR
from utils.latex_utils import compile_latex
from utils.helpers import normalize_image_name, sort_questions

# Setup Jinja2 environment
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=False)
template = env.get_template(TEMPLATE_NAME)

skipped_due_to_missing_image = []

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

    if compile_latex(tex_path, compiled_pdf):
        shutil.move(str(compiled_pdf), str(final_pdf))
        print(f"[✓] PDF moved to: {final_pdf}")
    else:
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

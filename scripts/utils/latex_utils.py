import subprocess
import shutil
from pathlib import Path

def compile_latex(tex_path: Path, output_pdf_path: Path, passes: int = 2) -> bool:
    compiled_pdf = tex_path.with_suffix(".pdf")

    try:
        for i in range(passes):
            subprocess.run(
                ["lualatex", "-interaction=nonstopmode", "-output-directory", str(tex_path.parent), str(tex_path)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        if compiled_pdf.exists():
            shutil.move(str(compiled_pdf), str(output_pdf_path))
            return True
        else:
            print(f"[!] LaTeX ran but did not produce: {compiled_pdf}")
    except subprocess.CalledProcessError:
        print(f"[!] Failed to compile LaTeX: {tex_path}")
    return False

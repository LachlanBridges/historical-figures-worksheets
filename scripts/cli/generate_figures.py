import argparse
from pathlib import Path
from core.generator import already_exists, load_random_examples, prompt_user_with_tempfile, write_json

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("people", nargs="*", help="Names of figures to generate")
    parser.add_argument("--file", type=Path, help="Text file with names (newline-separated)")
    parser.add_argument("--batch-size", type=int, default=5, help="How many figures per batch")
    args = parser.parse_args()

    names = []
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            names.extend([line.strip() for line in f if line.strip()])
    if args.people:
        names.extend(args.people)

    names = [name for name in names if not already_exists(name)]
    if not names:
        print("[✓] All figures already exist. Nothing to do.")
        return

    for i in range(0, len(names), args.batch_size):
        batch = names[i:i + args.batch_size]
        print(f"\n[→] Processing batch: {', '.join(batch)}")
        examples = load_random_examples(skip_names=batch)
        result = prompt_user_with_tempfile(batch, examples)
        if result:
            write_json(result)

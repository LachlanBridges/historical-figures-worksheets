import os
import json
import argparse
import subprocess
import tempfile
from pathlib import Path
from random import sample
from textwrap import dedent

DATA_DIR = Path("data")  # <- CHANGE HERE if needed
DATA_DIR.mkdir(parents=True, exist_ok=True)

def normalize_filename(name):
    return name.lower().replace(" ", "-").replace("'", "")

def already_exists(name):
    filename = normalize_filename(name) + ".json"
    return (DATA_DIR / filename).exists()

def load_random_examples(skip_names, max_examples=2):
    files = [f for f in DATA_DIR.glob("*.json")]
    examples = []
    for f in files:
        with open(f, "r", encoding="utf-8") as jf:
            try:
                obj = json.load(jf)
                if isinstance(obj, dict):
                    obj = [obj]
                for entry in obj:
                    if entry["name"] not in skip_names:
                        examples.append(entry)
            except Exception:
                continue
    return sample(examples, k=min(len(examples), max_examples))


def write_json(data):
    for person in data:
        filename = normalize_filename(person["name"]) + ".json"
        outpath = DATA_DIR / filename
        with open(outpath, "w", encoding="utf-8") as f:
            json.dump(person, f, indent=2, ensure_ascii=False)
        print(f"[✓] Saved: {outpath}")


def prompt_user_with_tempfile(batch, example_data):
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt", encoding="utf-8") as tf:
        # Prompt
        tf.write("You are helping generate educational profile data for children aged 6–9.\n")
        tf.write("Use this format:\n\n")

        # Examples
        tf.write("```json\n[\n")
        for i, ex in enumerate(example_data):
            json.dump(ex, tf, indent=2, ensure_ascii=False)
            if i < len(example_data) - 1:
                tf.write(",\n")
            else:
                tf.write("\n")
        tf.write("]\n```\n\n")

        tf.write("Now generate entries for the following figures:\n\n")
        for name in batch:
            tf.write(f"- {name}\n")
        tf.write("\nPaste the resulting JSON array below:\n\n")
        tf.flush()

        subprocess.run(["notepad", tf.name])
        tf.seek(0)
        lines = tf.read()

    try:
        json_start = lines.index("[")
        json_data = json.loads(lines[json_start:])
        return json_data
    except Exception as e:
        print("[!] Failed to parse JSON. Skipping this batch.")
        print("Error:", e)
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("people", nargs="*", help="Names of figures to generate")
    parser.add_argument("--file", type=Path, help="Text file with names (newline-separated)")
    parser.add_argument("--batch-size", type=int, default=5, help="How many figures per prompt batch")
    args = parser.parse_args()

    # Load names
    names = []
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            names.extend([line.strip() for line in f if line.strip()])
    if args.people:
        names.extend(args.people)

    # Filter already-generated
    names = [name for name in names if not already_exists(name)]
    if not names:
        print("[✓] All figures already exist. Nothing to do.")
        return

    # Process batches
    for i in range(0, len(names), args.batch_size):
        batch = names[i:i + args.batch_size]
        print(f"\n[→] Processing batch: {', '.join(batch)}")
        examples = load_random_examples(skip_names=batch)
        result = prompt_user_with_tempfile(batch, examples)
        if result:
            write_json(result)


if __name__ == "__main__":
    main()

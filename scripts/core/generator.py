import json
import tempfile
import subprocess
from pathlib import Path
from random import sample
from core.config import DATA_DIR
from utils.helpers import normalize_filename

DATA_DIR.mkdir(parents=True, exist_ok=True)

def already_exists(name):
    filename = normalize_filename(name) + ".json"
    return (DATA_DIR / filename).exists()

def load_random_examples(skip_names, max_examples=2):
    examples = []
    for f in DATA_DIR.glob("*.json"):
        try:
            with open(f, "r", encoding="utf-8") as jf:
                obj = json.load(jf)
                if isinstance(obj, dict):
                    obj = [obj]
                for entry in obj:
                    if entry.get("name") not in skip_names:
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
        tf.write("You are helping generate educational profile data for children aged 6–9.\n")
        tf.write("Use this format:\n\n")

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

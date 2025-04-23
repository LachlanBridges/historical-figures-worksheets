import re

# --- Helper function to normalize figure names ---
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

def normalize_filename(name):
    return name.lower().replace(" ", "-").replace("'", "")


def sort_questions(questions):
    def total_length(q):
        # Max length among question and its options
        return max([len(q["q"])] + [len(opt) for opt in q.get("options", [])])
    
    sorted_qs = sorted(questions, key=total_length)
    return sorted_qs[:2] + sorted_qs[2:]


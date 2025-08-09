import re
import random

def remove_extra_spaces(text: str) -> int:
    normalized = re.sub(r'\s+', ' ', text).strip()
    return normalized

def generate_random_color() -> str:
    """Generate a random hex color code."""
    return '#{:06x}'.format(random.randint(0, 0xFFFFFF))
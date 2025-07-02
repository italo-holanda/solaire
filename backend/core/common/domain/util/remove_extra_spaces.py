import re

def remove_extra_spaces(text: str) -> int:
    normalized = re.sub(r'\s+', ' ', text).strip()
    return normalized
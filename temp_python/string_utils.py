import re


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def snake_to_camel(name: str) -> str:
    return "".join(part.capitalize() or "_" for part in name.split("_"))

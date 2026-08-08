import re


def extract_markdown_images(text: str) -> list[(str, str)]:
    reg = r"!\[([^\]]+)\]\(([^\)]+)\)"
    matches = re.findall(reg, text)
    return matches

def extract_markdown_links(text: str) -> list[(str, str)]:
    reg = r"(?<!!)\[([^\]]+)\]\(([^\)]+)\)"
    matches = re.findall(reg, text)

    return matches
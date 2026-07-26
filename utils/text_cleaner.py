import re

def remove_linebreak_text(text: str) -> str:
    """Remove quebras de linha e múltiplos espaços de um texto."""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def remove_emojis_text(text: str) -> str:
    """Remove emojis de um texto preservando caracteres acentuados da língua portuguesa."""
    if not text:
        return ""
    emoji_pattern = re.compile(
        r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\u2600-\u27bf\U0001F900-\U0001F9FF\U0001FA70-\U0001FAFF]+'
    )
    return emoji_pattern.sub("", text).strip()

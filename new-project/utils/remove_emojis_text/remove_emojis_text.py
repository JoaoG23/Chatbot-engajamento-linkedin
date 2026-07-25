import emoji

def remove_emojis_text(text: str) -> str:
    """Remove emojis do texto fornecido."""
    if not text:
        return ""
    return emoji.replace_emoji(str(text), replace="")

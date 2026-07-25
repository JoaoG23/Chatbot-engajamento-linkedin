def remove_linebreak_text(text: str) -> str:
    """Remove quebras de linha do texto fornecido."""
    if not text:
        return ""
    return text.replace("\n", "")

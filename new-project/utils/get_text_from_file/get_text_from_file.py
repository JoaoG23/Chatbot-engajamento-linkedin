def get_text_from_file(file_path: str) -> str:
    """Lê e retorna o conteúdo de um arquivo de texto."""
    if not file_path:
        return ""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

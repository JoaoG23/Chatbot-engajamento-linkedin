import os
import json
import hashlib
from config import HISTORY_FILE
from utils.text_cleaner import remove_linebreak_text


def load_history() -> set:
    """Carrega o histórico de postagens comentadas."""
    if not os.path.exists(HISTORY_FILE):
        return set()

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as history_file_stream:
            return set(json.load(history_file_stream))
    except Exception:
        return set()


def save_history(history_set: set) -> None:
    """Salva o conjunto de hashes no arquivo JSON de histórico."""
    history_directory = os.path.dirname(HISTORY_FILE)
    if history_directory:
        os.makedirs(history_directory, exist_ok=True)

    with open(HISTORY_FILE, "w", encoding="utf-8") as history_file_stream:
        json.dump(list(history_set), history_file_stream, ensure_ascii=False, indent=2)


def get_post_hash(text: str) -> str:
    """Gera um hash MD5 a partir dos primeiros 200 caracteres do texto limpo do post."""
    if not text:
        return ""

    cleaned_post_text = remove_linebreak_text(text)[:200]
    return hashlib.md5(cleaned_post_text.encode("utf-8")).hexdigest()

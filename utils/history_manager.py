import os
import json
import hashlib
from config import HISTORY_FILE
from utils.text_cleaner import remove_linebreak_text

def load_history() -> set:
    """Carrega o histórico de postagens comentadas."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_history(history_set: set) -> None:
    """Salva o conjunto de hashes no arquivo JSON de histórico."""
    folder = os.path.dirname(HISTORY_FILE)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(list(history_set), f, ensure_ascii=False, indent=2)

def get_post_hash(text: str) -> str:
    """Gera um hash MD5 a partir do texto limpo do post."""
    clean = remove_linebreak_text(text)[:200]
    return hashlib.md5(clean.encode('utf-8')).hexdigest()

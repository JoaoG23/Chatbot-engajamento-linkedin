import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL", "")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD", "")
CDP_URL = os.getenv("CDP_URL", "http://127.0.0.1:9222")
HISTORY_FILE = os.getenv("HISTORY_FILE", os.path.join("data", "commented_posts_history.json"))
PROMPT_FILE = os.getenv("PROMPT_FILE", os.path.join("data", "persona.txt"))
EXAMPLES_FILE = os.getenv("EXAMPLES_FILE", os.path.join("data", "exemplares.txt"))
LINKEDIN_HOME_URL = "https://www.linkedin.com/home"
LINKEDIN_FEED_URL = "https://www.linkedin.com/feed/"
LIMIT_COMMENTS = int(os.getenv("LIMIT_COMMENTS", 25))

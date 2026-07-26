import os
from dotenv import load_dotenv

load_dotenv()

AI_TOKEN = os.getenv("AI_TOKEN", "AIzaSyB6PeCgkJxnk7TQ6_-FUF2AhjTbZrwdReQ")
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL", "")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD", "")
CDP_URL = os.getenv("CDP_URL", "http://127.0.0.1:9222")
HISTORY_FILE = os.getenv("HISTORY_FILE", "commented_posts_history.json")
PROMPT_FILE = os.getenv("PROMPT_FILE", "prompt.txt")
LINKEDIN_HOME_URL = "https://www.linkedin.com/home"
LINKEDIN_FEED_URL = "https://www.linkedin.com/feed/"
LIMIT_COMMENTS = int(os.getenv("LIMIT_COMMENTS", 25))

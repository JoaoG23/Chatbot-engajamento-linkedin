import os

from google import genai
from google.genai import types

from utils.get_text_from_file.get_text_from_file import get_text_from_file
from utils.remove_emojis_text.remove_emojis_text import remove_emojis_text
from utils.remove_linebreak_text.remove_linebreak_text import remove_linebreak_text
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def create_comment_based_post(content_post):

    prompt = get_text_from_file("templates/prompt.txt")
    prompt_without_linebreak = remove_linebreak_text(prompt)

    token = os.getenv("AI_TOKEN")
    client = genai.Client(api_key=token)

    full_prompt = f"{prompt_without_linebreak}\n\nPostagem: (({content_post}))"

    models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]

    for model in models:
        try:
            print(f"[create_comment_based_post] Tentando chamada com o modelo: {model}...")
            response = client.models.generate_content(
                model=model,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    top_p=0.8,
                    top_k=10,
                    stop_sequences=["Title"],
                ),
            )

            generated_text = response.text
            text_without_linebreak = remove_linebreak_text(generated_text)
            text_without_emojis = remove_emojis_text(text_without_linebreak)
            return text_without_emojis

        except Exception as e:
            print(f"[create_comment_based_post] Falha com o modelo {model}: {e}")
            if model == models[-1]:
                raise e

    return None

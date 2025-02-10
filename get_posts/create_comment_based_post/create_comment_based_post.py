import json
import os
import requests

from utils.get_text_from_file.get_text_from_file import get_text_from_file
from utils.remove_emojis_text.remove_emojis_text import remove_emojis_text
from utils.remove_linebreak_text.remove_linebreak_text import remove_linebreak_text


def create_comment_based_post(content_post):
    
    prompt = get_text_from_file('templates/prompt.txt')
    prompt_without_linebreak = remove_linebreak_text(prompt)
    
    token = os.getenv("AI_TOKEN")
    URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={token}"  # URL corrigida
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [
            {
                "role": "assistant",
                "parts": [
                    {
                        "text": f"{prompt_without_linebreak}"
                    }
                ]
            },
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"Postagem: (({content_post}))"
                    }
                ]
            }
        ],
        "generation_config": {
            # "candidate_count": 1,
            "temperature": 0.9
        }
    }
    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()  # Lança exceção para status 4xx/5xx
        
        if response.status_code == 200:
            response_json = response.json()
            generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
            text_without_linebreak = remove_linebreak_text(generated_text)
            text_without_emojis = remove_emojis_text(text_without_linebreak)
            return text_without_emojis
        return None
            
    except requests.exceptions.RequestException as e:
        raise e
    except json.JSONDecodeError as e:
        raise e
    
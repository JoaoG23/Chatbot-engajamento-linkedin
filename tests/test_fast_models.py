import time
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from google import genai
from google.genai import types
from config import AI_TOKEN

def test_fast_models():
    client = genai.Client(api_key=AI_TOKEN)
    
    # Official stable low-latency models
    models = [
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
    ]
    
    prompt = "Postagem: ((10 Dicas Simples para APPs consistentes no Ecossistema React.js e TypeScript))"
    
    for model in models:
        t0 = time.time()
        try:
            print(f"Testando modelo: {model}...")
            res = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=100
                )
            )
            elapsed = time.time() - t0
            print(f"[OK] {model} respondeu em {elapsed:.2f}s: '{res.text.strip()}'")
            break
        except Exception as e:
            elapsed = time.time() - t0
            print(f"[ERRO] {model} falhou em {elapsed:.2f}s: {e}")

if __name__ == "__main__":
    test_fast_models()

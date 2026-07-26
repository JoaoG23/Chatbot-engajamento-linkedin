import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from google import genai
from google.genai import types
from config import AI_TOKEN

def test_models():
    client = genai.Client(api_key=AI_TOKEN)
    
    candidates = [
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.1-flash-live",
        "gemini-3.1-flash",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite"
    ]
    
    prompt = "Responda apenas: OK"
    
    print("=================== TESTANDO DISPONIBILIDADE DOS MODELOS ===================")
    for model in candidates:
        t0 = time.time()
        try:
            res = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(max_output_tokens=10)
            )
            elapsed = time.time() - t0
            print(f"✅ {model} [FUNCIONANDO] - Tempo: {elapsed:.2f}s | Resposta: {res.text.strip()}")
        except Exception as e:
            elapsed = time.time() - t0
            err_msg = str(e)
            if "404" in err_msg:
                print(f"❌ {model} [NÃO EXISTE / 404] - {err_msg[:100]}...")
            elif "429" in err_msg:
                print(f"⚠️ {model} [LIMITE DE COTA / 429] - Cota diária/minuto atingida.")
            elif "503" in err_msg:
                print(f"⚠️ {model} [INDISPONÍVEL / 503] - Alta demanda temporária.")
            else:
                print(f"❌ {model} [ERRO] - {err_msg[:100]}...")

if __name__ == "__main__":
    test_models()

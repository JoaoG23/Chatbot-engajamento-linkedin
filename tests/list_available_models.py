import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from google import genai
from config import AI_TOKEN

def list_all_models():
    client = genai.Client(api_key=AI_TOKEN)
    print("=================== MODELOS DISPONÍVEIS NA SUA API KEY ===================")
    try:
        models = client.models.list()
        for m in models:
            name = getattr(m, 'name', str(m))
            print(f"- {name}")
    except Exception as e:
        print(f"Erro ao listar modelos: {e}")

if __name__ == "__main__":
    list_all_models()

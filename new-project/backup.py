import asyncio
import os
from pathlib import Path
from typing import List
from pydantic import BaseModel, Field
from playwright.async_api import async_playwright
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Carrega o .env da pasta raiz do projeto
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
GEMINI_API_KEY = os.getenv("AI_TOKEN")

# 1. Definição do esquema de dados desejado usando Pydantic
class Citacao(BaseModel):
    frase: str = Field(description="A frase ou citação encontrada na página")
    autor: str = Field(description="O nome do autor da frase")
    tags: List[str] = Field(description="Lista de tags ou categorias associadas")

class ListaCitacoes(BaseModel):
    citacoes: List[Citacao]

async def extrair_dados_com_ia(url: str, prompt_usuario: str):
    # 2. Captura do conteúdo dinâmico via Playwright
    async with async_playwright() as p:
        # Lança o navegador em modo background
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print(f"Acessando: {url}...")
        await page.goto(url, wait_until="networkidle") # Aguarda o carregamento da rede
        
        # Extrai o texto visível para economizar tokens na API do Gemini
        html_content = await page.locator("body").inner_text()
        await browser.close()
        
    print("Conteúdo capturado com sucesso! Enviando para o Gemini...")

    # 3. Processamento do texto com o novo SDK do Gemini (google-genai)
    # Certifique-se de configurar sua chave: export GEMINI_API_KEY="sua_chave_aqui"
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Chamada assíncrona utilizando o módulo 'client.aio'
    resposta = await client.aio.models.generate_content(
        model='gemini-2.5-flash', # Modelo rápido e ideal para extração de texto
        contents=f"Texto da página web:\n\n{html_content}\n\nPedido de extração: {prompt_usuario}",
        config=types.GenerateContentConfig(
            # Força o modelo a responder estritamente no formato estruturado do Pydantic
            response_mime_type="application/json",
            response_schema=ListaCitacoes,
            temperature=0
        ),
    )
    
    return resposta.text

# Execução do Script
async def main():
    # Nota: Mudamos a URL para o endpoint de citações correto do sandbox indicado
    target_url = "https://quotes.toscrape.com"
    pedido = "Extraia todas as frases, incluindo o autor de cada uma e as tags associadas."
    
    resultado_json = await extrair_dados_com_ia(target_url, pedido)
    print("\n--- Resultado Extraído pela IA (JSON) ---")
    print(resultado_json)

if __name__ == "__main__":
    asyncio.run(main())

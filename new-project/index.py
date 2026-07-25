import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from playwright.async_api import async_playwright

from do_login import do_login
from get_feed import get_feed
from engage import engage_with_posts

# Carrega variáveis de ambiente do .env na raiz do projeto
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

EMAIL = os.getenv("USER_LINKEDIN")
PASSWORD = os.getenv("PASSWORD_LINKEDIN")
COMMENT_LIMIT = int(os.getenv("COMMENT_LIMIT", "5"))


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print("Iniciando login no LinkedIn...")
        await do_login(page, email=EMAIL, password=PASSWORD)
        print("Login realizado com sucesso!")

        # Navega para o feed e prepara a página
        await get_feed(page)

        print("\nIniciando o processo de engajamento...")
        engaged_count = await engage_with_posts(page, limit=COMMENT_LIMIT)
        print(f"\nEngajamento concluído! Total de posts processados: {engaged_count}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())


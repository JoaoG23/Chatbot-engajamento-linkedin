import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from playwright.async_api import async_playwright

from do_login import do_login

# Carrega variáveis de ambiente do .env na raiz do projeto
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

EMAIL = os.getenv("USER_LINKEDIN")
PASSWORD = os.getenv("PASSWORD_LINKEDIN")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print("Iniciando login no LinkedIn...")
        await do_login(page, email=EMAIL, password=PASSWORD)
        print("Login realizado com sucesso!")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())

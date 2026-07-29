import sys
import asyncio
from playwright.async_api import async_playwright
from config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD, CDP_URL, LIMIT_COMMENTS
from services.browser_service import BrowserService
from services.ollama_service import OllamaService
from services.linkedin_service import LinkedInService

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

async def main(use_cdp: bool = True, target_posts: int = LIMIT_COMMENTS):
    """
    Função principal que orquestra a automação do LinkedIn.

    Args:
        use_cdp: Se True, conecta à sessão já aberta do Chrome (porta 9222).
                 Se False, abre um novo navegador e realiza login com e-mail/senha.
        target_posts: Quantidade de postagens a comentar.
    """
    print("=================== LINKEDIN AUTOMATION BOT ===================")

    async with async_playwright() as p:
        browser = None
        if use_cdp:
            try:
                browser, context, page = await BrowserService.connect_existing_chrome(p, cdp_url=CDP_URL)
            except Exception as e:
                print(f"[Main] Falha ao conectar via CDP ({e}). Alternando para inicialização de novo navegador...")
                use_cdp = False

        if not use_cdp:
            browser, context, page = await BrowserService.launch_new_browser(p, headless=False)
            if LINKEDIN_EMAIL and LINKEDIN_PASSWORD:
                await BrowserService.do_login(page, LINKEDIN_EMAIL, LINKEDIN_PASSWORD)
            else:
                print("[Main] E-mail e senha não informados no .env. Por favor, faça o login manualmente na janela aberta.")
                await page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")
                await asyncio.sleep(15)

        # Inicializa os serviços
        ollama_service = OllamaService()
        linkedin_service = LinkedInService(page=page, llm_service=ollama_service)

        # Executa os comentários no feed
        await linkedin_service.process_feed_comments(target_count=target_posts)

        print("[Main] Execução finalizada com sucesso!")

if __name__ == "__main__":
    # Altere use_cdp para False se desejar abrir um novo navegador e fazer login com e-mail/senha
    asyncio.run(main(use_cdp=True, target_posts=LIMIT_COMMENTS))

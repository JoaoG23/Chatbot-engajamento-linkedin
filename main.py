import sys
import asyncio
from playwright.async_api import async_playwright
import argparse
from config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD, CDP_URL, LIMIT_COMMENTS, USE_CDP
from services.browser_service import BrowserService
from services.ollama_service import OllamaService
from services.linkedin_service import LinkedInService
from utils.logger import setup_logger

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

logger = setup_logger("Main")


async def main(use_cdp: bool = USE_CDP, target_posts: int = LIMIT_COMMENTS):
    """
    Função principal que orquestra a automação do LinkedIn.

    Args:
        use_cdp: Se True, conecta à sessão já aberta do Chrome (porta 9222).
                 Se False, abre um novo navegador e realiza login com e-mail/senha.
        target_posts: Quantidade de postagens a comentar.
    """
    logger.info("=================== LINKEDIN ENGAJADOR COMENTADOR DE POSTS ===================")
    logger.info("=================== Criado por Joao Guilherme Desenvolvedor Python ===================")
    logger.info(f"Modo de execução selecionado: {'Conectar ao Chrome Ativo (CDP)' if use_cdp else 'Abrir Novo Navegador (Playwright)'}")

    async with async_playwright() as playwright_instance:
        browser = None
        if use_cdp:
            try:
                browser, context, page = await BrowserService.connect_existing_chrome(
                    playwright_instance, cdp_url=CDP_URL
                )
            except Exception as connection_error:
                logger.warning(
                    f"Falha ao conectar via CDP ({connection_error}). Alternando para inicialização de novo navegador..."
                )
                use_cdp = False

        if not use_cdp:
            browser, context, page = await BrowserService.launch_new_browser(
                playwright_instance, headless=False
            )
            if LINKEDIN_EMAIL and LINKEDIN_PASSWORD:
                await BrowserService.do_login(page, LINKEDIN_EMAIL, LINKEDIN_PASSWORD)
            else:
                logger.warning(
                    "E-mail e senha não informados no .env. Por favor, faça o login manualmente na janela aberta."
                )
                await page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")
                await asyncio.sleep(15)

        # Inicializa os serviços
        ollama_service = OllamaService()
        linkedin_service = LinkedInService(page=page, llm_service=ollama_service)

        # Executa os comentários no feed
        await linkedin_service.process_feed_comments(target_count=target_posts)

        logger.info("Execução finalizada com sucesso!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bot de Engajamento para LinkedIn")
    parser.add_argument(
        "--mode",
        choices=["cdp", "browser"],
        default=None,
        help="Modo de inicialização: 'cdp' para usar Chrome aberto ou 'browser' para abrir novo navegador",
    )
    args = parser.parse_args()

    selected_use_cdp = USE_CDP
    if args.mode == "cdp":
        selected_use_cdp = True
    elif args.mode == "browser":
        selected_use_cdp = False

    asyncio.run(main(use_cdp=selected_use_cdp, target_posts=LIMIT_COMMENTS))

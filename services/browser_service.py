import asyncio
from playwright.async_api import Playwright, Browser, BrowserContext, Page
from config import CDP_URL, LINKEDIN_HOME_URL

class BrowserService:
    """Serviço responsável pelo gerenciamento de navegador e autenticação via Playwright."""

    @staticmethod
    async def _safe_goto(page: Page, url: str, retries: int = 3) -> None:
        """Navega com tentativas de re-conexão para evitar falhas de rede transitórias."""
        for attempt in range(retries):
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=20000)
                return
            except Exception as e:
                print(f"[BrowserService] Tentativa {attempt + 1}/{retries} de navegação para {url} falhou: {e}")
                if attempt == retries - 1:
                    raise e
                await asyncio.sleep(2)

    @staticmethod
    async def connect_existing_chrome(playwright: Playwright, cdp_url: str = CDP_URL) -> tuple[Browser, BrowserContext, Page]:
        """Conecta a uma instância já aberta do Chrome via Chrome DevTools Protocol (CDP)."""
        print(f"[BrowserService] Conectando ao Chrome em execução via CDP ({cdp_url})...")
        browser = await playwright.chromium.connect_over_cdp(cdp_url)
        context = browser.contexts[0]
        
        page = None
        for p in context.pages:
            if "linkedin.com" in p.url:
                page = p
                break
        
        if not page:
            page = await context.new_page()
            await BrowserService._safe_goto(page, "https://www.linkedin.com/feed/")
            
        await page.bring_to_front()
        print(f"[BrowserService] Conectado à página: {await page.title()}")
        return browser, context, page

    @staticmethod
    async def launch_new_browser(playwright: Playwright, headless: bool = False) -> tuple[Browser, BrowserContext, Page]:
        """Inicia uma nova instância de navegador (Chromium/Chrome)."""
        print("[BrowserService] Iniciando nova instância do navegador...")
        browser = await playwright.chromium.launch(headless=headless)
        context = await browser.new_context()
        page = await context.new_page()
        return browser, context, page

    @staticmethod
    async def do_login(page: Page, email: str, password: str) -> None:
        """
        Realiza o login no LinkedIn via Playwright.

        Args:
            page: Instância da página do Playwright.
            email: E-mail ou telefone do usuário.
            password: Senha do usuário.
        """
        print(f"[BrowserService] Navegando para {LINKEDIN_HOME_URL}...")
        await BrowserService._safe_goto(page, LINKEDIN_HOME_URL)
        await asyncio.sleep(20)

        # Clica no botão Entrar da landing page se visível
        sign_in_cta = page.locator('[data-test-id="home-hero-sign-in-cta"]')
        if await sign_in_cta.is_visible():
            await sign_in_cta.click()
            await asyncio.sleep(1)

        print("[BrowserService] Preenchendo e-mail...")
        email_field = page.get_by_role("textbox", name="E-mail ou telefone")
        await email_field.click()
        await asyncio.sleep(1)
        await email_field.fill(email)
        await asyncio.sleep(1)

        print("[BrowserService] Preenchendo senha...")
        password_field = page.get_by_role("textbox", name="Senha")
        await password_field.click()
        await asyncio.sleep(1)
        await password_field.fill(password)
        await asyncio.sleep(1)

        print("[BrowserService] Submetendo formulário de login...")
        submit_btn = page.get_by_role("button", name="Entrar", exact=True)
        if await submit_btn.is_visible():
            await submit_btn.click()
            await page.wait_for_load_state("domcontentloaded")
            await asyncio.sleep(30)

        if "feed" not in page.url:
            await BrowserService._safe_goto(page, "https://www.linkedin.com/feed/")
            await asyncio.sleep(3)

        print("[BrowserService] Sessão iniciada no Feed do LinkedIn!")

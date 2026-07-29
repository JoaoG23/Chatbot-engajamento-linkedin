import asyncio
import tempfile
from playwright.async_api import Playwright, Browser, BrowserContext, Page
from config import CDP_URL, LINKEDIN_HOME_URL


class BrowserService:
    """Serviço responsável pelo gerenciamento do navegador e autenticação via Playwright."""

    @staticmethod
    async def _safe_goto(page: Page, url: str, maximum_retries: int = 3) -> None:
        """Navega com tentativas de re-conexão para evitar falhas de rede transitórias."""
        for attempt_index in range(maximum_retries):
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=20000)
                return
            except Exception as navigation_error:
                print(
                    f"[BrowserService] Tentativa {attempt_index + 1}/{maximum_retries} de navegação para {url} falhou: {navigation_error}"
                )
                if attempt_index == maximum_retries - 1:
                    raise navigation_error
                await asyncio.sleep(2)

    @staticmethod
    async def connect_existing_chrome(
        playwright_instance: Playwright, cdp_url: str = CDP_URL
    ) -> tuple[Browser, BrowserContext, Page]:
        """Conecta a uma instância já aberta do Chrome via Chrome DevTools Protocol (CDP)."""
        print(f"[BrowserService] Conectando ao Chrome em execução via CDP ({cdp_url})...")
        browser = await playwright_instance.chromium.connect_over_cdp(cdp_url)
        context = browser.contexts[0]

        active_page = None
        for open_page in context.pages:
            if "linkedin.com" in open_page.url:
                active_page = open_page
                break

        if not active_page:
            active_page = await context.new_page()
            await BrowserService._safe_goto(active_page, "https://www.linkedin.com/feed/")

        await active_page.bring_to_front()
        print(f"[BrowserService] Conectado à página: {await active_page.title()}")
        return browser, context, active_page

    @staticmethod
    async def launch_new_browser(
        playwright_instance: Playwright, headless: bool = False
    ) -> tuple[Browser, BrowserContext, Page]:
        """Inicia uma nova instância de navegador no modo anônimo (incognito) em tamanho padrão."""
        print("[BrowserService] Iniciando nova instância do navegador no modo anônimo (incognito)...")
        temporary_user_data_dir = tempfile.mkdtemp()
        context = await playwright_instance.chromium.launch_persistent_context(
            user_data_dir=temporary_user_data_dir,
            headless=headless,
            viewport={"width": 1280, "height": 800},
            args=["--incognito"],
        )
        active_page = context.pages[0] if context.pages else await context.new_page()
        return None, context, active_page

    @staticmethod
    async def do_login(page: Page, email: str, password: str) -> None:
        """Realiza o login no LinkedIn abrindo primeiro a home por 13 segundos."""
        print(f"[BrowserService] Navegando para {LINKEDIN_HOME_URL}...")
        await BrowserService._safe_goto(page, LINKEDIN_HOME_URL)
        await asyncio.sleep(13)

        sign_in_call_to_action = page.locator('[data-test-id="home-hero-sign-in-cta"]')
        if await sign_in_call_to_action.is_visible():
            await sign_in_call_to_action.click()
            await asyncio.sleep(5)

        print("[BrowserService] Preenchendo e-mail...")
        email_input_locator = page.locator('#username, input[name="session_key"], input[id="username"]').first
        if not await email_input_locator.is_visible():
            email_input_locator = page.get_by_role("textbox", name="E-mail ou telefone").first

        await email_input_locator.click()
        await email_input_locator.fill(email)
        await asyncio.sleep(1)

        print("[BrowserService] Preenchendo senha...")
        password_input_locator = page.locator('#password, input[name="session_password"], input[id="password"]').first
        if not await password_input_locator.is_visible():
            password_input_locator = page.get_by_role("textbox", name="Senha").first

        await password_input_locator.click()
        await password_input_locator.fill(password)
        await asyncio.sleep(1)

        print("[BrowserService] Submetendo formulário de login...")
        submit_button_locator = page.locator('button[type="submit"], button:has-text("Entrar")').first
        if await submit_button_locator.is_visible():
            await submit_button_locator.click()
        else:
            await password_input_locator.press("Enter")

        try:
            await page.wait_for_url("**/feed**", timeout=30000)
        except Exception:
            await asyncio.sleep(10)

        if "feed" in page.url:
            print("[BrowserService] Sessão iniciada no Feed do LinkedIn com sucesso!")
            return

        print("[BrowserService] Login efetuado. Se houver verificação ou 2FA, conclua na janela aberta.")

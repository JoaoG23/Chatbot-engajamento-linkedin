import asyncio

from playwright.async_api import Page


LINKEDIN_HOME_URL = "https://www.linkedin.com/home"


async def _navigate_to_home(page: Page) -> None:
    """Navega para a página inicial do LinkedIn."""
    await page.goto(LINKEDIN_HOME_URL, wait_until="networkidle")


async def _click_sign_in_button(page: Page) -> None:
    """Clica no botão de entrar na landing page."""
    await page.locator("[data-test-id=\"home-hero-sign-in-cta\"]").click()


async def _fill_email(page: Page, email: str) -> None:
    """Preenche o campo de e-mail ou telefone."""
    await page.get_by_role("textbox", name="E-mail ou telefone").click()
    await asyncio.sleep(2)
    await page.get_by_role("textbox", name="E-mail ou telefone").fill(email)
    await asyncio.sleep(2)


async def _fill_password(page: Page, password: str) -> None:
    """Preenche o campo de senha."""
    await page.get_by_role("textbox", name="Senha").click()
    await asyncio.sleep(2)
    await page.get_by_role("textbox", name="Senha").fill(password)
    await asyncio.sleep(2)


async def _submit_login(page: Page) -> None:
    """Clica no botão de entrar no formulário de login."""
    await asyncio.sleep(2)
    await page.get_by_role("button", name="Entrar", exact=True).click()
    await page.wait_for_load_state("networkidle")


async def do_login(page: Page, email: str, password: str) -> None:
    """
    Realiza o login no LinkedIn via Playwright.

    Args:
        page: Instância da página do Playwright.
        email: E-mail ou telefone do usuário.
        password: Senha do usuário.
    """
    await _navigate_to_home(page)
    await _click_sign_in_button(page)
    await _fill_email(page, email)
    await _fill_password(page, password)
    await _submit_login(page)

import asyncio

from playwright.async_api import Page


LINKEDIN_FEED_URL = "https://www.linkedin.com/feed/"

WAIT_FOR_TOKEN_SECONDS = 22
SCROLL_TIMES = 3
SCROLL_STEP_PX = 800
SCROLL_DELAY_SECONDS = 2


async def _wait_for_token() -> None:
    """Aguarda o token de autenticação ser processado pelo LinkedIn."""
    print(f"Aguardando {WAIT_FOR_TOKEN_SECONDS}s para o token ser validado...")
    await asyncio.sleep(WAIT_FOR_TOKEN_SECONDS)


async def _navigate_to_feed(page: Page) -> None:
    """Navega para o feed do LinkedIn."""
    print("Navegando para o feed...")
    await page.goto(LINKEDIN_FEED_URL, wait_until="domcontentloaded")


async def _scroll_down(page: Page) -> None:
    """Rola a página para baixo N vezes."""
    print(f"Rolando para baixo {SCROLL_TIMES}x...")
    for _ in range(SCROLL_TIMES):
        await page.mouse.wheel(0, SCROLL_STEP_PX)
        await asyncio.sleep(SCROLL_DELAY_SECONDS)


async def _scroll_up(page: Page) -> None:
    """Rola a página para cima N vezes."""
    print(f"Rolando para cima {SCROLL_TIMES}x...")
    for _ in range(SCROLL_TIMES):
        await page.mouse.wheel(0, -SCROLL_STEP_PX)
        await asyncio.sleep(SCROLL_DELAY_SECONDS)


async def _click_main_feed(page: Page) -> None:
    """Clica no elemento principal do feed."""
    print("Clicando no mainFeed...")
    await page.get_by_test_id("mainFeed").click()
    await asyncio.sleep(2)


async def _get_feed_children(page: Page) -> list[str]:
    """
    Captura os filhos diretos do mainFeed e retorna seus inner_texts.

    Returns:
        Lista de textos dos elementos filhos do mainFeed.
    """
    print("Capturando filhos do mainFeed...")
    main_feed = page.get_by_test_id("mainFeed")
    children = await main_feed.locator("> *").all()

    posts = []
    for child in children:
        text = await child.inner_text()
        if text.strip():
            posts.append(text.strip())

    return posts


async def get_feed(page: Page) -> list[str]:
    """
    Acessa o feed do LinkedIn e captura os posts do mainFeed.

    Fluxo:
        1. Aguarda token de autenticação (22s)
        2. Navega para o feed
        3. Rola 3x para baixo
        4. Rola 3x para cima
        5. Clica no mainFeed
        6. Retorna os filhos (posts) do mainFeed

    Args:
        page: Instância da página do Playwright.

    Returns:
        Lista de textos dos posts encontrados no feed.
    """
    await _wait_for_token()
    await _navigate_to_feed(page)
    await _scroll_down(page)
    await _scroll_up(page)
    # await _click_main_feed(page)
    posts = await _get_feed_children(page)

    print(f"{len(posts)} posts capturados do feed.")
    return posts

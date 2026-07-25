import asyncio
import os
from pathlib import Path
from playwright.async_api import Page, Locator
from google import genai
from google.genai import types

from utils.get_text_from_file.get_text_from_file import get_text_from_file
from utils.remove_emojis_text.remove_emojis_text import remove_emojis_text
from utils.remove_linebreak_text.remove_linebreak_text import remove_linebreak_text


async def generate_comment(content_post: str) -> str:
    """Gera um comentário com IA baseado no conteúdo do post."""
    if not content_post:
        return ""

    prompt_path = Path(__file__).parent.parent.parent / "templates" / "prompt.txt"
    prompt = get_text_from_file(str(prompt_path))
    prompt_clean = remove_linebreak_text(prompt)

    token = os.getenv("AI_TOKEN")
    if not token:
        return ""

    client = genai.Client(api_key=token)
    full_prompt = f"{prompt_clean}\n\nPostagem: (({content_post}))"

    # Modelos suportados pela API Gemini
    models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    for model in models:
        try:
            response = await client.aio.models.generate_content(
                model=model,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    top_p=0.8,
                    top_k=10,
                    stop_sequences=["Title"],
                ),
            )
            if response.text:
                comment = remove_linebreak_text(response.text)
                return remove_emojis_text(comment)
        except Exception as e:
            print(f"[IA] Falha ao gerar comentário com {model}: {e}")

    return ""


async def get_post_text(post: Locator) -> str:
    """Extrai o texto da publicação, expandindo-o se necessário."""
    more_button = post.locator("button:has-text('…mais'), span:has-text('…mais')").first
    if await more_button.is_visible():
        await more_button.click()
        await asyncio.sleep(1)

    description = post.locator(
        ".feed-shared-update-v2__description, .update-components-update-v2__commentary"
    ).first

    if not await description.is_visible():
        return ""

    text = await description.inner_text()
    return remove_linebreak_text(text)


async def like_post(post: Locator) -> bool:
    """Reage com 'Gostei' no post se ainda não estiver curtido."""
    like_button = post.locator(
        "button.react-button__trigger, button[aria-label^='Reagir']"
    ).first

    if not await like_button.is_visible():
        return False

    aria_label = await like_button.get_attribute("aria-label")
    if aria_label not in ["Reagir com gostei", "Gostei"]:
        return False

    await like_button.click()
    await asyncio.sleep(1)
    return True


async def is_already_commented(post: Locator, my_name: str = "João Guilherme") -> bool:
    """Verifica se o post já foi comentado por mim."""
    if not my_name:
        return False

    authors = post.locator(".comments-comment-meta__description-title")
    count = await authors.count()

    if count == 0:
        return False

    for i in range(count):
        name = await authors.nth(i).inner_text()
        if my_name.lower() in name.lower():
            return True

    return False


async def comment_on_post(post: Locator, comment_text: str) -> bool:
    """Digita e envia o comentário no post."""
    if not comment_text:
        return False

    # 1. Abre a caixa de comentários
    comment_trigger = post.get_by_label("Comentar").first
    if not await comment_trigger.is_visible():
        comment_trigger = post.locator("button").filter(has_text="Comentar").first

    if not await comment_trigger.is_visible():
        return False

    await comment_trigger.click()
    await asyncio.sleep(2)

    # 2. Localiza e preenche o input do comentário
    comment_input = post.locator(
        ".ql-editor[role='textbox'], [aria-label='Editor de texto para criar comentário'], [data-placeholder='Adicionar comentário…']"
    ).first

    if not await comment_input.is_visible():
        return False

    await comment_input.click()
    await comment_input.fill(comment_text)
    await asyncio.sleep(2)

    # 3. Modo simulação para desenvolvimento (evita comentários reais em teste)
    if os.getenv("ENVIRONMENT") == "dev":
        print(f"[Simulação DEV] Comentário gerado: '{comment_text}'")
        return True

    # 4. Envia o comentário (botão "Publicar" ou "Comentar" no final do formulário)
    submit_button = post.locator(
        "button.comments-comment-box__submit-button, button:has-text('Publicar'), button:has-text('Comentar')"
    ).last

    if not await submit_button.is_visible() or not await submit_button.is_enabled():
        return False

    await submit_button.click()
    await asyncio.sleep(4)
    return True


async def engage_with_posts(page: Page, limit: int = 5) -> int:
    """Percorre os posts do feed, curtindo e comentando usando IA."""
    if limit <= 0:
        return 0

    # Busca posts no feed principal
    posts = await page.locator(
        "div.feed-shared-update-v2, .fie-impression-container, [data-testid='mainFeed'] > div[role='listitem']"
    ).all()

    total_posts = len(posts)
    if total_posts == 0:
        print("Nenhum post encontrado no feed.")
        return 0

    print(f"Posts encontrados no feed: {total_posts}. Limite de engajamento: {limit}")

    engaged_count = 0
    for i in range(min(total_posts, limit)):
        post = posts[i]
        print(f"\n--- Processando Post {i+1}/{min(total_posts, limit)} ---")

        post_text = await get_post_text(post)
        if not post_text:
            print("Post sem texto disponível. Pulando...")
            continue

        already_commented = await is_already_commented(post)
        if already_commented:
            print("Post já comentado anteriormente. Pulando...")
            continue

        # Realiza ações
        await like_post(post)

        comment_text = await generate_comment(post_text)
        if not comment_text:
            print("Não foi possível gerar comentário por IA. Pulando...")
            continue

        success = await comment_on_post(post, comment_text)
        if not success:
            print("Falha ao publicar comentário.")
            continue

        print(f"Post engajado com sucesso: '{comment_text[:40]}...'")
        engaged_count += 1

    return engaged_count

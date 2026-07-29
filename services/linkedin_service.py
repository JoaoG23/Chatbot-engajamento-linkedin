import random
import asyncio
from tqdm import tqdm
from playwright.async_api import Page
from services.ollama_service import OllamaService
from utils.text_cleaner import remove_linebreak_text
from utils.history_manager import load_history, save_history, get_post_hash


class LinkedInService:
    """Serviço responsável pelas interações automatizadas no feed do LinkedIn."""

    def __init__(self, page: Page, llm_service: OllamaService):
        self.page = page
        self.llm_service = llm_service
        self.history = load_history()

    async def expand_post_if_needed(self, post_index: int) -> None:
        """Clica no botão '...mais' para expandir o texto do post se estiver oculto."""
        try:
            await self.page.evaluate(
                """(targetButtonIndex) => {
                const commentButtons = Array.from(document.querySelectorAll('button[aria-label*="Comentar"]'));
                const targetButton = commentButtons[targetButtonIndex];
                if (!targetButton) return;
                
                let parentContainer = targetButton.closest('div[data-id], article, div.scaffold-finite-scroll__content > div') || targetButton.parentElement.parentElement.parentElement;
                if (!parentContainer) parentContainer = document.body;
                
                const seeMoreButton = Array.from(parentContainer.querySelectorAll('button')).find(button => button.innerText.includes('mais') || button.innerText.includes('see more'));
                if (seeMoreButton) seeMoreButton.click();
            }""",
                post_index,
            )
            await asyncio.sleep(1)
        except Exception as expansion_error:
            print(f"[LinkedInService] Aviso ao expandir texto do post {post_index + 1}: {expansion_error}")

    async def extract_post_text(self, post_index: int) -> str:
        """Extrai o texto legível da postagem no feed."""
        raw_text = await self.page.evaluate(
            """(targetButtonIndex) => {
            const commentButtons = Array.from(document.querySelectorAll('button[aria-label*="Comentar"]'));
            const targetButton = commentButtons[targetButtonIndex];
            if (!targetButton) return '';
            
            let parentContainer = targetButton.closest('div[data-id], article, div.scaffold-finite-scroll__content > div') || targetButton.parentElement.parentElement.parentElement;
            return parentContainer ? parentContainer.innerText : '';
        }""",
            post_index,
        )
        return remove_linebreak_text(raw_text)

    async def has_existing_user_comment_in_dom(self, post_index: int) -> bool:
        """Verifica se a postagem já possui um comentário feito pelo usuário logado."""
        return await self.page.evaluate(
            """(targetButtonIndex) => {
            const commentButtons = Array.from(document.querySelectorAll('button[aria-label*="Comentar"]'));
            const targetButton = commentButtons[targetButtonIndex];
            if (!targetButton) return false;
            
            let parentContainer = targetButton.closest('div[data-id], article, div.scaffold-finite-scroll__content > div') || targetButton.parentElement.parentElement.parentElement;
            if (!parentContainer) return false;
            
            const commentItems = parentContainer.querySelectorAll('.comments-comment-item, .comments-post-meta, article.comments-comment-item');
            for (let item of commentItems) {
                const itemText = item.innerText || '';
                if (itemText.includes('Você') || itemText.includes('Seu comentário')) {
                    return true;
                }
            }
            return false;
        }""",
            post_index,
        )

    async def type_and_submit_comment(self, post_index: int, comment_text: str) -> bool:
        """Digita o comentário na caixa de texto do post e clica no botão de submissão."""
        typing_success = await self.page.evaluate(
            """({ targetIndex, textToType }) => {
            const commentButtons = Array.from(document.querySelectorAll('button[aria-label*="Comentar"]'));
            const targetButton = commentButtons[targetIndex];
            let parentContainer = targetButton ? (targetButton.closest('div[data-id], article, div.scaffold-finite-scroll__content > div') || targetButton.parentElement.parentElement.parentElement) : document.body;
            if (!parentContainer) parentContainer = document.body;
            
            const textEditor = parentContainer.querySelector('div[role="textbox"], div[contenteditable="true"]');
            if (textEditor) {
                textEditor.focus();
                document.execCommand('insertText', false, textToType);
                return true;
            }
            return false;
        }""",
            {"targetIndex": post_index, "textToType": comment_text},
        )

        if not typing_success:
            await self.page.keyboard.type(comment_text)

        await asyncio.sleep(1.5)

        is_submitted = await self.page.evaluate(
            """() => {
            const allButtons = Array.from(document.querySelectorAll('button'));
            const submitButton = allButtons.find(button => !button.disabled && button.innerText.trim() === 'Comentar' && (!button.getAttribute('aria-label') || button.getAttribute('aria-label') === ''));
            if (submitButton) {
                submitButton.click();
                return true;
            }
            return false;
        }"""
        )

        return is_submitted

    def _record_history(self, post_hash: str) -> None:
        """Adiciona o hash da postagem ao histórico e persiste no disco."""
        self.history.add(post_hash)
        save_history(self.history)

    async def _should_skip_post(self, post_index: int, post_hash: str) -> bool:
        """Verifica se a postagem deve ser ignorada (histórico ou já comentada pelo usuário)."""
        if post_hash in self.history:
            return True

        if await self.has_existing_user_comment_in_dom(post_index):
            self._record_history(post_hash)
            return True

        return False

    async def _scroll_page(self, scroll_times: int = 1, delay_seconds: float = 2.0) -> None:
        """Executa a rolagem da página com a tecla PageDown."""
        for _ in range(scroll_times):
            await self.page.keyboard.press("PageDown")
        await asyncio.sleep(delay_seconds)

    async def _process_single_post(
        self, post_index: int, comment_button, progress_bar: tqdm
    ) -> bool:
        """Executa o ciclo completo de leitura, geração e envio de comentário para um único post."""
        await comment_button.scroll_into_view_if_needed()
        await asyncio.sleep(1)

        await self.expand_post_if_needed(post_index)

        cleaned_post_text = await self.extract_post_text(post_index)
        post_hash = get_post_hash(cleaned_post_text)

        if await self._should_skip_post(post_index, post_hash):
            return False

        snippet_display = cleaned_post_text[:80]
        progress_bar.set_postfix_str(f"Lendo: {snippet_display}...")

        generated_comment_text = self.llm_service.generate_comment(cleaned_post_text)

        await comment_button.click()
        await asyncio.sleep(1.5)

        is_submitted = await self.type_and_submit_comment(post_index, generated_comment_text)

        if not is_submitted:
            await asyncio.sleep(2)
            return False

        self._record_history(post_hash)
        progress_bar.update(1)

        # Intervalo seguro de 7 a 10 segundos entre comentários
        random_post_delay = random.uniform(7.0, 10.0)
        progress_bar.set_postfix_str(f"Aguardando {random_post_delay:.1f}s...")
        await asyncio.sleep(random_post_delay)
        return True

    async def process_feed_comments(self, target_count: int = 30) -> int:
        """Processa o feed com barra de progresso (tqdm) até atingir a quantidade desejada."""
        print(f"\n[LinkedInService] Iniciando automação para {target_count} comentários no feed...")
        await self.page.keyboard.press("Home")
        await asyncio.sleep(2)

        successful_comment_count = 0
        processed_element_indices = set()
        scroll_attempt_count = 0

        progress_bar = tqdm(total=target_count, desc="Comentando posts", unit="post")

        while successful_comment_count < target_count and scroll_attempt_count < 100:
            comment_action_buttons = await self.page.query_selector_all('button[aria-label*="Comentar"]')

            for button_index, comment_button in enumerate(comment_action_buttons):
                if button_index in processed_element_indices:
                    continue

                processed_element_indices.add(button_index)

                was_commented = await self._process_single_post(
                    button_index, comment_button, progress_bar
                )
                if was_commented:
                    successful_comment_count += 1

                await self._scroll_page(scroll_times=1, delay_seconds=2.0)

                if successful_comment_count >= target_count:
                    break

            await self._scroll_page(scroll_times=2, delay_seconds=3.0)
            scroll_attempt_count += 1
            processed_element_indices.clear()

        progress_bar.close()
        print(
            f"\n=================== CONCLUÍDO: {successful_comment_count} COMENTÁRIOS PUBLICADOS ==================="
        )
        return successful_comment_count

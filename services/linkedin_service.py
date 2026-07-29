import random
from tqdm import tqdm
import asyncio
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
        """Clica no botão '...mais' para expandir o texto do post se houver."""
        try:
            await self.page.evaluate("""(btnIndex) => {
                const btns = Array.from(document.querySelectorAll('button[aria-label*="Comentar"]'));
                const target = btns[btnIndex];
                if (!target) return;
                let parent = target.closest('div[data-id], article, div.scaffold-finite-scroll__content > div') || target.parentElement.parentElement.parentElement;
                if (!parent) parent = document.body;
                const sm = Array.from(parent.querySelectorAll('button')).find(b => b.innerText.includes('mais') || b.innerText.includes('see more'));
                if (sm) sm.click();
            }""", post_index)
            await asyncio.sleep(1)
        except Exception as e:
            print(f"[LinkedInService] Aviso ao expandir texto do post {post_index+1}: {e}")

    async def extract_post_text(self, post_index: int) -> str:
        """Extrai o texto legível da postagem no feed."""
        raw_text = await self.page.evaluate("""(btnIndex) => {
            const btns = Array.from(document.querySelectorAll('button[aria-label*="Comentar"]'));
            const target = btns[btnIndex];
            if (!target) return '';
            let parent = target.closest('div[data-id], article, div.scaffold-finite-scroll__content > div') || target.parentElement.parentElement.parentElement;
            return parent ? parent.innerText : '';
        }""", post_index)
        return remove_linebreak_text(raw_text)

    async def has_existing_user_comment_in_dom(self, post_index: int) -> bool:
        """Verifica se o DOM da postagem já contém um comentário do usuário logado."""
        return await self.page.evaluate("""(btnIndex) => {
            const btns = Array.from(document.querySelectorAll('button[aria-label*="Comentar"]'));
            const target = btns[btnIndex];
            if (!target) return false;
            let parent = target.closest('div[data-id], article, div.scaffold-finite-scroll__content > div') || target.parentElement.parentElement.parentElement;
            if (!parent) return false;
            
            const commentItems = parent.querySelectorAll('.comments-comment-item, .comments-post-meta, article.comments-comment-item');
            for (let item of commentItems) {
                const text = item.innerText || '';
                if (text.includes('Você') || text.includes('Seu comentário')) {
                    return true;
                }
            }
            return false;
        }""", post_index)

    async def type_and_submit_comment(self, post_index: int, comment_text: str) -> bool:
        """Digita o comentário na caixa de texto e clica no botão de submeter."""
        type_success = await self.page.evaluate("""({ idx, text }) => {
            const btns = Array.from(document.querySelectorAll('button[aria-label*="Comentar"]'));
            const target = btns[idx];
            let parent = target ? (target.closest('div[data-id], article, div.scaffold-finite-scroll__content > div') || target.parentElement.parentElement.parentElement) : document.body;
            if (!parent) parent = document.body;
            
            const editor = parent.querySelector('div[role="textbox"], div[contenteditable="true"]');
            if (editor) {
                editor.focus();
                document.execCommand('insertText', false, text);
                return true;
            }
            return false;
        }""", {"idx": post_index, "text": comment_text})

        if not type_success:
            await self.page.keyboard.type(comment_text)

        await asyncio.sleep(1.5)

        submitted = await self.page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const submitBtn = btns.find(b => !b.disabled && b.innerText.trim() === 'Comentar' && (!b.getAttribute('aria-label') || b.getAttribute('aria-label') === ''));
            if (submitBtn) {
                submitBtn.click();
                return true;
            }
            return false;
        }""")

        return submitted

    def _record_history(self, post_hash: str) -> None:
        """Adiciona o hash da postagem ao histórico e persiste o arquivo."""
        self.history.add(post_hash)
        save_history(self.history)

    async def _should_skip_post(self, post_index: int, post_hash: str) -> bool:
        """Verifica se a postagem deve ser ignorada (já no histórico ou já comentada pelo usuário)."""
        if post_hash in self.history:
            return True

        if await self.has_existing_user_comment_in_dom(post_index):
            self._record_history(post_hash)
            return True

        return False

    async def _scroll_page(self, times: int = 1, delay: float = 2.0) -> None:
        """Executa rolagem com a tecla PageDown determinada quantidade de vezes."""
        for _ in range(times):
            await self.page.keyboard.press("PageDown")
        await asyncio.sleep(delay)

    async def _process_single_post(self, post_index: int, btn, pbar: tqdm) -> bool:
        """Executa o ciclo completo de leitura, geração e envio de comentário para um post.

        Retorna True se o comentário foi enviado com sucesso, False caso contrário.
        """
        await btn.scroll_into_view_if_needed()
        await asyncio.sleep(1)

        await self.expand_post_if_needed(post_index)

        clean_text = await self.extract_post_text(post_index)
        post_hash = get_post_hash(clean_text)

        if await self._should_skip_post(post_index, post_hash):
            return False

        snippet_display = clean_text[:80]
        pbar.set_postfix_str(f"Lendo: {snippet_display}...")

        comment_text = self.llm_service.generate_comment(clean_text)

        await btn.click()
        await asyncio.sleep(1.5)

        submitted = await self.type_and_submit_comment(post_index, comment_text)

        if submitted:
            self._record_history(post_hash)
            pbar.update(1)

            # Intervalo seguro de 7 a 10 segundos entre comentários
            post_delay = random.uniform(7.0, 10.0)
            pbar.set_postfix_str(f"Aguardando {post_delay:.1f}s...")
            await asyncio.sleep(post_delay)
            return True
        else:
            await asyncio.sleep(2)
            return False

    async def process_feed_comments(self, target_count: int = 30) -> int:
        """Processa o feed com barra de progresso (tqdm) até atingir a quantidade desejada."""
        print(f"\n[LinkedInService] Iniciando automação para {target_count} comentários no feed...")
        await self.page.keyboard.press("Home")
        await asyncio.sleep(2)

        successful_comments = 0
        processed_elements = set()
        scroll_attempts = 0

        pbar = tqdm(total=target_count, desc="Comentando posts", unit="post")

        while successful_comments < target_count and scroll_attempts < 100:
            action_btns = await self.page.query_selector_all('button[aria-label*="Comentar"]')

            for idx, btn in enumerate(action_btns):
                if idx in processed_elements:
                    continue

                processed_elements.add(idx)

                commented = await self._process_single_post(idx, btn, pbar)
                if commented:
                    successful_comments += 1

                await self._scroll_page(times=1, delay=2.0)

                if successful_comments >= target_count:
                    break

            await self._scroll_page(times=2, delay=3.0)
            scroll_attempts += 1
            processed_elements.clear()

        pbar.close()
        print(f"\n=================== CONCLUÍDO: {successful_comments} COMENTÁRIOS PUBLICADOS ===================")
        return successful_comments

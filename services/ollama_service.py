import os
import random
import ollama

from config import OLLAMA_HOST, OLLAMA_MODEL, PROMPT_FILE, EXAMPLES_FILE
from utils.text_cleaner import remove_linebreak_text, remove_emojis_text
from utils.logger import setup_logger

logger = setup_logger("OllamaService")


class OllamaService:
    def __init__(self, model_name=None, host=None, prompt_path=None, examples_path=None):
        self.model_name = model_name or OLLAMA_MODEL
        self.host = host or OLLAMA_HOST
        self.client = ollama.Client(host=self.host)
        self.prompt_path = prompt_path or PROMPT_FILE
        self.examples_path = examples_path or EXAMPLES_FILE
        self.system_prompt = self._read_prompt()

        self.fallback_comments = [
            "Excelente postagem! Conteúdo muito relevante e importante para a nossa comunidade de tecnologia. Valeu!",
            "Muito bom! Conteúdo de altíssimo nível que agrega bastante valor no dia a dia do desenvolvedor. Parabéns!",
            "Excelente reflexão! Muito importante compartilhar conteúdos de qualidade como esse com a nossa rede.",
            "Conteúdo sensacional! Parabéns pelo trabalho e muito obrigado por compartilhar essa visão conosco!",
        ]

    def _read_file_content(self, path: str) -> str:
        """Lê o conteúdo de um arquivo caso ele exista."""
        if not path or not os.path.exists(path):
            return ""

        with open(path, "r", encoding="utf8") as file_stream:
            return file_stream.read().strip()

    def _read_prompt(self) -> str:
        """Lê e combina o arquivo de instruções da persona e o arquivo de exemplos."""
        persona_content = self._read_file_content(self.prompt_path)
        examples_content = self._read_file_content(self.examples_path)

        if not persona_content:
            return examples_content

        if not examples_content:
            return persona_content

        return f"{persona_content}\n\n{examples_content}"

    def get_fallback_comment(self) -> str:
        """Retorna um comentário de contingência aleatório."""
        return random.choice(self.fallback_comments)

    def generate_comment(self, content_post: str) -> str:
        """Gera um comentário inteligente utilizando o Ollama diretamente sem cortes no código."""
        if not content_post or not content_post.strip():
            logger.warning("Conteúdo do post vazio. Utilizando comentário de contingência.")
            return self.get_fallback_comment()

        self.system_prompt = self._read_prompt()

        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt,
                    },
                    {
                        "role": "user",
                        "content": f"Postagem no LinkedIn: {content_post}",
                    },
                ],
                options={
                    "temperature": 0.3,
                    "top_p": 0.8,
                    "top_k": 20,
                },
            )
        except Exception as communication_error:
            logger.error(f"Erro ao comunicar com Ollama ({communication_error}). Utilizando contingência.")
            return self.get_fallback_comment()

        if not response or "message" not in response or "content" not in response["message"]:
            logger.error("Resposta inválida recebida do Ollama. Utilizando contingência.")
            return self.get_fallback_comment()

        raw_text = response["message"]["content"].strip()
        cleaned_text = remove_emojis_text(remove_linebreak_text(raw_text))

        if len(cleaned_text) < 10:
            logger.warning("Comentário gerado é muito curto (< 10 chars). Utilizando contingência.")
            return self.get_fallback_comment()

        logger.info(f"Comentário gerado com sucesso pelo Ollama: {cleaned_text}")
        return cleaned_text

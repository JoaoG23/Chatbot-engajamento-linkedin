import os
import random
import time

from google import genai
from google.genai import types

from config import AI_TOKEN, PROMPT_FILE
from utils.text_cleaner import remove_linebreak_text, remove_emojis_text


class GeminiService:
    def __init__(self, api_key=None, prompt_path=None):
        self.client = genai.Client(api_key=api_key or AI_TOKEN)

        self.prompt_path = prompt_path or PROMPT_FILE
        self.system_prompt = self._read_prompt()

        self.models = [
            "gemini-flash-latest",
            "gemini-flash-lite-latest",
            "gemini-2.0-flash",
            "gemini-2.0-flash-lite",
        ]

        self.fallback_comments = [
            "Que massa! Muito top!",
            "Interessantíssimo! Excelente conteúdo!",
            "Que show! Parabéns pelo post!",
            "Muito bom! Excelente publicação.",
            "Sensacional! Conteúdo de altíssimo nível.",
            "Muito massa! Parabéns pela iniciativa.",
            "Ótima reflexão! Muito obrigado por compartilhar.",
            "Que legal! Muito bom mesmo.",
            "Excelente post! Valeu pelo compartilhamento.",
            "Shooow! Muito bacana.",
            "Conteúdo top demais! Parabéns.",
            "Que visão bacana! Excelente.",
            "Muito interessante! Conteúdo relevante.",
            "Que massa! Parabéns pelo trabalho.",
            "Sensacional! Muito bom.",
            "Excelente contribuição para a comunidade!",
            "Muito top! Acompanhando por aqui.",
            "Que show! Conteúdo fantástico.",
            "Post sensacional! Valeu por compartilhar.",
            "Muito bom mesmo! Parabéns pelo post.",
            "Excelente leitura! Muito obrigado por compartilhar.",
            "Conteúdo sensacional! Parabéns pelo trabalho.",
            "Muito show! Excelente reflexão.",
            "Que bacana! Ótima contribuição.",
            "Top demais! Sempre trazendo conteúdo de valor.",
            "Muito interessante essa abordagem! Parabéns.",
            "Que post massa! Valeu demais.",
            "Excelente sacada! Muito bom.",
            "Sensacional! Conteúdo rico e direto.",
            "Muito bom! Post indispensável.",
            "Que aula! Parabéns pela publicação.",
            "Excelente material! Obrigado por compartilhar.",
            "Show de bola! Muito bacana mesmo.",
            "Ótimo post! Muito relevante.",
            "Conteúdo excelente! Parabéns pela clareza.",
            "Que massa essa perspectiva! Muito bom.",
            "Sensacional a explicação! Parabéns.",
            "Muito top! Valeu por agregar tanto valor.",
            "Excelente postagem! Conteúdo incrível.",
            "Muito show! Acompanhando os próximos.",
            "Sensacional! Tema de grande importância.",
            "Muito bacana esse ponto de vista!",
            "Que post enriquecedor! Parabéns.",
            "Excelente resumo! Muito direto e objetivo.",
            "Muito massa! Parabéns pelo empenho.",
            "Top demais! Excelente análise.",
            "Ótima publicação! Conteúdo impecável.",
            "Que show! Sempre agregando conhecimento.",
            "Muito bom! Valeu demais pela dica.",
            "Excelente postagem! Vale a pena acompanhar.",
            "Sensacional! Muito bem elaborado.",
            "Que massa! Conteúdo de utilidade pública para devs.",
            "Muito top! Post super relevante.",
            "Excelente visão sobre o assunto! Parabéns.",
            "Que legal! Muito enriquecedor.",
            "Sensacional! Parabéns pelo conteúdo gerado.",
            "Muito bom! Obrigado por compartilhar essa visão.",
            "Shooow de post! Valeu demais.",
            "Excelente! Conteúdo extremamente útil.",
            "Muito massa! Parabéns pela excelente postagem.",
        ]

    def _read_prompt(self):
        """Lê o arquivo de prompt de texto."""
        with open(self.prompt_path, "r", encoding="utf8") as f:
            return f.read().strip()

    def generate_comment(self, content_post):
        """Gera comentário com 10s de intervalo antes da requisição."""
        print("[GeminiService] Aguardando 10 segundos antes da geração do modelo...")
        time.sleep(10)

        for model in self.models:
            try:
                config_kwargs = {
                    "temperature": 0.5,
                    "top_p": 0.8,
                    "top_k": 20,
                    "max_output_tokens": 250,
                    "system_instruction": self.system_prompt
                }

                response = self.client.models.generate_content(
                    model=model,
                    contents=content_post,
                    config=types.GenerateContentConfig(**config_kwargs),
                )

                if response and response.text:
                    text = remove_emojis_text(
                        remove_linebreak_text(response.text.strip())
                    )
                    if len(text) > 10:
                        return text

            except Exception as e:
                print(f"[GeminiService] Modelo {model} indisponível ou limite atingido ({e}). Tentando próximo modelo...")
                continue

        print("[GeminiService] Todos os modelos falharam ou estão em limite de cota. Utilizando comentário de contingência.")
        return random.choice(self.fallback_comments)
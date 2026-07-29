import sys
import os
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.ollama_service import OllamaService


class TestOllamaService(unittest.TestCase):
    """Suíte de testes unitários e de integração para o OllamaService."""

    def setUp(self):
        self.service = OllamaService()

    def test_empty_content_post_returns_fallback_comment(self):
        """Verifica se uma postagem vazia dispara o comentário de contingência."""
        comment = self.service.generate_comment("")
        self.assertIn(comment, self.service.fallback_comments)

    def test_none_content_post_returns_fallback_comment(self):
        """Verifica se None como postagem dispara o comentário de contingência."""
        comment = self.service.generate_comment(None)
        self.assertIn(comment, self.service.fallback_comments)

    def test_get_fallback_comment_returns_valid_string(self):
        """Verifica se o gerador de contingência retorna um item da lista esperada."""
        comment = self.service.get_fallback_comment()
        self.assertIsInstance(comment, str)
        self.assertIn(comment, self.service.fallback_comments)

    @patch("ollama.Client")
    def test_generate_comment_with_mocked_client(self, mock_client_class):
        """Testa o comportamento do serviço simulando a API do Ollama via mock."""
        mock_instance = MagicMock()
        mock_instance.chat.return_value = {
            "message": {
                "content": "Excelente postagem! Conteúdo muito relevante e importante para a nossa comunidade de tecnologia. Valeu!"
            }
        }
        mock_client_class.return_value = mock_instance

        service = OllamaService()
        comment = service.generate_comment("Postagem sobre arquitetura de software e C#.")

        self.assertIsInstance(comment, str)
        self.assertTrue(len(comment) > 10)

    def test_integration_generate_comment_with_ollama(self):
        """Teste de integração real com o servidor Ollama (Llama 3.2)."""
        sample_post = """Tem muita IA, muito framework e muita novidade. Mas como tudo isso se conecta no desenvolvimento de software?
No AI na Prática, vamos conversar com especialistas, de desenvolvedores a CTOs, para entender como aplicar IA em todas as etapas da engenharia de software.
A ideia é mostrar como a IA pode apoiar toda a jornada, do upstream ao downstream, com experiências reais e sem hype.
As lives são gratuitas, ao vivo e abertas para perguntas e as 19h"""
        comment = self.service.generate_comment(sample_post)
        print(comment)

        self.assertIsInstance(comment, str)
        self.assertTrue(len(comment) >= 100)
        self.assertTrue(len(comment) <= 140)


if __name__ == "__main__":
    unittest.main()

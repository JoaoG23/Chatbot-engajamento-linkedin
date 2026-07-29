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
        sample_post = """A discussão sobre reforma tributária costuma girar em torno de alíquotas, regras e legislação. Mas, na prática, a transformação será muito mais ampla.
Em conversa com Priscila Rossini, da Accenture, Rosana Jayme, Superintendente Executiva de Gestão Fiscal no Santander Brasil, compartilha a visão de quem está conduzindo a preparação de uma das maiores instituições financeiras do país para esse novo cenário.
Elas falam sobre o desafio de revisar processos ponta a ponta, o impacto da reforma sobre dados, tecnologia e operações, a necessidade de coordenação entre áreas que historicamente trabalhavam de forma separada e o tamanho da mudança que as organizações terão de absorver nos próximos anos.
👉 Assista ao conteúdo completo no YouTube: https://accntu.re/4foJyoF"""
        comment = self.service.generate_comment(sample_post)
        print(comment)

        self.assertIsInstance(comment, str)
        self.assertTrue(len(comment) > 10)


if __name__ == "__main__":
    unittest.main()

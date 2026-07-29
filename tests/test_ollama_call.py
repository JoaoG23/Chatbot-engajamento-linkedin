import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.ollama_service import OllamaService


def test_ollama():
    sample_posts = [
        "Estou muito feliz em anunciar que nossa equipe concluiu com sucesso a implementação de um projeto inovador com IA e Automação.",
        "Dica de hoje sobre C# e ASP.NET: evite NullReferenceException com boas práticas de validação no seu backend.",
        "Projeto incrível de React Native lançado essa semana com alta performance e animações fluidas!",
    ]

    ollama_service = OllamaService()
    for i, post in enumerate(sample_posts, 1):
        comment = ollama_service.generate_comment(post)
        print(f"\n--- Post {i} ---")
        print(f"Comentário ({len(comment)} chars):\n'{comment}'")


if __name__ == "__main__":
    test_ollama()

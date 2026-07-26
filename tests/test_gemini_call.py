import os
import sys

# Adiciona o diretório raiz ao sys.path para importação dos módulos do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.gemini_service import GeminiService

def test_gemini():
    gemini = GeminiService()
    sample_post = "Dicas avançadas de arquitetura C# e ASP.NET com React Native no mobile"
    comment = gemini.generate_comment(sample_post)
    print(f"\n[Teste Gemini] Comentário gerado:\n'{comment}'")

if __name__ == "__main__":
    test_gemini()

# Bot de Comentador para LinkedIn 🤖

Automação inteligente e humanizada para o LinkedIn desenvolvida em **Python** utilizando **Playwright** e a IA local **Ollama (Llama 3.2)**. O robô é capaz de conectar a uma sessão ativa do Chrome, analisar as postagens do seu feed, gerar comentários contextuais e relevantes de forma automatizada com base em sua persona/currículo e registrar o histórico para evitar duplicatas.

---

## 1. Tecnologias Utilizadas 🛠

* **Automação de Navegador:** [Playwright](https://playwright.dev/) (mais rápido e seguro que o Selenium)
* **Inteligência Artificial Local:** [Ollama Python SDK](https://github.com/ollama/ollama-python) rodando o modelo **Llama 3.2**
* **Linguagem:** [Python](https://www.python.org/)
* **Controle de Progresso:** [tqdm](https://github.com/tqdm/tqdm) (barra de progresso interativa no terminal)
* **Outros:** `python-dotenv` para variáveis de ambiente e `hashlib` para criptografia (deduplicação)

---

## 2. Fluxo da Aplicação 🔧

1. **Conexão/Login:**
   * O robô tenta se conectar a uma janela ativa do Google Chrome utilizando o protocolo **CDP (Chrome DevTools Protocol)** na porta `9222`. Isso permite usar sua sessão já logada sem precisar fazer login toda vez.
   * Caso não consiga, ele inicia uma nova instância do navegador e realiza o login automático utilizando as credenciais fornecidas no arquivo `.env`.
2. **Navegação e Leitura:**
   * Acessa a página inicial do feed do LinkedIn.
   * Realiza rolagem automática para carregar novas postagens.
3. **Análise de Conteúdo (Evitando Duplicatas):**
   * Extrai o texto da publicação e gera um **hash MD5** exclusivo a partir dos primeiros 200 caracteres do post.
   * Verifica se o hash já existe no arquivo [commented_posts_history.json](file:///n:/github/Chatbot-engajamento-linkedin/commented_posts_history.json). Se já existir ou se um comentário seu já for detectado na postagem, ela é pulada automaticamente.
4. **Geração de Comentário pela IA:**
   * Envia o texto da postagem para o Ollama local (modelo `llama3.2`) junto com as regras de persona e diretrizes configuradas no [persona.txt](file:///n:/github/Chatbot-engajamento-linkedin/persona.txt).
   * O Ollama gera um comentário profissional personalizado.
5. **Publicação:**
   * O robô clica no campo de comentário do post, insere a resposta gerada e clica em publicar.
   * O hash do post é registrado no arquivo de histórico local para garantir que nunca seja comentado de novo.

---

## 3. Estrutura do Projeto 📂

Para uma descrição detalhada de cada módulo, consulte a [DOCUMENTACAO.md](file:///n:/github/Chatbot-engajamento-linkedin/DOCUMENTACAO.md). A estrutura simplificada é:

* `main.py`: Ponto de entrada e orquestrador principal do robô.
* `config.py`: Arquivo de configurações globais e variáveis de ambiente.
* `persona.txt`: Persona e regras fornecidas para a IA formular as respostas.
* `commented_posts_history.json`: Histórico persistente de hashes MD5 dos posts comentados.
* `services/`: Módulos de interação com o navegador (`browser_service.py`), integração com a IA local (`ollama_service.py`) e interações no LinkedIn (`linkedin_service.py`).
* `utils/`: Módulos para limpeza de texto (`text_cleaner.py`) e controle de histórico (`history_manager.py`).

---

## 4. Como Instalar 👨🏽‍💻

### Pré-requisitos
* Python 3.10 ou superior
* Google Chrome instalado
* Ollama instalado com o modelo `llama3.2` baixado (`ollama run llama3.2`)

### Passo a Passo

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/JoaoG23/Chatbot-engajamento-linkedin.git
   cd Chatbot-engajamento-linkedin
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Instale os binários do Playwright:**
   ```bash
   playwright install
   ```

4. **Configure o arquivo `.env`:**
   Crie um arquivo `.env` na raiz do projeto e configure as seguintes variáveis:
   ```env
   OLLAMA_HOST="http://localhost:11434"
   OLLAMA_MODEL="llama3.2"
   LINKEDIN_EMAIL="seu_email_do_linkedin"
   LINKEDIN_PASSWORD="sua_senha_do_linkedin"
   CDP_URL="http://127.0.0.1:9222"
   LIMIT_COMMENTS=25
   ```

---

## 5. Como Usar 😃

### Modo Recomendado (Via CDP com seu navegador ativo)

Para que o robô use seu perfil já conectado do Chrome (evitando verificações de segurança/2FA do LinkedIn):

1. **Feche todas as janelas do Chrome** completamente.
2. Abra o Chrome via terminal ou Prompt de Comando com a depuração remota ativada:
   * **Windows:**
     ```cmd
     chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\ChromeDebug"
     ```
   * **macOS / Linux:**
     ```bash
     google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/ChromeDebug"
     ```
3. Acesse o LinkedIn no navegador aberto por esse comando e certifique-se de que está logado na sua conta.
4. Certifique-se de que o **Ollama** está em execução na sua máquina.
5. Execute o bot no terminal do seu projeto:
   ```bash
   python main.py
   ```

O bot começará a rodar no terminal, mostrando uma barra de progresso para acompanhar o envio de cada comentário até atingir o limite configurado em `LIMIT_COMMENTS`.

---

## 6. Autor do Projeto

<img style="border-radius:50%;" src="https://avatars.githubusercontent.com/u/80895578?v=4" width="100px;" alt="João Guilherme"/>
<br />
<sub><b>Joao Guilherme</b></sub> <a href="https://github.com/JoaoG23/">🚀</a>

Feito com ❤️ por Joao Guilherme 👋🏽 Entre em contato:

[![Linkedin Badge](https://img.shields.io/badge/-Joao%20Guilherme-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/joaog123/)](https://www.linkedin.com/in/joaog123/)
[![Email Badge](https://img.shields.io/badge/-joaoguilherme94@live.com-c80?style=flat-square&logo=Microsoft&logoColor=white&link=mailto:joaoguilherme94@live.com)](mailto:joaoguilherme94@live.com)

---

## 7. Licença 📝

Este projeto está licenciado sob a licença descrita no arquivo [LICENSE](./LICENSE).

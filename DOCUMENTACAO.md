# 📘 Documentação do Sistema de Automação do LinkedIn

Este documento detalha a arquitetura, a responsabilidade de cada pasta e o funcionamento de cada arquivo do projeto de automação do LinkedIn com **Playwright** e **Ollama (Llama 3.2)**.

---

## 📂 Estrutura de Arquivos e Pastas

```text
Chatbot-engajamento-linkedin/
│
├── .env                            # Variáveis de ambiente (Host e Modelo Ollama, Credenciais)
├── requirements.txt                # Lista de dependências Python do projeto
├── config.py                       # Módulo central de configurações
├── main.py                         # Ponto de entrada principal da aplicação (Orquestrador)
├── data/
│   ├── persona.txt                 # Instruções principais, perfil profissional e regras para a IA
│   ├── exemplares.txt              # Exemplos de postagens e respostas ideais para Few-Shot Prompting
│   └── commented_posts_history.json# Histórico persistente em JSON dos hashes dos posts comentados
│
├── services/                       # Camada de Serviços de Negócio
│   ├── __init__.py                 # Inicializador do pacote de serviços
│   ├── browser_service.py          # Gerenciador do Navegador (Conexão CDP ou Login manual/automatizado)
│   ├── ollama_service.py           # Serviço de integração com o servidor local Ollama (Llama 3.2)
│   └── linkedin_service.py         # Serviço de raspagem e automação do Feed do LinkedIn (Clean Code)
│
├── utils/                          # Camada de Utilitários e Helpers
│   ├── __init__.py                 # Inicializador do pacote de utilitários
│   ├── history_manager.py          # Gerenciador de histórico e geração de Hashes MD5
│   └── text_cleaner.py             # Funções de higienização de texto e emojis
│
└── tests/                          # Suíte de Testes e Diagnósticos
    ├── __init__.py                 # Inicializador do pacote de testes
    ├── check_user_name.py          # Inspeção de perfil do usuário no LinkedIn
    ├── inspect_comment_box_detail.py# Inspeção detalhada do DOM da caixa de comentário
    ├── inspect_feed.py             # Inspeção de estrutura do feed
    ├── test_ollama_call.py         # Teste isolado das chamadas ao Ollama (Llama 3.2)
    └── test_submit.py              # Teste isolado do clique no botão de publicação
```

---

## 🛠️ Detalhamento dos Componentes Principais

### 1. `config.py`
**Responsabilidade:** Centralizar todas as configurações e variáveis globais do projeto.
- **Principais variáveis:**
  - `OLLAMA_HOST`: URL do servidor local do Ollama (`http://localhost:11434`).
  - `OLLAMA_MODEL`: Modelo da IA local (`llama3.2`).
  - `LINKEDIN_EMAIL` / `LINKEDIN_PASSWORD`: Credenciais para login opcional.
  - `CDP_URL`: URL do protocolo DevTools do Chrome (`http://localhost:9222`).
  - `HISTORY_FILE`: Caminho para o arquivo de histórico de posts comentados.
  - `PROMPT_FILE`: Caminho do arquivo de prompt da IA (`data/persona.txt`).

---

## 2. Módulo de Serviços (`services/`)

#### 🔹 `services/browser_service.py`
**Responsabilidade:** Gerenciar a conexão e ciclo de vida do navegador via Playwright (`async_api`).
- **Principais funções:**
  - `connect_existing_chrome(...)`: Conecta diretamente à sessão já aberta do seu navegador Chrome (através do porta 9222/CDP), reaproveitando o login existente sem abrir novas janelas.
  - `launch_new_browser(...)`: Abre uma nova instância limpa do Chromium/Chrome.
  - `do_login(page, email, password)`: Executa o fluxo automatizado de login na página inicial do LinkedIn (`https://www.linkedin.com/home`), preenchendo os campos de e-mail, senha e submetendo o formulário.

#### 🔹 `services/ollama_service.py`
**Responsabilidade:** Gerar respostas inteligentes, personalizadas e humanizadas utilizando o servidor local do **Ollama** com o modelo **Llama 3.2**.
- **Principais funções:**
  - `_read_prompt()`: Lê as instruções e diretrizes do arquivo `data/persona.txt`.
  - `generate_comment(content_post)`: Conecta ao Ollama via SDK `ollama-python`, envia o prompt do sistema e o texto da publicação, higieniza a resposta gerada e inclui um sistema de contingência/fallback automático.

#### 🔹 `services/linkedin_service.py`
**Responsabilidade:** Automatizar a navegação no feed do LinkedIn e a postagem de comentários (Estruturado conforme princípios de Clean Code).
- **Principais funções:**
  - `_record_history(post_hash)`: Adiciona o hash ao conjunto em memória e persiste em disco via `save_history`.
  - `_should_skip_post(post_index, post_hash)`: Verifica se o post deve ser ignorado (histórico local ou comentário prévio detectado no DOM).
  - `_scroll_page(times, delay)`: Executa rolagens de tela (`PageDown`) com atraso configurável.
  - `_process_single_post(post_index, btn, pbar)`: Gerencia o ciclo completo de processamento de um post (expansão, extração, geração de comentário via OllamaService, submissão e atualização da barra de progresso).
  - `process_feed_comments(target_count=25)`: Orquestrador principal de alto nível para o loop no feed.

---

## 3. Módulo de Utilitários (`utils/`)

#### 🔹 `utils/text_cleaner.py`
**Responsabilidade:** Formatação e limpeza de strings.
- **Funções:**
  - `remove_linebreak_text(text)`: Substitui múltiplas quebras de linha e espaços extras por um espaço simples.
  - `remove_emojis_text(text)`: Remove emojis do texto usando Regex sem afetar os caracteres acentuados da língua portuguesa (á, é, í, ó, ú, ç, ã, etc.).

#### 🔹 `utils/history_manager.py`
**Responsabilidade:** Manter a persistência de posts já comentados para evitar duplicatas.
- **Funções:**
  - `load_history()`: Lê o arquivo `commented_posts_history.json`.
  - `save_history(history_set)`: Grava os hashes atualizados no disco em formato JSON.
  - `get_post_hash(text)`: Gera uma assinatura digital única (**Hash MD5**) dos primeiros 200 caracteres da postagem.

---

## 4. Orquestrador e Arquivos de Suporte

#### 🔹 `main.py`
**Responsabilidade:** Ponto de entrada da aplicação.
- Inicializa o Playwright assíncrono (`asyncio`).
- Decide entre conectar ao Chrome em execução via CDP ou realizar o login manual/automático.
- Instancia os serviços (`OllamaService` e `LinkedInService`) e inicia o processamento do feed.

#### 🔹 `data/persona.txt`
**Responsabilidade:** Definir a persona, o perfil profissional, experiências e regras para a IA em formato de texto.
- Contém a persona ("Desenvolvedor Fullstack"), histórico profissional (experiências passadas), stacks (C#, React, Python, NestJS, etc.) e regras (respostas de 120-180 caracteres, sem emojis, em PT-BR).

#### 🔹 `commented_posts_history.json`
**Responsabilidade:** Base de dados local em JSON armazenando a lista de hashes MD5 dos posts já comentados.

#### 🔹 `.env`
**Responsabilidade:** Armazenamento de variáveis de ambiente (`OLLAMA_HOST`, `OLLAMA_MODEL`) e credenciais de acesso.

---

## 🧪 Scripts de Teste e Inspeção (Utilitários)

- `test_ollama_call.py`: Script isolado para validar a integração e geração do Ollama (Llama 3.2).
- `test_submit.py`: Script para testar a localização e o clique no botão de confirmação do comentário no LinkedIn.
- `inspect_feed.py` & `inspect_comment_box_detail.py`: Scripts de depuração para inspecionar elementos do DOM do LinkedIn.
- `check_user_name.py`: Script de depuração para verificar elementos da barra de navegação do LinkedIn.

---

## 🚀 Como Executar o Projeto

Para executar a automação completa conectada ao seu Chrome ativo:

```bash
python main.py
```

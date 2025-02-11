# Bot Engajamento linkedin

🧲 Desenvolver um bot de engajamento para o LinkedIn que funcione da seguinte forma: ao inserir um nome na barra de pesquisa, o sistema acessa as publicações, analisa o conteúdo com base em um prompt e, automaticamente, adiciona um comentário curto (máximo de 60 caracteres) e um 'gostei' 👍🏽

**Tempo: 17**

## 1. Tecnologias Utilizadas 🛠

**Automatização** 🤖

[![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![GeminiAI](https://img.shields.io/badge/GeminiAI-FF6600?style=for-the-badge&logo=ai&logoColor=white)]()
![Chrome Web Store](https://img.shields.io/badge/Chrome-Web%20Store-blue?style=for-the-badge&logo=google-chrome)
![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=for-the-badge&logo=linkedin&logoColor=white)


## 2. Fluxo da Aplicação 🔧

✅ **0. Acessar tela de login LinkedIn e preencher usuário e senha**

✅ **1. Preencher a barra de pesquisa com a (__descrição__) buscada**

✅ **2. Entrar em cada postagem e capturar o texto dela com o assunto**

✅ **3. Clicar em gostei na postagem**

✅ **4. Enviar para AI Gemini, com o prompt requerido**

✅ **5. Capturar a resposta da AI Gemini**

✅ **6. Preencher o comentário com base na resposta da AI Gemini**

✅ **7. Enviar comentário**

✅ **8. Inserir postagem e comentário nos logs para controle**.

## 3. Como Instalar 👨🏽‍💻

### Backend

1. Clone este repositório;
2. Instale as dependências utilizando `pip install -r requirements.txt`;
3. Configure as variáveis de ambiente no arquivo `.env`:

```
DESCRIPTION="sobre spring boot"
USER_LINKEDIN="email@emai.com" 
PASSWORD_LINKEDIN="2393932" 
COMMENT_LIMIT=10 # Limite de conexoes
AI_TOKEN='token'
```

4. Execute o bot com `python __init__.py`.

## 4. Como Usar 😃

1. Acesse o LinkedIn e faça login com um usuário válido;
2. No terminal, insira a palavra-chave desejada para busca;
3. O bot navegará automaticamente, curtindo e comentando nas postagens até o limite estabelecido na variavel `COMMENT_LIMIT=10`;
4. Os logs serão armazenados para análise posterior.

## 5. Autor do Projeto

 <img style="border-radius:50%;" src="https://avatars.githubusercontent.com/u/80895578?v=4" width="100px;" alt=""/>
 <br />
 <sub><b>Joao Guilherme</b></sub></a> <a href="https://github.com/JoaoG23/">🚀</a>

Feito com ❤️ por Joao Guilherme 👋🏽 Entre em contato pelos links abaixo!

[![Linkedin Badge](https://shields.io/badge/-Joao%20Guilherme-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/joaog123/)](https://www.linkedin.com/in/joaog123/)

[![Email Badge](https://shields.io/badge/-joaoguilherme94@live.com-c80?style=flat-square&logo=Microsoft&logoColor=white&link=mailto:joaoguilherme94@live.com)](mailto:joaoguilherme94@live.com)

## 6. Licença 📝

[![License](https://shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)


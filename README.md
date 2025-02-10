# Chatbot-engajamento-linkedin

🧲Desenvolver um bot de engajamento para o LinkedIn que funcione da seguinte forma: ao inserir um nome na barra de pesquisa, o sistema acessará as publicações, analisará o conteúdo com base em um prompt e, automaticamente, adicionará um comentário curto (máximo de 80 caracteres) e um 'gostei' 👍🏽

Tempo de desenvolvimento: 10
🛠 Tecnologias:

✅ Selenium – Para navegar pelo LinkedIn e interagir com as postagens.

✅ OpenAI API – Para gerar comentários curtos com base no conteúdo da postagem.

✅ Requests + BeautifulSoup (Opcional) – Para scraping de dados (caso queira evitar Selenium).

🔧 Passos para o funcionamento do bot:


[x] 1. Acessar tela de login e preencher usuário e senha;

[x] 2. Preencher a barra de pesquisa com a (__descrição__) buscada;

[x] 3. Entrar em cada postagem capturar o **texto** dela com o assunto;

[] 4. Enviar para **AI Gemini**, com o prompt requirido;

[] 5. Capturar a resposta **AI Gemini**;

[x] 6. Preencher o comentário com base na resposta do **AI Gemini**;

[x] 7. Enviar comentário;

[] 8. Inserir **postagem** e **comentário** nos logs para controle;


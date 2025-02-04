# Chatbot-engajamento-linkedin
🧲Desenvolver um bot de engajamento para o LinkedIn que funcione da seguinte forma: ao inserir um nome na barra de pesquisa, o sistema acessará as publicações, analisará o conteúdo com base em um prompt e, automaticamente, adicionará um comentário curto (máximo de 80 caracteres) e um 'gostei' 👍🏽

🛠 Tecnologias:
✅ Selenium – Para navegar pelo LinkedIn e interagir com as postagens.
✅ OpenAI API – Para gerar comentários curtos com base no conteúdo da postagem.
✅ Requests + BeautifulSoup (Opcional) – Para scraping de dados (caso queira evitar Selenium).

🔧 Passos para o funcionamento do bot:
1️⃣ Login no LinkedIn – O bot precisa acessar sua conta (pode usar autenticação manual ou cookies salvos).
2️⃣ Pesquisa pelo nome – O sistema faz uma busca pelo nome na barra de pesquisa.
3️⃣ Acessa as postagens – Abre cada postagem do usuário.
4️⃣ Analisa o conteúdo – Extrai o texto da publicação.
5️⃣ Gera um comentário curto – Usa a OpenAI API para criar um comentário de até 80 caracteres.
6️⃣ Publica o comentário – Escreve o comentário e envia.
7️⃣ Dá um ‘gostei’ – Clica no botão de ‘curtir’ na postagem.

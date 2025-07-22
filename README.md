# 🤖 BotManager

**BotManager** é um bot para Discord feito em Python que permite gerenciar e interagir com múltiplos aplicativos de forma simples.

---

## 🚀 Funcionalidades principais

- **Sistema de whitelist:**  
  Usuários que não estiverem na whitelist, ao tentar usar o comando `/upload`, recebem um QR Code para pagamento via PIX.
- **Geração automática de QR Code:**  
  O bot gera e envia o QR Code para o pagamento PIX diretamente no Discord.
- **Webhook de pagamento:**  
  Recebe atualizações em tempo real sobre o status do pagamento via webhook.
- **Notificação automática:**  
  Ao confirmar o pagamento, o bot envia uma mensagem direta ao usuário que gerou o QR Code liberando o upload.

---

---

## 🚀 Comandos

- `/upload` — Comando para enviar/upload de uma aplicacão
- `/status` — Comando para verificar o status de uma aplicacão, também com autocomplete para selecionar o app.

---

## 🧰 Tecnologias usadas

- [Python 3.13](https://www.python.org/)
- [discord.py (v2.5.2)](https://discordpy.readthedocs.io/)
- [aiohttp (0.21.0)](https://docs.aiohttp.org/en/stable/)
- [squarecloud-api](https://github.com/squarecloudofc/sdk-api-py)
- [pillow](https://pypi.org/project/pillow/)
- [aisqlite](https://aiosqlite.omnilib.dev/en/stable/api.html)

---

## 📦 Instalação

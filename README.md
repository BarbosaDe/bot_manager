# 🤖 BotManager

**BotManager** é um bot para Discord feito em Python que permite gerenciar e interagir com múltiplos aplicativos de forma simples.

---

## ✨ Funcionalidades principais

- **Sistema de whitelist:**  
  Usuários que não estiverem na whitelist, ao tentar usar o comando `/upload`, recebem um QR Code para pagamento via PIX.

- **Geração automática de QR Code:**  
  O bot gera e envia o QR Code para o pagamento PIX diretamente no Discord.
- **Webhook de pagamento:**  
  Recebe atualizações em tempo real sobre o status do pagamento via webhook.

- **Notificação automática:**  
  Ao confirmar o pagamento, o bot envia uma mensagem direta ao usuário que gerou o QR Code liberando o upload.

---

## 🚀 Comandos

- `/upload` — Comando para enviar/upload de uma aplicacão
- `/status` — Comando para verificar o status de uma aplicação (serão listadas apenas suas aplicações)
- `/config` — Comando para enviar um painel para configurar os planos
- `/comprar-plano` — Comando para comprar um plano

---

## ✨ Comandos detalhados

## `/upload`

Ao enviar sua aplicação, o deploy será realizado automaticamente **caso ela contenha um arquivo de configuração** (`squarecloud.app` ou `squarecloud.config`).

Se **não houver arquivo de configuração**, será exibido um painel perguntando se a aplicação é um website. Após selecionar uma opção, um modal será exibido com as **configurações básicas**:

- Nome da aplicação
- Arquivo principal
- Memória máxima
- Subdomínio (caso seja um website)

Se todas as informações forem preenchidas corretamente, o deploy será iniciado.

> 💡 Para configurações mais avançadas, utilize um dos arquivos de configuração:  
> `squarecloud.app` ou `squarecloud.config`.

## `/comprar-plano`

Ao utilizar esse comando, será exibido um **menu de seleção** (Select Menu), onde será possível escolher o plano desejado.  
Cada opção do menu exibirá as seguintes informações:

- **Nome do plano**
- **Valor**
- **Memória RAM máxima**

Após selecionar um plano, serão gerados:

- Um **QR Code** para pagamento
- Um **código "copia e cola"** para facilitar o pagamento via PIX

- Basta realizar o pagamento para concluir a compra.

## 🧰 Tecnologias usadas

- [Python 3.13](https://www.python.org/)
- [discord.py (v2.5.2)](https://discordpy.readthedocs.io/)
- [aiohttp (0.21.0)](https://docs.aiohttp.org/en/stable/)
- [squarecloud-api (3.7.4)](https://github.com/squarecloudofc/sdk-api-py)
- [pillow (11.3.0)](https://pypi.org/project/pillow/)
- [aisqlite (0.21.0)](https://aiosqlite.omnilib.dev/en/stable/api.html)

---

## 📦 Instalação

# Local

```bash

# Clone o repositorio
git clone https://github.com/BarbosaDe/bot_manager.git

# Acesse o diretorio
cd bot_manager

# Instale as dependencias
pip install .

# Execute o bot
python build/lib/main.py

```

# SquareCloud

1. Baixe o arquivo `.zip` neste link:  
   [bot_manager.zip](https://github.com/BarbosaDe/bot_manager/releases/download/1.0/bot_manager.zip)

2. Acesse o painel de upload do SquareCloud:  
   https://squarecloud.app/pt-br/dashboard/upload?type=archive

3. Clique em **"Selecione um arquivo .zip"** e escolha o arquivo baixado.

4. Configure seu bot conforme desejar, ajuste as variáveis de ambiente e clique em **"Enviar aplicação"**.

---

_💡 Lembre-se de configurar seu .env. Use .env.example como referência._

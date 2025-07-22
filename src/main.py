import asyncio
import logging
import os
from pathlib import Path

import discord
from aiohttp import web
from discord.ext import commands
from dotenv import load_dotenv

from database import Database, Transaction, Whitelist
from payments import Payment

load_dotenv()

COGS_DIR = Path(__file__).parent / "cogs"


discord.utils.setup_logging(level=logging.INFO)
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)
webhook = web.Application()


async def load_extensions():
    for file in os.listdir(COGS_DIR):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")


@bot.event
async def on_ready():
    print("[on_ready] Bot Pronto.")

    await bot.tree.sync()


@bot.event
async def setup_hook():
    print("[setup_hook] Iniciando bot...")

    await Database.init_db()
    print("[setup_hook] Banco de dados pronto.")

    await load_extensions()
    print("[setup_hook] Extensões carregadas.")

    await bot.tree.sync()
    print("[setup_hook] Slash commands sincronizados.")


async def notifications(request: web.Request):
    try:
        queryparams = request.rel_url.query

        payment_id = queryparams.get("data.id")

        payment = await Payment.get(payment_id)

        if payment["status"] == "approved":
            transaction = await Transaction.get(payment_id)

            await transaction.change_status(payment_id, "success")

            payer_id = transaction.payer_id

            await Whitelist.create(payer_id, 1)

            server = await bot.fetch_guild(transaction.server_id)
            user = await server.fetch_member(payer_id)

            await user.send(content="Seu pagamento foi aprovado.")

    except Exception as e:
        print(f"[WEBHOOK ERROR: {e}]")

    finally:
        return web.Response(status=200, text="OK!")


webhook.add_routes([web.post("/notifications", notifications)])


async def main():
    runner = web.AppRunner(webhook)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 5000)
    await site.start()

    print("[Webhook] Servidor iniciado em http://127.0.0.1:5000")

    await bot.start(os.environ["BOT_TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import os
from pathlib import Path

import discord
from aiohttp import web
from discord.ext import commands
from dotenv import load_dotenv

from database import Database
from database.models import Plan, User
from database.repository import TransactionRepository, UserRepository
from payments import payment_service
from utils.logger import logger

load_dotenv()

COGS_DIR = Path(__file__).parent / "cogs"

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)
webhook = web.Application()


async def load_extensions():
    for file in os.listdir(COGS_DIR):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")


@bot.event
async def on_ready():
    logger.info("[on_ready] Bot Pronto.")

    await bot.tree.sync()


@bot.event
async def setup_hook():
    logger.info("[setup_hook] Iniciando bot...")

    await Database.init_db()
    logger.info("[setup_hook] Banco de dados pronto.")

    await load_extensions()
    logger.info("[setup_hook] Extensões carregadas.")

    await bot.tree.sync()
    logger.info("[setup_hook] Slash commands sincronizados.")


async def send_confirmation_payment(server_id, payer_id):
    server = await bot.fetch_guild(server_id)
    user = await server.fetch_member(payer_id)

    embed = discord.Embed(
        title="✅ Plano adquirido com sucesso!",
        description="Você adquiriu o plano **tanana**.",
        color=discord.Color.green(),
    )

    embed.add_field(name="💰 Preço", value="R$ 20.00", inline=True)
    embed.add_field(name="🧠 RAM máxima", value="20244 MB", inline=True)
    embed.set_footer(text="Obrigado por escolher nossos serviços!")
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/190/190411.png")

    await user.send(embed=embed)


async def notifications(request: web.Request):
    try:
        queryparams = request.rel_url.query

        payment_id = queryparams.get("data.id")

        payment = await payment_service.get(payment_id)

        if payment["status"] == "approved":
            transaction = await TransactionRepository.get(payment_id)

            plan = Plan(id=transaction.plan)
            user = User(user_id=transaction.payer_id, plan=plan)

            await asyncio.gather(
                TransactionRepository.change_status(transaction),
                UserRepository.insert(user),
            )

            return await send_confirmation_payment(
                transaction.server_id, transaction.payer_id
            )

    except Exception:
        logger.critical("Erro verificar/atualizar status do pagamento", exc_info=True)

    finally:
        return web.Response(status=200, text="OK!")


webhook.add_routes([web.post("/notifications", notifications)])


async def main():
    runner = web.AppRunner(webhook)
    await runner.setup()
    site = web.TCPSite(runner, HOST, PORT)
    await site.start()

    logger.info(f"[Webhook] Servidor iniciado em http://{HOST}:{PORT}")

    await bot.start(os.environ["BOT_TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())

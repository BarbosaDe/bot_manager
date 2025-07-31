from discord import Color, Embed

from database.repository import ApplicationRepository
from exceptions import get_translated_exception_message
from services.square_manager import square_manager


async def handle_application_upload(zip: bytes, owner: int) -> Embed:
    try:
        response = await square_manager.upload_application(zip, owner)

        embed = Embed(
            title="✅ Aplicação Enviada com Sucesso!",
            description=response.description
            or "Sua aplicação foi processada com sucesso.",
            color=Color.green(),
        )

        embed.add_field(name="🆔 ID", value=response.id, inline=False)
        embed.add_field(name="📦 Nome", value=response.name, inline=True)
        embed.add_field(
            name="💻 Linguagem", value=response.language["name"], inline=True
        )
        embed.add_field(name="🧠 RAM", value=f"{response.ram} MB", inline=True)
        embed.add_field(name="⚙️ CPU", value=f"{response.cpu} vCPU", inline=True)

        if response.domain:
            embed.add_field(name="🌐 Domínio", value=response.domain, inline=False)

        return embed
    except Exception as e:
        msg = get_translated_exception_message(e)

        return Embed(
            title="❌ Erro ao enviar aplicação",
            description=msg,
            color=Color.red(),
        )


async def chack_ram_limit(user, config):
    apps = await ApplicationRepository.list(user.user_id)

    if not apps:
        return

    ram_used = sum((app.ram for app in apps))

    if ram_used + config.memory > user.plan.max_ram:
        return Embed(
            title="❌ Erro de Recursos",
            description="A aplicação requer mais memória RAM do que o disponível.",
            color=Color.red(),
        )

import asyncio

import discord
from discord.ext import commands

from database.repository.user_repository import UserRepository
from square_manager import square_manager
from ui.buttons_is_website import WebsiteButtons
from utils.cache import Cache
from utils.config_parser import get_squarecloud_config


class UploadCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="upload", description="Hospede sua aplicacão")
    async def callback(
        self,
        interaction: discord.Interaction,
        arquivo: discord.Attachment,
    ):
        if arquivo.size > 100 * 1024 * 1024:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="❌ Arquivo muito grande",
                    description="O arquivo ultrapassa o limite de 100 MB.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )

        if arquivo.content_type != "application/zip":
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="❌ Tipo de arquivo inválido",
                    description="Apenas arquivos `.zip` são permitidos. Por favor, envie um arquivo compactado válido.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )

        _, user = await asyncio.gather(
            interaction.response.defer(thinking=True, ephemeral=True),
            UserRepository.get(interaction.user.id),
        )

        if not user.expired:
            return await interaction.edit_original_response(
                embed=discord.Embed(
                    title="🚫 Nenhum plano ativo encontrado",
                    description=(
                        "Parece que você ainda não possui um plano ativo. Para começar a subir seus projetos, "
                        "use o comando /planos e escolha o que melhor se encaixa no seu uso! 💡"
                    ),
                    color=discord.Color.red(),
                ),
            )

        zip_bytes = await arquivo.read()
        Cache.insert(interaction.user.id, zip_bytes)
        config = get_squarecloud_config(zip_bytes)

        if config:
            response = await square_manager.upload_application(zip_bytes, "Foo")
            return await interaction.edit_original_response(content=response)

        embed = discord.Embed(
            title="🌐 Sua aplicação é um website?",
            description="Responda se a aplicação que está enviando é um site acessível por navegador.",
            color=discord.Color.blurple(),
        )

        return await interaction.edit_original_response(
            embed=embed, view=WebsiteButtons()
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(UploadCog(bot))

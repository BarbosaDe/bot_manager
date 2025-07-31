import asyncio

import discord
from discord.ext import commands

from database.repository.user_repository import UserRepository
from services.uploader_service import chack_ram_limit, handle_application_upload
from ui.upload.buttons_is_website import WebsiteButtons
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

        # Verifica se o usuario existe e se seu plano esta expirado
        if not user or user.expired:
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

        # Se não tiver inicia o processo de configuracão da aplicacão
        if not config:
            embed = discord.Embed(
                title="🌐 Sua aplicação é um website?",
                description="Responda se a aplicação que está enviando é um site acessível por navegador.",
                color=discord.Color.blurple(),
            )

            return await interaction.edit_original_response(
                embed=embed, view=WebsiteButtons()
            )

        ram_exceeded = await chack_ram_limit(user, config)

        if ram_exceeded:
            return await interaction.edit_original_response(embed=ram_exceeded)

        embed = await handle_application_upload(zip_bytes, interaction.user.id)

        await interaction.edit_original_response(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(UploadCog(bot))

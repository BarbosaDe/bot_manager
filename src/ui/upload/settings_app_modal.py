import discord
from squarecloud.utils import ConfigFile

from database.repository import UserRepository
from services.uploader_service import chack_ram_limit, handle_application_upload
from utils.cache import Cache
from utils.config_parser import insert_squarecloud_config


class SettingsSquareApp(discord.ui.Modal):
    def __init__(self, website: bool):
        super().__init__(title="Configurações do Projeto", timeout=None)

        self.website = website

        self.name = discord.ui.TextInput(label="Nome do projeto", max_length=32)
        self.main = discord.ui.TextInput(
            label="Arquivo principal do projeto", required=False
        )
        self.memory = discord.ui.TextInput(
            label="RAM (MB)", default=512 if website else 256
        )

        self.subdomain = None
        if website:
            self.subdomain = discord.ui.TextInput(label="Subdomínio do projeto")

        self.add_item(self.name)
        self.add_item(self.main)
        self.add_item(self.memory)
        if self.subdomain:
            self.add_item(self.subdomain)

    async def on_submit(self, interaction: discord.Interaction):
        if not self.memory.value.isdecimal():
            return await self._send_error(
                interaction,
                title="Valor de Memória Inválido",
                description="💾 A memória deve ser um número em megabytes (MB).",
                color=0xFAA61A,
            )

        config = {
            "display_name": self.name.value,
            "main": self.main.value,
            "memory": int(self.memory.value),
        }
        if self.subdomain:
            config["subdomain"] = self.subdomain.value

        await interaction.response.defer(thinking=True, ephemeral=True)
        try:
            config_file = ConfigFile(**config)

            user = await UserRepository.get(interaction.user.id)

            ram_exceeded = await chack_ram_limit(user, config)

            if ram_exceeded:
                return await interaction.edit_original_response(embed=ram_exceeded)

            zip_bytes = Cache.get(interaction.user.id)

            if not zip_bytes:
                return await self._send_error(
                    interaction,
                    "Erro",
                    "Arquivo não encontrado. Envie-o novamente.",
                    0xED4245,
                )

            new_zip = insert_squarecloud_config(
                zip_bytes, "squarecloud.app", config_file.content().encode()
            )

            embed = await handle_application_upload(new_zip, interaction.user.id)
            await interaction.edit_original_response(embed=embed)

        except ValueError as e:
            error_message = str(e).lower()

            if "memory" in error_message:
                return await self._send_error(
                    interaction,
                    title="Requisitos de Memória",
                    description="🔹 **Memória mínima:** 256 MB\n🔹 **Para websites:** mínimo de 512 MB",
                    color=0x5865F2,
                )
            elif "version" in error_message:
                return await self._send_error(
                    interaction,
                    title="Versão inválida",
                    description="❗ A versão deve ser `recommended` ou `latest`.",
                    color=0xED4245,
                )
            else:
                return await self._send_error(
                    interaction,
                    title="Erro ao validar configuração",
                    description=f"⚠️ {e}",
                    color=0xED4245,
                )

    async def _send_error(
        self, interaction: discord.Interaction, title: str, description: str, color: int
    ):
        embed = discord.Embed(title=title, description=description, color=color)
        await interaction.edit_original_response(embed=embed)

import asyncio

import discord
from discord.ext import commands

from database.repository import ApplicationRepository
from exceptions import get_translated_exception_message
from services.square_manager import square_manager
from utils.logger import logger


async def component_status(app_id: int):
    status = await square_manager.status_application(app_id)

    if not status:
        return

    embed = discord.Embed()

    embed.title = status.name
    embed.description = (
        f"<t:{int(status.uptime / 1000)}:R>"
        if status.running
        else "Aplicacão desligada"
    )
    embed.add_field(name="Status", value="🟢Online" if status.running else "🔴Offline")
    embed.add_field(name="CPU", value=status.cpu)
    embed.add_field(name="RAM", value=status.ram)
    embed.add_field(name="Armazenamento", value=status.storage)
    embed.add_field(name="Rede em uso", value=status.network_now)
    embed.add_field(name="Rede total usada", value=status.network_total)

    embed.set_footer(text=status.id)

    view = AppControlView(status)

    return embed, view


class ConfirmationModal(discord.ui.Modal):
    def __init__(self, app_id: int, app_name: str):
        super().__init__(title="Confirmar Exclusao")
        self.name = discord.ui.TextInput(
            label="label", placeholder="Digite o nome do aplicativo pra confirmar"
        )

        self.add_item(self.name)

        self.app_id = app_id
        self.app_name = app_name

    async def on_submit(self, interaction: discord.Interaction):
        if not self.name.value == self.app_name:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="❌ Nome incorreto",
                    description=(
                        "O nome informado não corresponde ao da aplicação.\n"
                        "Por favor, verifique e tente novamente."
                    ),
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )

        try:
            await asyncio.gather(
                square_manager.delete_app(app_id=self.app_id),
                ApplicationRepository.delete(app_id=self.app_id),
            )

            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="✅ Aplicação excluída",
                    description="Seu app foi removido com sucesso da plataforma.",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )

        except Exception as e:
            logger.error("Erro ao excluir aplicacão", exc_info=True)

            error = get_translated_exception_message(e)

            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="❌ Erro ao excluir aplicacão",
                    description=(
                        error
                        if error
                        else "Ocorreu um erro desconhecido. Se o problema persistir, entre em contato com um administrador."
                    ),
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )


class AppControlView(discord.ui.View):
    def __init__(self, status):
        super().__init__(timeout=None)

        self.name = status.name
        self.app_id = status.id
        self.running = status.running
        self.lang = status.lang

        self.btn_start = discord.ui.Button(label="Iniciar", disabled=self.running)
        self.btn_restart = discord.ui.Button(
            label="Reiniciar", disabled=not self.running
        )
        self.btn_stop = discord.ui.Button(label="Desligar", disabled=not self.running)
        self.btn_logs = discord.ui.Button(label="Logs")
        self.btn_delete = discord.ui.Button(label="Deletar")

        self.btn_start.callback = self.start
        self.btn_restart.callback = self.restart
        self.btn_stop.callback = self.stop
        self.btn_logs.callback = self.logs
        self.btn_delete.callback = self.delete

        self.add_item(self.btn_start)
        self.add_item(self.btn_restart)
        self.add_item(self.btn_stop)
        self.add_item(self.btn_logs)
        self.add_item(self.btn_delete)

    async def start(self, interaction: discord.Interaction):
        await square_manager.start_app(app_id=self.app_id)

        status = await component_status(app_id=self.app_id)

        await interaction.response.edit_message(embed=status[0], view=status[1])

    async def restart(self, interaction: discord.Interaction):
        await square_manager.restart_app(app_id=self.app_id)

        status = await component_status(app_id=self.app_id)

        await interaction.response.edit_message(embed=status[0], view=status[1])

    async def stop(self, interaction: discord.Interaction):
        await square_manager.stop_app(app_id=self.app_id)

        status = await component_status(app_id=self.app_id)

        await interaction.response.edit_message(embed=status[0], view=status[1])

    async def logs(self, interaction: discord.Interaction):
        app = await square_manager.get_logs(app_id=self.app_id)

        template = f"```{self.lang}\n{app.logs}```"

        if len(template) < 2000:
            return await interaction.response.send_message(
                content=template, ephemeral=True
            )
        import io

        buffer = io.BytesIO(app.logs.encode())

        await interaction.response.send_message(
            file=discord.File(buffer, "logs.txt"), ephemeral=True
        )

    async def delete(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ConfirmationModal(self.app_id, self.name))


class StatusCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(
        name="status", description="Veja status de suas aplicacoes"
    )
    async def command_callback(self, interaction: discord.Interaction, name: str):
        await interaction.response.defer(thinking=True, ephemeral=True)

        status = await component_status(name)

        if status:
            return await interaction.edit_original_response(
                embed=status[0], view=status[1]
            )

        await interaction.edit_original_response(
            embed=discord.Embed(
                title="🔍 App não encontrado",
                description="Nenhum aplicativo foi encontrado com esse ID. Verifique se o ID está correto ou tente novamente.",
                color=discord.Color.orange(),
            )
        )

    @command_callback.autocomplete(name="name")
    async def search_app(self, interaction, name: str):
        apps = await ApplicationRepository.list(interaction.user.id)

        if not apps:
            return [
                discord.app_commands.Choice(name="Nenhum app encontrado", value="foo")
            ]

        choices = [
            discord.app_commands.Choice(name=app.name, value=app.application_id)
            for app in apps
            if app.name.startswith(name)
        ]

        return choices[:25]


async def setup(bot: commands.Bot):
    await bot.add_cog(StatusCog(bot))

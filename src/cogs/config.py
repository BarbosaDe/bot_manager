import discord
from discord.ext import commands

from ui.config.buttons import AddPlanButton, EditPlanButton, RemovePlanButton


class ConfigCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="config", description="configure seu bot[admin]")
    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message(
                "❌ Você precisa ser administrador para usar este comando.",
                ephemeral=True,
            )

        embed = discord.Embed(
            title="⚙️ Configuração de Planos",
            description="Gerencie os planos disponíveis para seu bot.\n\n- Adicione novos planos\n- Edite os existentes\n- Remova planos obsoletos",
            color=discord.Color.blurple(),
        )
        embed.set_footer(text="Painel de configuração de planos")

        view = discord.ui.View()

        view.add_item(AddPlanButton())
        view.add_item(EditPlanButton())
        view.add_item(RemovePlanButton())
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(ConfigCog(bot))

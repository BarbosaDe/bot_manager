import discord
from discord.ext import commands

from database.repository import PlanRepository
from ui.config.select import SelectPlan


class PlanCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(
        name="comprar-plano",
        description="compre o plano perfeito pra voce",
    )
    async def callback(self, interaction: discord.Interaction):
        view = discord.ui.View()

        plans = await PlanRepository.list(25)

        view.add_item(SelectPlan(plans, "buy"))

        await interaction.response.send_message(view=view, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(PlanCog(bot))

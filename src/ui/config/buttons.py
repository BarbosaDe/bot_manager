import discord

from database.repository import PlanRepository
from ui.config.modals import AddPlanModal
from ui.config.select import SelectPlan


class RemovePlanButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.danger,
            label="Remover Plano",
            emoji="🗑️",
        )

    async def callback(self, interaction: discord.Interaction):
        plans = await PlanRepository.list(25)

        if not plans:
            embed = discord.Embed(
                title="Nenhum plano disponível",
                description="Atualmente não há planos cadastrados ou disponíveis para seleção.",
                color=discord.Color.red(),
            )

            return await interaction.response.send_message(embed=embed, ephemeral=True)

        view = discord.ui.View()

        view.add_item(SelectPlan(plans, "remove"))

        await interaction.response.send_message(view=view, ephemeral=True)


class AddPlanButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.green,
            label="Adicionar Plano",
            emoji="➕",
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AddPlanModal())


class EditPlanButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.blurple,
            label="Editar Plano",
            emoji="✏️",
        )

    async def callback(self, interaction: discord.Interaction):
        plans = await PlanRepository.list()

        if not plans:
            embed = discord.Embed(
                title="Nenhum plano disponível",
                description="Atualmente não há planos cadastrados ou disponíveis para seleção.",
                color=discord.Color.red(),
            )

            return await interaction.response.send_message(embed=embed, ephemeral=True)

        view = discord.ui.View()

        view.add_item(SelectPlan(plans, "edit"))
        await interaction.response.send_message(view=view, ephemeral=True)

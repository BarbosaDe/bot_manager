import discord

from database.models import Plan
from database.repository import PlanRepository
from exceptions import DuplicateEntryError


class AddPlanModal(discord.ui.Modal, title="Adicione um plano"):
    name = discord.ui.TextInput(
        label="Nome do Plano",
        placeholder="Ex: Plano Básico",
    )

    price = discord.ui.TextInput(
        label="Preço",
        placeholder="Ex: 19.99",
        default="0.00",
    )

    max_ram = discord.ui.TextInput(
        label="Memoria RAM",
        placeholder="Ex: 1024",
        default="0",
    )

    async def on_submit(self, interaction: discord.Interaction):
        name = self.name.value.strip()
        price = self.price.value.strip()
        max_ram = self.max_ram.value.strip()

        try:
            await PlanRepository.insert(name, price, max_ram)

            await interaction.response.send_message(
                embed=discord.Embed(
                    title="✅ Plano criado com sucesso!",
                    description=f"O plano **{name}** foi criado corretamente.",
                    color=0x57F287,
                ),
                ephemeral=True,
            )

        except DuplicateEntryError:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="⚠️ Nome duplicado",
                    description="Já existe um plano com esse nome. Escolha outro nome para continuar.",
                    color=0xFEE75C,
                ),
                ephemeral=True,
            )


class EditPlanModal(discord.ui.Modal):
    def __init__(self, plan: Plan):
        super().__init__(title=f"Editar o plano {plan.name}")

        self.name = discord.ui.TextInput(
            label="Nome", placeholder="Ex: Plano Básico", default=plan.name
        )

        self.price = discord.ui.TextInput(
            label="Preço",
            placeholder="Ex: 19.99",
            default=str(plan.price),
        )

        self.max_ram = discord.ui.TextInput(
            label="Memoria RAM",
            placeholder="Ex: 1024",
            default=str(plan.max_ram),
        )

        self.add_item(self.name)
        self.add_item(self.price)
        self.add_item(self.max_ram)

        self.plan = plan

    async def on_submit(self, interaction):
        old_plan = self.plan

        new_plan = Plan(
            name=self.name.value, price=self.price.value, max_ram=self.max_ram.value
        )

        await PlanRepository.update(old_plan, new_plan)

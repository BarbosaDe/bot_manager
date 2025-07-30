import discord

from database.models import Plan
from database.repository import PlanRepository
from exceptions import DuplicateEntryError
from utils.validators import type_check


class AddPlanModal(discord.ui.Modal, title="Adicione um plano"):
    name = discord.ui.TextInput(
        label="Nome do Plano", placeholder="Ex: Plano Básico", max_length=15
    )

    price = discord.ui.TextInput(
        label="Preço", placeholder="Ex: 19.99", default="0.00", max_length=7
    )

    max_ram = discord.ui.TextInput(
        label="Memoria RAM", placeholder="Ex: 1024", default="0", max_length=7
    )

    async def on_submit(self, interaction: discord.Interaction):
        name = self.name.value.strip()
        price = type_check(self.price.value.strip(), float)
        max_ram = type_check(self.max_ram.value.strip(), int)

        if not price:
            campo = "preço"
            valor = self.price.value
        elif not max_ram:
            campo = "RAM"
            valor = self.max_ram.value

        if not all([price, max_ram]):
            embed = discord.Embed(
                title="Valor inválido",
                description=f"O valor informado para **{campo}** (`{valor}`) não é um número válido.",
                color=discord.Color.red(),
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

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
            label="Nome",
            placeholder="Ex: Plano Básico",
            default=plan.name,
            max_length=15,
        )

        self.price = discord.ui.TextInput(
            label="Preço",
            placeholder="Ex: 19.99",
            default=str(plan.price),
            max_length=7,
        )

        self.max_ram = discord.ui.TextInput(
            label="Memoria RAM",
            placeholder="Ex: 1024",
            default=str(plan.max_ram),
            max_length=7,
        )

        self.add_item(self.name)
        self.add_item(self.price)
        self.add_item(self.max_ram)

        self.plan = plan

    async def on_submit(self, interaction):
        price = type_check(self.price.value.strip(), float)
        max_ram = type_check(self.max_ram.value.strip(), int)

        if not price:
            campo = "preço"
            valor = self.price.value
        elif not max_ram:
            campo = "RAM"
            valor = self.max_ram.value

        if not all([price, max_ram]):
            embed = discord.Embed(
                title="Valor inválido",
                description=f"O valor informado para **{campo}** (`{valor}`) não é um número válido.",
                color=discord.Color.red(),
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        new_plan = Plan(name=self.name.value, price=price, max_ram=max_ram)

        await PlanRepository.update(self.plan, new_plan)

        await interaction.response.send_message(
            embed=discord.Embed(
                title="✅ Plano criado com sucesso!",
                description=f"O plano **{self.plan.name}** foi atualizado corretamente.",
                color=0x57F287,
            ),
            ephemeral=True,
        )

import base64
import io

import discord

from database.repository import PlanRepository
from payments import payment_service
from ui.config.modals import EditPlanModal


class SelectPlan(discord.ui.Select):
    def __init__(self, plans, mode: str):
        super().__init__(placeholder="Selecione o plano")

        self.options = [
            discord.SelectOption(
                label=plan.name[:25],
                description=f"💾 {plan.max_ram}MB | 💰 R$ {plan.price:.2f}"[:50],
                value=str(plan.id),
            )
            for plan in plans
        ]

        self.mode = mode

    async def callback(self, interaction):
        plan = await PlanRepository.get(int(self.values[0]))

        if not plan:
            embed = discord.Embed(
                title="🗑️ Plano não encontrado",
                description="O plano selecionado não foi encontrado.",
                color=discord.Color.red(),
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        if self.mode == "edit":
            await interaction.response.send_modal(EditPlanModal(plan))

        elif self.mode == "remove":
            await PlanRepository.delete(plan)

            embed = discord.Embed(
                title="🗑️ Plano deletado",
                description=f"O plano **{plan.name}** foi removido com sucesso.",
                color=discord.Color.red(),
            )
            embed.set_footer(text="A ação não pode ser desfeita.")

            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif self.mode == "buy":
            payment_codes = await payment_service.create(
                interaction.user.id, interaction.guild.id, plan
            )
            qr_bytes = io.BytesIO(base64.b64decode(payment_codes["qr_code_base64"]))
            file = discord.File(qr_bytes, filename="qr_code.png")

            embed = discord.Embed(
                title="💳 Pagamento gerado com sucesso!",
                description=f"Você está adquirindo o plano **{plan.name}**.\n\n"
                f"Use o QR Code abaixo ou copie o código Pix para pagar.",
                color=discord.Color.blue(),
            )

            embed.add_field(
                name="🔢 Código Pix (copia e cola)",
                value=f"```{payment_codes['qr_code']}```",
                inline=False,
            )
            embed.set_image(url="attachment://qr_code.png")
            embed.set_footer(text="O pagamento expira em 24 horas.")

            await interaction.response.send_message(
                embed=embed, file=file, ephemeral=True
            )

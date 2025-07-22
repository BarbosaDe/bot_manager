import base64
import io

import discord
from discord.ext import commands
from squarecloud import UploadData

from database import Whitelist
from payments import Payment
from square_manager import square_manager


class UploadCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="upload", description="Hospede sua aplicacão")
    async def callback(
        self, interaction: discord.Interaction, file: discord.Attachment
    ):
        await interaction.response.defer(thinking=True, ephemeral=True)
        user_id = interaction.user.id
        server_id = interaction.guild.id
        whitelist = await Whitelist.get(user_id)

        if not whitelist:
            price = 0.01
            payment = await Payment.create_qr(user_id, server_id, price)

            image = io.BytesIO(base64.b64decode(payment["qr_code_base64"]))
            return await interaction.edit_original_response(
                attachments=[discord.File(image, filename="qrcode.png")],
                content=payment["qr_code"],
            )

        response = await square_manager.upload_application(
            await file.read(), file.filename
        )

        if not isinstance(response, UploadData):
            return await interaction.edit_original_response(
                content=f"Ocorreu um erro durante o deploy: {response}"
            )

        return await interaction.edit_original_response(
            content=f"A aplicacão `{response.name}` foi hospedada com sucesso !"
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(UploadCog(bot))

import discord

from ui.upload.settings_app_modal import SettingsSquareApp


class WebsiteButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.btn_sim = discord.ui.Button(
            label="Sim",
        )

        self.btn_nao = discord.ui.Button(
            label="Não",
        )

        self.btn_sim.callback = self.sim_callback
        self.btn_nao.callback = self.nao_callback

        self.add_item(self.btn_sim)
        self.add_item(self.btn_nao)

    async def sim_callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(SettingsSquareApp(True))

    async def nao_callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(SettingsSquareApp(False))

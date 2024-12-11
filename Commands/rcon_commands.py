import nextcord
from nextcord.ext import commands
from Functions.rcon_functions import RCON_Functions
from Functions.static_embeds import Static_Embeds as se

class RCON_Commands(commands.Cog):
    def __init__(self, bot: commands.Bot, rconf: RCON_Functions):
        self.bot = bot
        self.rconf = rconf
    
    @nextcord.slash_command(name="rcon", description="Send an RCON command to the server")
    async def rcon(self, interaction: nextcord.Interaction, command: str):
        await interaction.response.defer(ephemeral=True)
        response = await self.rconf.send_command(command)
        if response:
            await interaction.followup.send(ephemeral=True, embed=se.success_embed(f"**Command:** {command}\n**Response:** {response}"))
        else:
            await interaction.followup.send(ephemeral=True, embed=se.error_embed("The RCON command timed out. Please try again later."))
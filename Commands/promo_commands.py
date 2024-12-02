import nextcord
from nextcord.ext import commands
from Functions.static_embeds import Static_Embeds as se

# This class contains the commands that are used to interact with the Promotion threads.
class Promo_Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @nextcord.slash_command(name="cleanup", description="Cleans up the thread by deleting all the messages below 200 characters. Excluding the first message.")
    async def cleanup(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True)
        channel = interaction.channel

        if channel.owner.id != interaction.user.id:
            await interaction.followup.send(ephemeral=True, embed=se.error_embed("You are not the owner of this channel!"))
            return
        else:
            messages = await channel.history(limit=None).flatten()
            for message in messages[:-1]:
                if len(message.content) < 200:
                    await message.delete()
            await interaction.followup.send(ephemeral=True, embed=se.success_embed("Messages cleaned up!"))

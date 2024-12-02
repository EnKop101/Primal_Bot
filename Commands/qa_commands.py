import nextcord
from nextcord.ext import commands
from Functions.qa_functions import Qa_Functions as qaf
from Functions.static_embeds import Static_Embeds as se

# This class contains the commands that are used to interact with the LLM Chatbot model using the API endpoint.
class Qa_Commands(commands.Cog):
    def __init__(self, bot: commands.Bot, qaf: qaf):
        self.bot = bot
        self.qaf = qaf


    @nextcord.slash_command(name="ask-chaos", description="Ask a question about Primal Chaos")
    async def ask_chaos(self, interaction: nextcord.Interaction, question: str):
        await interaction.response.defer(ephemeral=True)
        chat_response = await self.qaf.generate_completions(question, True)

        # Checks whether the chat_response is not empty. If it is empty something went wrong with the API request.
        if chat_response:
            await interaction.followup.send(ephemeral=True, embed=se.response_embed(chat_response))
        else:
            await interaction.followup.send(ephemeral=True, embed=se.error_embed("It seems something went wrong with your request. If this continues please contact an Admin for help instead."))

    @nextcord.slash_command(name="ask-nemesis", description="Ask a question about Primal Nemesis")
    async def ask_nemesis(self, interaction: nextcord.Interaction, question: str):
        await interaction.response.defer(ephemeral=True)
        chat_response = await self.qaf.generate_completions(question, False)

        # Checks whether the chat_response is not empty. If it is empty something went wrong with the API request.
        if chat_response:
            await interaction.followup.send(ephemeral=True, embed=se.response_embed(chat_response))
        else:
            await interaction.followup.send(ephemeral=True, embed=se.error_embed("It seems something went wrong with your request. If this continues please contact an Admin for help instead."))
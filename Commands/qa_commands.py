import nextcord
from nextcord.ext import commands
from Functions.qa_functions import Qa_Functions as qaf
from Functions.static_embeds import Static_Embeds as se
from Functions.dh_functions import DH_Functions
# from Classes.pc_class import PC_Class
# from Classes.pn_class import PN_Class
from Classes.add_qa_modal import Add_QA_Modal

# This class contains the commands that are used to interact with the LLM Chatbot model using the API endpoint.
class Qa_Commands(commands.Cog):
    def __init__(self, bot: commands.Bot, qaf: qaf, dhf: DH_Functions):
        self.bot = bot
        self.qaf = qaf
        self.dhf = dhf

    @nextcord.slash_command(name="ask-chaos", description="Ask a question about Primal Chaos")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ask_chaos(self, interaction: nextcord.Interaction, question: str):
        await interaction.response.defer(ephemeral=True)
        chat_response = await self.qaf.generate_completions(question, True)

        # Checks whether the chat_response is not empty. If it is empty something went wrong with the API request.
        if chat_response:
            await interaction.followup.send(ephemeral=True, embed=se.response_embed(chat_response))
        else:
            await interaction.followup.send(ephemeral=True, embed=se.error_embed("It seems something went wrong with your request. If this continues please contact an Admin for help instead."))

    @nextcord.slash_command(name="ask-nemesis", description="Ask a question about Primal Nemesis")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ask_nemesis(self, interaction: nextcord.Interaction, question: str):
        await interaction.response.defer(ephemeral=True)
        chat_response = await self.qaf.generate_completions(question, False)

        # Checks whether the chat_response is not empty. If it is empty something went wrong with the API request.
        if chat_response:
            await interaction.followup.send(ephemeral=True, embed=se.response_embed(chat_response))
        else:
            await interaction.followup.send(ephemeral=True, embed=se.error_embed("It seems something went wrong with your request. If this continues please contact an Admin for help instead."))

    @nextcord.slash_command(name="add-qa", description="Adds a question and answer to the QA context")
    async def add_qa(self, interaction: nextcord.Interaction, mod_option = nextcord.SlashOption(
        name="option", description="Select the QA context", required=True, choices={"Primal Chaos": "0", "Primal Nemesis": "1"})):
        is_pc = True if mod_option == "0" else False
        modal = Add_QA_Modal(self.dhf, is_pc)
        await interaction.response.send_modal(modal)
    
    @nextcord.slash_command(name="remove-qa", description="Removes a question and answer from the QA context")
    async def remove_qa(self, interaction: nextcord.Interaction, mod_option = nextcord.SlashOption(
        name="option", description="Select the QA context", required=True, choices={"Primal Chaos": "0", "Primal Nemesis": "1"}),
        message_id = str):
        await interaction.response.defer(ephemeral=True)
        is_pc = True if mod_option == "0" else False
        await self.dhf.remove_message(message_id, is_pc)
        await interaction.followup.send(ephemeral=True, embed=se.success_embed(f"Message with id: {message_id} has been removed from the QA context."))
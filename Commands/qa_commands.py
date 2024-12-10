import nextcord
from nextcord.ext import commands
from Functions.qa_functions import Qa_Functions as qaf
from Functions.static_embeds import Static_Embeds as se
from Functions.dh_functions import DH_Functions
from Classes.qa_class import QA_Class
# from Classes.pn_class import PN_Class
from Classes.add_qa_modal import Add_QA_Modal

# This class contains the commands that are used to interact with the LLM Chatbot model using the API endpoint.
class Qa_Commands(commands.Cog):
    def __init__(self, bot: commands.Bot, qaf: qaf, dhf: DH_Functions):
        self.bot = bot
        self.qaf = qaf
        self.dhf = dhf

#region This command uses the Primal Chaos context to generate completions for the given question.
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
#endregion
            
#region This command uses the Primal Nemesis context to generate completions for the given question.
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
#endregion

#region This command adds a question and answer to the QA context using a modal.
    @nextcord.slash_command(name="add-qa", description="Adds a question and answer to the QA context")
    async def add_qa(self, interaction: nextcord.Interaction, mod_option = nextcord.SlashOption(
        name="option", description="Select the QA context", required=True, choices={"Primal Chaos": "0", "Primal Nemesis": "1"})):
        is_pc = True if mod_option == "0" else False
        modal = Add_QA_Modal(self.qaf, self.dhf, is_pc)
        await interaction.response.send_modal(modal)
#endregion
        
#region This command removes a question and answer from the QA context.
    @nextcord.slash_command(name="remove-qa", description="Removes a question and answer from the QA context")
    async def remove_qa(self, interaction: nextcord.Interaction, mod_option = nextcord.SlashOption(
        name="option", description="Select the QA context", required=True, choices={"Primal Chaos": "0", "Primal Nemesis": "1"}),
        message_id = str):
        await interaction.response.defer(ephemeral=True)
        
        # Check the mod_option to determine which context to use.
        is_pc = True if mod_option == "0" else False
        updated_messages: list[QA_Class] = await self.dhf.remove_message(message_id, is_pc)

        # Check if the updated_messages is None. If it is, send a message to the user.
        if updated_messages == None:
            await interaction.followup.send(ephemeral=True, embed=se.error_embed("No message found with that id."))
            return
        
        # Update the QA context with the new messages.
        await self.qaf.update_qaf_variables(updated_messages, is_pc)
        await interaction.followup.send(ephemeral=True, embed=se.success_embed(f"QA with id: {message_id} has been removed from the QA context."))
#endregion
        
#region This command lists all the questions and answers in the QA context.
    @nextcord.slash_command(name="list-qa", description="Lists all the questions and answers in the QA context")
    async def list_qa(self, interaction: nextcord.Interaction, mod_option = nextcord.SlashOption(
        name="option", description="Select the QA context", required=True, choices={"Primal Chaos": "0", "Primal Nemesis": "1"})):
        await interaction.response.defer(ephemeral=True)

        # Checks the mod_option to determine which context to use.
        is_pc = True if mod_option == "0" else False
        if is_pc:
            messages = self.dhf.pc_messages
        else:
            messages = self.dhf.pn_messages 
        
        # Checks if there are any messages in the list. If there are none, send a message to the user.
        if not messages:
            await interaction.followup.send(embed=se.response_embed("There are no QA's for this category."))
            return
        
        # Create a view and a button to delete all the messages.
        view = nextcord.ui.View(timeout=None)
        list_of_sent_messages: list[nextcord.Message] = []
        button = nextcord.ui.Button(style=nextcord.ButtonStyle.danger, label="Delete All Messages")

        # This is the buttons callback function. It deletes all the messages in the list.
        async def delete_all_listed_qa(interaction: nextcord.Interaction):
            try:
                for message in list_of_sent_messages:
                    await message.delete()
                await interaction.response.edit_message(embed=se.success_embed("All messages have been deleted."), view=None)
            except:
                # If an error occurs, The message has probably already been deleted. Do nothing.
                pass
        
        # Set the buttons callback function and add it to the view.
        button.callback = delete_all_listed_qa
        view.add_item(button)

        # Loop through the messages and send them to the channel.
        for message in messages:
            list_of_sent_messages.append(await interaction.channel.send(embed=se.response_embed(f"**Id:** {message.id}\n**Question:** {message.question}\n**Answer:** {message.answer}")))
        
        # Finally send the view to the user along with a Done message.
        await interaction.followup.send(embed=se.response_embed(f"All QA's have been listed. Click the button to delete them all again."), ephemeral=True, view=view)
#endregion

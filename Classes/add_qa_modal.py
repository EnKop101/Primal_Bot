import nextcord
from nextcord.ui import Modal, TextInput, StringSelect
from Classes.qa_class import QA_Class
from Functions.dh_functions import DH_Functions
from Functions.qa_functions import Qa_Functions
from Functions.static_embeds import Static_Embeds as se

# This class is a modal that is used to add a QA to the QA context JSON file.
class Add_QA_Modal(Modal):
    def __init__(self, qaf: Qa_Functions, dhf: DH_Functions, is_pc: bool):
        super().__init__("Add a QA")
        self.is_pc = is_pc
        self.dhf: DH_Functions = dhf
        self.qaf = qaf
        # Create the input values for the modal.
        self.question = TextInput(placeholder="Question", label="Question")
        self.answer = TextInput(placeholder="Answer", label="Answer", min_length=1, style=nextcord.TextInputStyle.paragraph)
        self.category = StringSelect(placeholder="Select a Category")
        
        # Add the items to the modal.
        self.add_item(self.question)
        self.add_item(self.answer)

    # This function is called when the modal is submitted.
    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True)
        # Create a QA_Class object with the values from the modal.
        message = QA_Class(self.question.value, self.answer.value)

        # Add the message to the QA context.
        updated_messages: list[QA_Class] = await self.dhf.add_message(message, self.is_pc)

        # Check if the message was added successfully. If not send an error message.
        if updated_messages == None:
            await interaction.followup.send(embed=se.error_embed("Failed to add message. If this continues please contact EnKop"), ephemeral=True)
            return

        # Update the Qa_Functions variables with the new messages.
        await self.qaf.update_qaf_variables(updated_messages, self.is_pc)
        await interaction.followup.send(embed=se.success_embed(f"**QA Added**\n**Id:** {message.id}\n**Question:** {message.question}\n**Answer:** {message.answer}"), ephemeral=True)
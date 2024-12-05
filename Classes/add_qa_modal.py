import nextcord
from nextcord.ui import Modal, TextInput, StringSelect
from Classes.pc_class import PC_Class
from Classes.pn_class import PN_Class
from Functions.dh_functions import DH_Functions
from Functions.static_embeds import Static_Embeds as se
# dh_functions: DH_Functions,
class Add_QA_Modal(Modal):
    def __init__(self, dhf: DH_Functions, is_pc: bool):
        super().__init__("Add a QA")
        self.is_pc = is_pc
        self.dhf: DH_Functions = dhf

        self.question = TextInput(placeholder="Question", label="Question")
        self.answer = TextInput(placeholder="Answer", label="Answer")
        self.category = StringSelect(placeholder="Select a Category")

        self.add_item(self.question)
        self.add_item(self.answer)

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if self.is_pc:
            message = PC_Class(self.question.value, self.answer.value)
        else:
            message = PN_Class(self.question.value, self.answer.value)

        response = f"**QA Added**\nQuestion: {message.question}\nAnswer: {message.answer}\nId: {message.id}"
        await self.dhf.add_message(message)
        await interaction.followup.send(embed=se.success_embed(response), ephemeral=True)
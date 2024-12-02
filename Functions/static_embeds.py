import nextcord
# This class contains static embeds that can be used in the Discord commands.
class Static_Embeds:
    @staticmethod
    def error_embed(message):
        embed = nextcord.Embed(title="Error!", description=message, color=nextcord.Color.red())
        return embed

    @staticmethod
    def success_embed(message):
        embed = nextcord.Embed(title="Success!", description=message, color=nextcord.Color.green())
        return embed

    @staticmethod
    def response_embed(description):
        embed = nextcord.Embed(description=description, color=nextcord.Color.blue())
        return embed
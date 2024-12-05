import nextcord
import re

from nextcord.ext import tasks
from datetime import datetime
from Functions.static_embeds import Static_Embeds as se

# This class contains all the QoL functions that are used in the bot. This includes filtering, cleanup and other functions.
class QoL_Functions:
    promo_channel: nextcord.TextChannel = None

    def __init__(self):
        pass

    @staticmethod
    @tasks.loop(hours=24)
    async def destroy_old_posts():
        # Formats time to be printed in the console
        formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Daily Server Promo Cleanup Initiated at {formatted_time}")
        deleted_count = 0
        async for thread in QoL_Functions.promo_channel.archived_threads(limit=None):
            await thread.delete()
            deleted_count += 1

        print(f"Deleted {deleted_count} archived posts!")
    
    @staticmethod
    async def filter_links(message: nextcord.Message, promo_channel_id: int):
        if message.channel.type != nextcord.ChannelType.text:
            if message.channel.parent_id == promo_channel_id and message.author.id == message.channel.owner_id:
                return False
            
        discord_url_pattern = re.compile(r'discord\.(gg|com)/(invite/\S+|[^/]+)')
        return discord_url_pattern.search(message.content)

    # This function checks if the user has already posted in the promotion channel. If so delete the newly created thread.
    @staticmethod
    async def limit_one_post_per_user(thread: nextcord.Thread):
        for post in QoL_Functions.promo_channel.threads:
            if post.owner.id == thread.owner.id and post.id != thread.id:
                await thread.owner.send(embed=se.error_embed(f"{thread.owner.mention}, you are only allowed to post once in the promotion channel!"))
                await thread.delete()
                return
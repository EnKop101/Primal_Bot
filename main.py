# Imports
import nextcord
import os
import pyfiglet

# Import all the classes
from Functions.qa_functions import Qa_Functions
from Functions.qol_functions import QoL_Functions
from Functions.static_embeds import Static_Embeds as se
from Functions.dh_functions import DH_Functions
from Functions.rcon_functions import RCON_Functions
from Classes.rcon_class import RCON_Class
from Commands import qa_commands as qac
from Commands import promo_commands as pc
from Commands import rcon_commands as rconc

# From imports
from nextcord.ext import commands
from dotenv import load_dotenv
from colorama import Fore, Style, init

#region .env file setup
# Load the .env file
dotenv_path = f"{os.getcwd()}//Configuration_Files/.env"
load_dotenv(dotenv_path)

#Get all the values from the .env file
bot_token = os.getenv('TOKEN')
# test_token = os.getenv('TEST')
promo_channel_id = int(os.getenv('PROMO_CHANNEL_ID'))
ai_channel_id = os.getenv('AI_CHANNEL_ID')
rcon_ip = os.getenv('RCON_IP')
rcon_port = os.getenv('RCON_PORT')
rcon_password = os.getenv('RCON_PASS')
authorized_roles_id = os.getenv('AUTHORIZED_ROLES_ID').split(',') if os.getenv('AUTHORIZED_ROLES_ID') else []
guild_id = int(os.getenv('GUILD_ID'))
doc_folder_path = os.getenv('DOC_FOLDER_PATH')

#endregion

# Set Json File Path for the QA context
pc_json_path = f"{doc_folder_path}{guild_id}/primal-chaos.json"
pn_json_path = f"{doc_folder_path}{guild_id}/primal-nemesis.json"

# Initialize colorama
init()

# Create the bot. Use all intents.
bot = commands.Bot(intents=nextcord.Intents.all())

# Create the instances of the classes.
dhf = DH_Functions(pc_json_path, pn_json_path)
qaf = Qa_Functions(dhf.pc_messages, dhf.pn_messages)
rcon_class = RCON_Class(rcon_ip, int(rcon_port), rcon_password)
rconf = RCON_Functions(rcon_class)

# Load the commands.
bot.add_cog(qac.Qa_Commands(bot, qaf, dhf))
bot.add_cog(pc.Promo_Commands(bot))
bot.add_cog(rconc.RCON_Commands(bot, rconf))
print(f'Cogs have been loaded.')

# Global variables
authorized_users_id = []

#region On Ready Event
@bot.event
async def on_ready():
    guild = bot.get_guild(guild_id)

    if guild == None:
        print("Guild Fetch Failed! Shutting down bot.")
        await bot.close()

    if promo_channel_id != "0":
        try:
            promo_channel = await bot.fetch_channel(promo_channel_id)
            print(f"Promo Channel Fetched: {promo_channel.name}")
            QoL_Functions.promo_channel = promo_channel
            QoL_Functions.destroy_old_posts.start()
        except:
            print("Promo Channel Fetch Failed!")
    
    if QoL_Functions.destroy_old_posts.is_running():
        print("Destroy Old Posts Task Started!")

    
    for role_id in authorized_roles_id:
        role = guild.get_role(int(role_id))
        if role:
            for member in role.members:
                if member.id not in authorized_users_id:
                    authorized_users_id.append(member.id)
                    # print(f"Added {member.name} to the authorized users list.")

    # Create the bot ascii art and print it
    on_ready_logo = pyfiglet.figlet_format("PRIMAL BOT\n    READY", font="slant")
    print(Fore.GREEN + on_ready_logo)
    print(Style.RESET_ALL)

#endregion
    
#region On Message and Raw Message Edit Events
# on Message event. This event is called whenever a message is sent in a channel the bot has access to.
@bot.event
async def on_message(message: nextcord.Message):
    if message.author == bot.user:
        return
    try:
        # Check if the user is an authorized user.
        if message.author.id not in authorized_users_id:
            # Check if the message contains a discord invite link. If it does, delete the message unless the link is in the promotion channel and user owns the thread.
            if await QoL_Functions.filter_links(message, promo_channel_id):
                await message.author.send(delete_after=5, embed=se.error_embed(f"{message.author.mention}, you are not allowed to send discord invite links other than in the promotion channel!"))
                print("Unauthorized User {0} sent a invite link in channel: {1}".format(message.author.name, message.channel.name))
                print("Message Content: {0}".format(message.content))
                print("----------" * 20)
                await message.delete()
    except:
        # If an error occurs, do nothing.
        pass

# on Raw Message Edit event. This event is called whenever a message is edited. This will mostly contain the same code as the on_message event.
@bot.event
async def on_raw_message_edit(message_payload: nextcord.RawMessageUpdateEvent):

    author = message_payload.data['author']
    if 'bot' in author and author['bot'] == True:
        return
    
    try:
        # Fetch the message from the payload.
        message = await bot.get_channel(message_payload.channel_id).fetch_message(message_payload.message_id)

        # Check if the user is an authorized user.
        if message.author.id not in authorized_users_id:
            # Check if the message contains a discord invite link. If it does, delete the message unless the link is in the promotion channel and user owns the thread.
            if await QoL_Functions.filter_links(message, promo_channel_id):
                await message.author.send(delete_after=5, embed=se.error_embed(f"{message.author.mention}, you are not allowed to send discord invite links other than in the promotion channel!"))
                print("Unauthorized User {0} sent a invite link in channel: {1}".format(message.author.name, message.channel.name))
                print("Message Content: {0}".format(message.content))
                print("----------" * 20)
                await message.delete()
    except:
        # If an error occurs, do nothing.
        pass

#endregion

#region On Thread Create Event   
@bot.event
async def on_thread_create(thread: nextcord.Thread):
    if thread.parent.id != promo_channel_id or QoL_Functions.promo_channel == None:
        return
    try:
        await QoL_Functions.limit_one_post_per_user(thread)
    except Exception as e:
        print(f"Error in on_thread_create: {e}")

#endregion

# Run the bot
bot.run(bot_token)

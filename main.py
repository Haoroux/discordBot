import os
import random
import discord
from discord import app_commands
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

#importation du token du bot
load_dotenv(dotenv_path="config")

#Démmarage et intents
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!',intents=intents)
guild_ids = [1035614329678082098]

@bot.event
async def on_ready():
    print('HideInTheShadows!')
    synced = await bot.tree.sync()
    print("Slash CMDs Synced " + str(len(synced)))

#Tout ce qui est slash commande
@bot.tree.command(name="hello", description="shutting dow the bot")
async def shutdown(interaction: discord.Interaction):
    await interaction.response.send_message(content="that a test")
    await bot.close()

bot.run(os.getenv("TOKEN"))

#mots interdits + suppression
#IWords = ["fuck","pute","fdp"]

#@bot.event
#async def on_message(message):
#    if message.content.lower() in IWords:
#        await message.channel.purge(limit=1)
#        print('MessageDécidentMaitriser')

#    if message.content.lower() == "chuchotePlusFort":
#        await message.channel.send("j’aime et bien et je trouve sa beau")

#quand une personne arrive sur le serv
#@bot.event
#async def on_member_join(member):
#    general_channel: discord.TextChannel = bot.get_channel(1035614495944474787)
#    await general_channel.send(content=f"bienvenue sur le serv {member.display_name}!")
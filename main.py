import os
import random
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

#importation du token du bot
load_dotenv(dotenv_path="config")

#Démmarage et intents
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    print('HideInTheShadows!')

#Tout ce qui est slash commande

slash = SlashCommand(bot, sync_commands=True)

@slash.slash(name="Lancer", guild_ids=[1035614329678082098] ,description="lance un dé pour toi")
async def lancer(ctx):
    await ctx.send("test")


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
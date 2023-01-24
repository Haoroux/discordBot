import os
import random
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

#importation du token du bot
load_dotenv(dotenv_path="config")

#Démmarage et intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents=intents)
guild_ids = [1035614329678082098]

@bot.event
async def on_ready():
    print('HideInTheShadows!')
    synced = await bot.tree.sync()
    print("Slash CMDs Synced " + str(len(synced)))

#Auto moderation
IWords = ["fuck","pute","fdp","ip"]

@bot.event
async def on_message(message):
    if message.content.lower() in IWords:
        await message.channel.purge(limit=1)

#pierre papier sciseaux
@app_commands.choices(actions = [
    app_commands.Choice(name="pierre", value="pierre"),
    app_commands.Choice(name="papier", value="papier"),
    app_commands.Choice(name="ciseaux", value="ciseaux")
])

@bot.tree.command(description="joue a pierre papier ciseaux avec moi")
async def rps(interaction: discord.Interaction, actions: str):
    if actions == 'pierre':
        await interaction.response.send_message("you won")
    elif actions == "papier":
        await interaction.response.send_message("you lose")
    else:
        await interaction.response.send_message("you lose")


#Tout ce qui est slash commande
@bot.tree.command(name="test", description="That a test")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message(content="that’s a test")

#Lancement du programme
bot.run(os.getenv("TOKEN"))


#quand une personne arrive sur le serv
#@bot.event
#async def on_member_join(member):
#    general_channel: discord.TextChannel = bot.get_channel(1035614495944474787)
#    await general_channel.send(content=f"bienvenue sur le serv {member.display_name}!")

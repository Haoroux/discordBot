#librairie
import os
import random
import json
import discord
from discord import member
from discord.ext.commands import has_permissions, MissingPermissions
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

#importation du token du bot
load_dotenv(dotenv_path="config.json")

#Démmarage et intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents=intents)
guild_ids = [1035614329678082098]

@bot.event
async def on_ready():
    print('System operating!')
    synced = await bot.tree.sync()
    print("Slash CMDs Synced " + str(len(synced)))

#slash command

#/help
@bot.tree.command(description="talk about the posibilities of this bot")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message("here is your help")

#test command
@bot.tree.command(name="ping", description="ping?")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('PONG')

#commande de modération

#clear
@bot.tree.command(description="suprime le nombre de msg voulu")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount:int):
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"voila le /clear est fini!", ephemeral=True)

@clear.error
async def on_clear_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(str(error), ephemeral=True)

#Auto moderation
BanWorldList = open("BanWorldListJson.json",)
IWordList = ["ip"]

@app_commands.choices(addordelete = [
    app_commands.Choice(name="add",value='add'),
    app_commands.Choice(name="delete", value='delete')
])
@bot.tree.command(description="rajoute ou suprime des mots de la list pour l’auto modération(écris les mots en minuscules)")
async def automod(interaction: discord.Interaction,addordelete: str,banworld: str):
    if addordelete == 'add':
        IWordList.append(banworld)
        await interaction.response.send_message(IWordList)
    else:
        IWordList.remove(banworld)
        await interaction.response.send_message(IWordList)

@bot.event
async def on_message(message):
    for  word in IWordList:
        if word in message.content.lower():
            await message.delete()
    await bot.process_commands(message)

#jeux

#pierre papier sciseaux
@app_commands.choices(actions = [
    app_commands.Choice(name="pierre", value="pierre"),
    app_commands.Choice(name="papier", value="papier"),
    app_commands.Choice(name="ciseaux", value="ciseaux")
])

@bot.tree.command(description="joue a pierre papier ciseaux avec moi")
async def rps(interaction: discord.Interaction, actions: str):
    botAction = random.randint(1,9)
    print(botAction)
    pierreNum = [1,4,7]
    papierNum = [2,5,8]
    ciseauxNum = [3,6,9]
    performedAction = 'waiting'
    if botAction in pierreNum:
        performedAction = 'pierre'
        if actions == 'papier':
            await interaction.response.send_message("Comme j’ai joué "+ performedAction +". Tu as gagné")
        elif actions == 'pierre':
            await interaction.response.send_message("On a tout les deux joué " + performedAction)
        else:
            await interaction.response.send_message("Comme j’ai joué " + performedAction + ". Tu as perdu")
    if botAction in papierNum:
        performedAction = 'papier'
        if actions == 'ciseaux':
            await interaction.response.send_message("Comme j’ai joué "+ performedAction +". Tu as gagné")
        elif actions == 'papier':
            await interaction.response.send_message("On a tout les deux joué " + performedAction)
        else:
            await interaction.response.send_message("Comme j’ai joué " + performedAction + ". Tu as perdu")
    if botAction in ciseauxNum:
        performedAction = 'ciseaux'
        if actions == 'pierre':
            await interaction.response.send_message("Comme j’ai joué "+ performedAction +". Tu as gagné")
        elif actions == 'ciseaux':
            await interaction.response.send_message("On a tout les deux joué " + performedAction)
        else:
            await interaction.response.send_message("Comme j’ai joué " + performedAction + ". Tu as perdu")

#Lancement du programme
bot.run(os.getenv("TOKEN"))
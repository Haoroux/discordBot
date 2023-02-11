#librairies
import os
import discord
import aiohttp
import asyncio
from config import TOKEN,TESTTOKEN,API_KEY
from discord.ext.commands import has_permissions, MissingPermissions
from discord import app_commands
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv

#importation du token du bot
load_dotenv(dotenv_path="config.py")

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
#help

#stats

#chatGpt
@bot.tree.command(description="create a txt with chat-gpt")
async def gpt(interaction: discord.Interaction, *, prompt:str):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        payload = {
            "model":"text-davinci-003",
            "prompt": prompt,
            "temperature": 0.5,
            "max_tokens": 2048,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "best_of": 1,
        }
        headers = {"Authorization": f"Bearer {API_KEY}"}
        async with session.post("https://api.openai.com/v1/completions", json=payload, headers=headers) as resp:
            response = await resp.json()
            em = discord.Embed(title="Chat gpt’s responce:", description=prompt + response["choices"][0]["text"])
            await asyncio.sleep(delay=0)
            await interaction.followup.send(embed=em)

#BlackMesa or ApertureScience
#@app_commands.choices(team_option=[
#    app_commands.Choice(name="Aperture Science", value='ApertureScience'),
#    app_commands.Choice(name="Black Mesa", value='BlackMesa')
#])

#@bot.tree.command(description="choose your team between Black Mesa or ApertureScience")
#@app_commands.checks.bot_has_permissions(manage_roles = True)
#async def team(interaction:discord.Interaction,team_option:str,member:discord.Member=None):
#    if member == None: 
#        member = interaction.message.author   
 #       await interaction.response.send_message(member)
 #   else:
 #       await interaction.response.send_message("nope")

#minecraft
#Ngrok ip
@bot.tree.command(description="change the ancient ip to the new ip")
@app_commands.checks.has_role("Minecraft Server Moderator")
async def change_ip(interaction:discord.Interaction, ip:str):
    global actual_ip
    actual_ip = ip
    await interaction.response.send_message("The ancient ip has been changed in " + actual_ip)

@change_ip.error
async def on_change_ip_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingRole):
        await interaction.response.send_message(str(error), ephemeral=True)

@bot.tree.command(description="Show the actual ip of the minecraft server")
async def mc_ip(interaction:discord.Interaction):
    await interaction.response.send_message(str(actual_ip))

#commande de modération
#clear
@bot.tree.command(description="delete the desired number of messages")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount:int):
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"The /clear is done!", ephemeral=True)

@clear.error
async def on_clear_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(str(error), ephemeral=True)

#Auto moderation
IWordList = ['sugoma','niga','nigga','niger']

@app_commands.choices(automod_options = [
    app_commands.Choice(name="add",value='add'),
    app_commands.Choice(name="delete", value='delete'),
    app_commands.Choice(name="list", value='list')
])
@bot.tree.command(description="add or delete word of the auto moderation")
@app_commands.checks.has_permissions(manage_messages=True,manage_roles=True)
async def automod(interaction: discord.Interaction,automod_options: str,banworld: str):
    if automod_options == 'add':
        IWordList.append(banworld)
        await interaction.response.send_message(IWordList)
    elif automod_options == 'list':
        await interaction.response.send_message(IWordList)
    else:
        IWordList.remove(banworld)
        await interaction.response.send_message(IWordList)

@automod.error
async def on_automod_error(interaction:discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(str(error), ephemeral=True)

@bot.event
async def on_message(message):
    if(message.author.id == bot.user.id):
        return
    else:
        for  word in IWordList:
            if word in message.content.lower():
                await message.delete()

#Lancement du programme
bot.run(TOKEN)
#librairies
import os
import discord
from discord.ext.commands import has_permissions, MissingPermissions
from discord import app_commands
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
#programming language


#Ngrok ip
@bot.tree.command(description="change the ancient ip to the new ip")
@app_commands.checks.has_role("MinecraftModerator")
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

#Auto moderation
IWordList = []

@app_commands.choices(addordelete = [
    app_commands.Choice(name="add",value='add'),
    app_commands.Choice(name="delete", value='delete')
])
@bot.tree.command(description="add or delete word of the auto moderation")
@app_commands.checks.has_permissions(manage_messages=True,manage_roles=True)
async def automod(interaction: discord.Interaction,addordelete: str,banworld: str):
    if addordelete == 'add':
        IWordList.append(banworld)
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
bot.run(os.getenv("TOKEN"))
from typing import Optional, Union, List

import discord
import os
from discord import app_commands
from dotenv import load_dotenv
from discord.ext import commands
import db
import random
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True
client = commands.Bot(intents=intents,command_prefix='/')

def is_owner(interaction: discord.Interaction):
    if interaction.user.id == interaction.guild.owner_id:
        return True
    else:
        return False

def check_command_permission(interaction: discord.Interaction):
    cmdrole = db.get(str(interaction.guild_id),db.KEYS.CMD_ROLE)
    for role in interaction.user.roles:
        if(role.name == cmdrole):
            return True
    return False


@client.tree.command()
async def kiss(interaction: discord.Interaction,member:discord.Member):
    """Give a user a big smooch"""
    await interaction.response.defer(ephemeral=True)
    print('inside Kiss')
    if member.id==interaction.user.id:
        await interaction.followup.send("you can't kiss yourself",ephemeral=True)
        return
    if member.bot==True:
        await interaction.followup.send("You can't kiss a bot",ephemeral=True)
        return

    nm1=interaction.user.name
    nm2=member.name
    if interaction.user.nick!=None:nm1=interaction.user.nick
    if member.nick!=None:nm2=member.nick

    guild_id=str(interaction.guild_id)
    embed=discord.Embed(color=db.get(guild_id,db.KEYS.EMBED_COLOR),title=f"{nm1} kisses {nm2}")
    gifs=[]
    with open("gifs/kisses.json") as f:
        gifs=json.load(f)
    url=gifs[random.randint(0,len(gifs)-1)]
    #url="https://gifdb.com/images/thumbnail/sexy-kissing-vampire-diaries-tq7ylcy4y7cp3zf6.gif"
    print(f'url:{url},len:{len(gifs)}')
    embed.set_image(url=url)
    await interaction.channel.send(f"<@{member.id}>",embed=embed)
    await interaction.followup.send('done')
    
    #for url in gifs:
    #    embed.description=url
    #    embed.set_image(url=url)
    #    await interaction.channel.send(embed=embed)
    await interaction.followup.send("done")
    return


@client.tree.command(name='setup')
@app_commands.check(is_owner)
async def setup(interaction: discord.Interaction,embed_color: str,role: discord.Role):
    """Set up femdom bot for this server"""
    await interaction.response.defer(ephemeral=True)
    print("inside setup")
    embed_color="0x"+embed_color
    embed_color_int=int(embed_color,16)
    role_name=role.name
    guild_id=str(interaction.guild_id)
    db.set(guild_id,db.KEYS.EMBED_COLOR,embed_color_int)
    db.set(guild_id,db.KEYS.CMD_ROLE,role_name)
    print(db.get(guild_id,db.KEYS.CMD_ROLE))
    print(db.get(guild_id,db.KEYS.EMBED_COLOR))
    await interaction.followup.send('Set up complete',ephemeral=True)
    return

@setup.error
async def setup_error(interaction: discord.Interaction,error):
    print("setup_error",error)
    await interaction.response.send_message("Only the server owner can access this command",ephemeral=True)
    return


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

    #print(cmdrole)
    #client.tree = app_commands.CommandTree(client)
    for guild in client.guilds:
        print("id: ",guild.id,"name: ",guild.name)
        client.tree.copy_global_to(guild=guild)
        await client.tree.sync(guild=guild)
    return

@client.event
async def on_guild_join(guild):
    print("on_guild_join")
    client.tree.copy_global_to(guild=guild)
    await client.tree.sync(guild=guild)
    return




client.run(TOKEN)

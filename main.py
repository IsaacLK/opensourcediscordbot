import os
import discord
import random
from discord.ext import commands

#fill with discord bot token
token = ""
client = commands.Bot(command_prefix='/')
@client.event
async def on_ready():
    print(f'{client.user} now online')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for /help | https://github.com/IsaacLK/opensourcediscordbot'))
    print("code rcan")
@client.command()
async def hello(ctx):    
    await ctx.send("Hello!")

client.run(token)

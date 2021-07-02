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
    embed=discord.Embed(title="Hello!", color=0x003b46)
    await ctx.send(embed=embed)
@client.command()
async def github(ctx):
    embed=discord.Embed(title="Click here to open up the GitHub!", url="https://github.com/IsaacLK/opensourcediscordbot", color=0x003b46)
    await ctx.send(embed=embed)
@client.command()
async def ping(ctx):
    ping = client.latency
    embed=discord.Embed(title="The bot's ping is "+ str(round(ping * 1000)) + "ms", color=0x003b46)
    await ctx.send(embed=embed)
    

client.run(token)

import discord
import os
from discord.ext import commands
from datetime import datetime

intents = discord.Intents().all()

client = commands.Bot(command_prefix='.', intents=intents)
client.colour1=0xFF1DCE
client.admins=[662651445857746946,451763550680121344]
client.launch_time=''
client.remove_command('help')
BOT_TOKEN='' #BOT TOKEN GOES HERE


@client.command()
async def load(ctx, extension):
    isAdmin=False
    for admin in client.admins:
        if admin == ctx.author.id:
            isAdmin=True
            client.load_extension(f'cogs.{extension}')
            print('Loaded - {0}'.format(extension))
            await ctx.send('Loaded - {0}'.format(extension))
    if not isAdmin:
            await ctx.send("Please don't.")

@client.command()
async def unload(ctx, extension):
    isAdmin=False
    for admin in client.admins:
        if admin == ctx.author.id:
            isAdmin=True
            client.unload_extension(f'cogs.{extension}')
            print('Unloaded - {0}'.format(extension))
            await ctx.send('Unloaded - {0}'.format(extension))
    if not isAdmin:
            await ctx.send("Please don't.")

@client.command()
async def reload(ctx, extension):
    isAdmin=False
    for admin in client.admins:
        if admin == ctx.author.id:
            isAdmin=True
            client.unload_extension(f'cogs.{extension}')
            client.load_extension(f'cogs.{extension}')
            print('Reloaded - {0}'.format(extension))
            await ctx.send('Reloaded - {0}'.format(extension))
    if not isAdmin:
            await ctx.send("Please don't.")

@client.command()
async def reloadall(ctx):
    isAdmin=False
    for admin in client.admins:
        if admin == ctx.author.id:
            isAdmin=True
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    client.unload_extension(f'cogs.{filename[:-3]}')
                    client.load_extension(f'cogs.{filename[:-3]}')
                    await ctx.send('Reloaded - {0}'.format(filename[:-3]))
            await ctx.send('Done :smile:')
    if not isAdmin:
            await ctx.send("Please don't.")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(BOT_TOKEN)

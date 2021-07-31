import discord
from discord.ext import commands
from config import settings

client = commands.Bot(command_prefix = settings['prefix'])
# client.remove_command('help')

@client.event
async def on_ready():
    print('Bot is online {0.user}'.format(client))

@client.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Hello, {author.mention}!')

client.run(settings['token'])

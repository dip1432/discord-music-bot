# -*- coding: utf-8 -*-
import os
import discord
import youtube_dl
from discord.ext import commands
from config import settings

client = commands.Bot(command_prefix = settings['prefix'])
# client.remove_command('help')

@client.event
async def on_ready():
    print('Bot is online {0.user}'.format(client))

server, server_id, name_channel = None, None, None

domains = ['https://www.youtube.com', 'http//www.youtube.com', 'https://youtube.be/', 'http://youtube.be/']
async def check_domains(link):
    for x in domains:
        if link.startswith(x):
            return True
    return False

@client.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Hello, {author.mention}!')
async def play(ctx, *, command = None):
    """Воспроизводит музыку"""
    global server, server_id, name_channel
    author = ctx.author
    if command == None:
        server = ctx.guild
        name_channel = author.voice.channel.name
        voice_channel = discord.utils.get(server.voice_channels, name = name_channel)
    params = command.split(' ')
    if len(params) == 1:
        sourse = params[0]
        server = ctx.guild
        name_channel = author.voice.channel.name
        voice_channel = discord.utils.get(server.voice_channels, name=name_channel)
        print('param 1')
    elif len(params) == 3:
        server_id = params[0]
        voice_id = params[1]
        sourse = params[2]
        try:
            server_id = int(server_id)
            voice_id = int(voice_id)
        except:
            await ctx.chanell.send(f'{author.mention}, id сервера или войса должно быть целочисленным!')
            return
        print('param 3')
        server = client.get_guild(server_id)
        voice_channel = discord.utils.get(server.voice_channels, id=voice_id)
    else:
        await ctx.channel.send(f'{author.mention} команда не корректна!')
        return

    voice = discord.utils.get(client.voice_clients, guild = server)
    if voice is None:
        await voice_channel.connect()
        voice = discord.utils.get(client.voice_clients, guild = server)

    if sourse == None:
        pass
    elif sourse.startswith('http'):
        if not check_domains(sourse):
            await ctx.channel.send(f'{author.mention} ссылка не является разрешенной!')
            return
        song_there = os.path.isfile('music/song.mp3')
        try:
            if song_there:
                    os.remove('song.mp3')
        except PermissionError:
            await ctx.chennel.send('Недостаточно прав для удаления файла!')
            return
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([sourse])
        for file in os.listdir('music/'):
            if file.endswith('.mp3'):
                os.rename(file, 'song.mp3')
        voice.play(discord.FFmpegPCMAudio('song.mp3'))
    else:
        voice.play(discord.FFmpegPCMAudio(f'music/{sourse}'))

client.run(settings['token'])


# async def help(ctx):
#     emb = discord.Embed(title='Список команд')

# @client.event
# async def on_member_join(member):
#     channel = client.get_channel(865733476209000449)
#     await channel.send(f'{member.mention} добро пожаловать на сервер!')
#
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     if message.content.startswith('d.help'):
#         await message.channel.send('help!')

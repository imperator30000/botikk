import discord
from discord.ext import commands, tasks
import sympy
import os, platform
from discord.utils import get
import threading

from threading import Thread

from parserr import Ass_bot

client = discord.Client()

bot = commands.Bot(command_prefix='!')
bot_Aki = Ass_bot()


@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(name='t')
async def test(ctx, text):
    flag = bot_Aki.comparison(text, bot_Aki.opts["otv"])[2]
    if not flag:
        await ctx.send('Неверный ввод', tts=True)
    elif flag == "end_game":
        await ctx.send("Игра закончена", tts=True)
    else:
        bot_Aki.otvet(flag)
        b = bot_Aki.question()
        if b:
            await ctx.send(b, tts=True)
        else:
            a, b = bot_Aki.end_game()
            await ctx.send(a, tts=True)
            await ctx.send(b)
            await ctx.send("Я угадал?")
            flag = bot_Aki.comparison(text, bot_Aki.opts["menu"])[2]
            if flag == "a_propose_yes":
                bot_Aki.menu_win(flag)
                flag = bot_Aki.comparison(text, bot_Aki.opts["menu"])[2]


@bot.command(name='start_akinator')
async def start_akinator(ctx, text):
    print(ctx)
    flag = bot_Aki.comparison(text, bot_Aki.opts["language"])
    print(flag)
    if not flag:
        await ctx.send('Неверный ввод', tts=True)
    else:
        await ctx.send('Игра началась', tts=True)
        bot_Aki.main(flag[2])
        flag = bot_Aki.question()
        if flag:
            await ctx.send(flag, tts=True)
        # if flag == "end_game":
        #     bot_Aki.end_game().picture()
        #     await ctx.send(bot_Aki.end_game().picture(), tts=True)
        # else:
        #     await ctx.send(flag, tts=True)


@bot.command(name='meme')
async def meme(ctx, text):
    await ctx.send(bot_Aki.png(text))


# @bot.command(aliases=['paly', 'queue', 'que'])
# async def play(ctx):
#     guild = ctx.guild
#     voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
#     audio_source = discord.FFmpegPCMAudio('Нервы.mp3')
#     if not voice_client.is_playing():
#         voice_client.play(audio_source, after=None)


# @bot.event
# async def on_ready():
#     print(f'We have logged in as {client.user}')
#
#
# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
#     if message.content[0] == '!':
#         bot.command()
#     s = message.content
#     # if message.content.startswith('$hello'):
#     await message.channel.send(s)


bot.run('OTY1MzMxOTk0MDkzNDQ5Mjk2.Ylxpeg.pJ68mNIkGlabjjarGT1lT5BQoxE')

from parserr import Ass_bot, Picture
import sympy

import discord
from discord.ext import commands

from youtube_dl import YoutubeDL
from asyncio import sleep
from black_jack import Game, bolshe_menshe, russian_roulette

client = discord.Client()

bot = commands.Bot(command_prefix='!')
BlackJack_d = dict()
MoreLess_d = dict()
RussianRoulette_d = dict()
bot_Aki_d = dict()
bot_meme = Picture()
flag_2_d = dict()
flag_3_d = dict()
f = open('help.txt', 'r', encoding='utf-8')
help_txt = f.read()
f.close()


def cut(txt):
    txt = str(txt)
    ll = len(txt) // 50 + 1
    arr = [0] + [i * 50 for i in range(1, ll)]

    if len(txt) % 50:
        arr.append(len(txt))
    ans = []
    for i in range(len(arr) - 1):
        ans.append('>>>' + txt[arr[i]:arr[i + 1]] + '>>>')
    ans[-1] = ans[-1][:-3]
    ans[0] = ans[0][3:]
    return ans


@bot.command()
async def AkinatorStart(ctx, text):

    if ctx.message.author not in bot_Aki_d:
        bot_Aki_d[ctx.message.author] = Ass_bot(ctx.message.author)
        flag_2_d[ctx.message.author] = False
        flag_3_d[ctx.message.author] = False

    if not bot_Aki_d[ctx.message.author].run:
        bot_Aki_d[ctx.message.author].__init__(ctx.message.author)
        flag = bot_Aki_d[ctx.message.author].comparison(text, bot_Aki_d[ctx.message.author].opts["language"])
        if not flag:
            await ctx.send('Неверный ввод', tts=True)
        else:
            await ctx.send('Игра началась', tts=True)
            bot_Aki_d[ctx.message.author].main(flag[2])
            flag = bot_Aki_d[ctx.message.author].question()
            if flag:
                await ctx.send(flag, tts=True)
                flag_2_d[ctx.message.author] = True
    else:
        await ctx.send('Ваша игра идёт!', tts=True)


@bot.command()
async def Akinator(ctx, text):
    if ctx.message.author not in bot_Aki_d:
        await ctx.send('Запустите игру', tts=True)
        return
    if bot_Aki_d[ctx.message.author].run:
        if flag_2_d[ctx.message.author]:  # Основной цикл программы вопрос ответ
            flag = bot_Aki_d[ctx.message.author].comparison(text, bot_Aki_d[ctx.message.author].opts["otv"])[2]
            if not flag:  # Если неверный ввод
                await ctx.send('Неверный ввод', tts=True)
            elif flag == "end_game":  # закончить игру
                await ctx.send("Игра закончена", tts=True)
                flag_2_d[ctx.message.author] = False
            else:
                bot_Aki_d[ctx.message.author].otvet(flag)
                b = bot_Aki_d[ctx.message.author].question()
                if b:
                    await ctx.send(b, tts=True)
                else:
                    a, b, flag_2_d[ctx.message.author] = bot_Aki_d[ctx.message.author].end_game()
                    await ctx.send(a, tts=True)
                    await ctx.send(b)
                    await ctx.send("Я угадал?", tts=True)
                    flag_3_d[ctx.message.author] = True
        elif (not flag_2_d[ctx.message.author]) or flag_3_d[ctx.message.author]:  # Угадал да или нет
            flag = bot_Aki_d[ctx.message.author].comparison(text, bot_Aki_d[ctx.message.author].opts["menu"])[2]
            print(flag)
            if flag == "a_propose_no":
                await ctx.send("Продолжение", tts=True)
                bot_Aki_d[ctx.message.author].f()
                flag_3_d[ctx.message.author], flag_2_d[ctx.message.author] = False, True
                await ctx.send(bot_Aki_d[ctx.message.author].question(), tts=True)
            else:
                await ctx.send("Игра окончена", tts=True)
                flag_3_d[ctx.message.author], flag_2_d[ctx.message.author] = False, False
        else:
            await ctx.send("Ваша команда не может быть выполнена", tts=True)
    else:
        await ctx.send('Запустите игру', tts=True)

@bot.command(name='meme')
async def meme(ctx, text):
    bot_meme.__init__()
    await ctx.send(bot_meme.png(text))


@bot.command()
async def Help(ctx):
    output = help_txt
    await ctx.send(output)


@bot.command(text='join')
async def join(ctx):
    if not ctx.message.author.voice:
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command()
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()


@bot.command()
async def SolveTheEquation(ctx, text):
    text = text.replace('^', '**')
    alfb = 'qwertyuiopasdfghjklzxcvbnmёйцукенгшщзхъфывапролджэячсмитьбю'
    text = str(text).lower()
    text_ = set(text)
    count = 0
    sym = ''
    for i in text_:
        if i in alfb:
            count += 1
            sym = sympy.symbols(i)
    if count != 1:
        await ctx.send('Некорректный ввод', tts=True)
        return
    ur = text.split('=')
    ur1 = sympy.sympify(str(ur[0]))
    ur2 = sympy.sympify(str(ur[1]))
    print(text, sympy.solve(ur1 - ur2, sym)[0])
    arr = [float(sympy.sympify(i.evalf())) for i in sympy.solve(ur1 - ur2, sym) if
           'I' not in str(sympy.sympify(i.evalf()))]
    if arr:
        for i in arr:
            txts = cut(i)
            for g in txts:
                await ctx.send(g)
    else:
        await ctx.send('нет корней в действительных числах')


FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format': 'worstaudio/best',
               'noplaylist': 'True', 'simulate': 'True', 'preferredquality': '192', 'preferredcodec': 'mp3',
               'key': 'FFmpegExtractAudio'}


@bot.command()
async def play(ctx, arg):
    global vc
    try:
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
    except:
        print('Уже подключен или не удалось подключиться')

    if vc.is_playing():
        await ctx.send(f'{ctx.message.author.mention}, музыка уже проигрывается.')

    else:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(arg, download=False)

        URL = info['formats'][0]['url']

        vc.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=URL, **FFMPEG_OPTIONS))

        while vc.is_playing():
            await sleep(1)
        if not vc.is_paused():
            await vc.disconnect()


@bot.command()
async def BlackJackStart(ctx):
    if ctx.message.author not in BlackJack_d:
        BlackJack_d[ctx.message.author] = Game(ctx.message.author)
    if not BlackJack_d[ctx.message.author].run:
        await ctx.send(BlackJack_d[ctx.message.author].start())

    else:
        await ctx.send('Игра уже идёт!')


@bot.command()
async def BlackJack(ctx, mes):
    if BlackJack_d[ctx.message.author].run:
        tt = BlackJack_d[ctx.message.author].hod(mes, ctx.message.author)
        await ctx.send(tt)
        if not BlackJack_d[ctx.message.author].run:
            BlackJack_d[ctx.message.author].__init__(ctx.message.author)
    else:
        await ctx.send('Запустите игру!')


@bot.command()
async def BlackJackStop(ctx):
    if BlackJack_d[ctx.message.author].run:
        BlackJack_d[ctx.message.author].__init__(ctx.message.author)
        await ctx.send('Игра завершена!')


@bot.command()
async def MoreLessStart(ctx):
    if ctx.message.author not in MoreLess_d:
        MoreLess_d[ctx.message.author] = bolshe_menshe(ctx.message.author)
    if MoreLess_d[ctx.message.author].run:
        await ctx.send(MoreLess_d[ctx.message.author].start())

    else:
        await ctx.send('Игра уже идёт!')


@bot.command()
async def MoreLess(ctx, mes):
    if MoreLess_d[ctx.message.author].run:
        await ctx.send(MoreLess_d[ctx.message.author].hod(mes, ctx.message.author))
        if not MoreLess_d[ctx.message.author].run:
            MoreLess_d[ctx.message.author].__init__(ctx.message.author)
    else:
        await ctx.send('Запустите игру!')


@bot.command()
async def MoreLessStop(ctx):
    if MoreLess_d[ctx.message.author].run:
        MoreLess_d[ctx.message.author].__init__(ctx.message.author)
        await ctx.send('Игра завершена!')


@bot.command(name='RussianRouletteteStart')
async def RussianRouletteteStart(ctx, mes):
    print(str(ctx.message.author), RussianRoulette_d)
    if ctx.message.author not in RussianRoulette_d:
        print(str(ctx.message.author), RussianRoulette_d)
        RussianRoulette_d[ctx.message.author] = russian_roulette(ctx.message.author)
    if not RussianRoulette_d[ctx.message.author].run:
        await ctx.send(RussianRoulette_d[ctx.message.author].start(mes))
    else:
        await ctx.send('Игра уже идёт!')


@bot.command()
async def RussianRoulettete(ctx, mes):
    if RussianRoulette_d[ctx.message.author].run:
        await ctx.send(RussianRoulette_d[ctx.message.author].hod(mes, ctx.message.author))
        if not RussianRoulette_d[ctx.message.author].run:
            RussianRoulette_d[ctx.message.author].__init__(ctx.message.author)
    else:
        await ctx.send('Запустите игру!')


@bot.command()
async def RussianRouletteteStop(ctx):
    if RussianRoulette_d[ctx.message.author].run:
        RussianRoulette_d[ctx.message.author].__init__(ctx.message.author)
        await ctx.send('Игра завершена!')


bot.run('OTY1MzMxOTk0MDkzNDQ5Mjk2.Ylxpeg.JCImrbcJ0wvkYbmomnH4NarawOg')

import discord
from discord.ext import commands, tasks
from parserr import Ass_bot, Picture

client = discord.Client()
bot = commands.Bot(command_prefix='!')
bot_Aki = Ass_bot()
bot_meme = Picture()
flag_2 = False
flag_3 = False


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


@bot.command(name='start_akinator')
async def start_akinator(ctx, text):
    global flag_2
    bot_Aki.__init__()
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
            flag_2 = True


@bot.command(name='t')
async def test(ctx, text):
    global flag_2, flag_3
    if flag_2:  # Основной цикл программы вопрос ответ
        flag = bot_Aki.comparison(text, bot_Aki.opts["otv"])[2]
        if not flag:  # Если неверный ввод
            await ctx.send('Неверный ввод', tts=True)
        elif flag == "end_game":  # закончить игру
            await ctx.send("Игра закончена", tts=True)
            flag_2 = False
        else:
            bot_Aki.otvet(flag)
            b = bot_Aki.question()
            if b:
                await ctx.send(b, tts=True)
            else:
                a, b, flag_2 = bot_Aki.end_game()
                await ctx.send(a, tts=True)
                await ctx.send(b)
                await ctx.send("Я угадал?", tts=True)
                flag_3 = True
    elif (not flag_2) or flag_3:  # Угадал да или нет
        flag = bot_Aki.comparison(text, bot_Aki.opts["menu"])[2]
        print(flag)
        if flag == "a_propose_no":
            await ctx.send("Продолжение", tts=True)
            bot_Aki.f()
            flag_3, flag_2 = False, True
            await ctx.send(bot_Aki.question(), tts=True)
        else:
            await ctx.send("Игра окончена", tts=True)
            flag_3, flag_2 = False, False
    else:
        await ctx.send("Ваша команда не может быть выполнена", tts=True)


@bot.command(name='meme')
async def meme(ctx, text):
    bot_meme.__init__()
    await ctx.send(bot_meme.png(text))


bot.run('OTY1MzMxOTk0MDkzNDQ5Mjk2.Ylxpeg.8hG9cDizSYOGbSDTUIMvhJ8TS2w')

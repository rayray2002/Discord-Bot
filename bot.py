#!/usr/bin/python3

import datetime
import time
import discord
from os import makedirs
import shutil
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from url_to_df import *

token_file = open('./token.txt', 'r')
TOKEN = token_file.read()

banned = ['星爆', '星報', 'sao', '興報', '艾恩格朗特', '雜燴', '標槍', 'sbs', '876', 'kirito',
          'urst', '585', '師大巴士', '斬', '流擊', '封閉者', '同仁', '闡釋者', '心爆', '桐谷',
          '核仁', '星和爆', '砸慧', 'Sword', '閃耀', 'vu/', '化成', '刀劍神域', '流展', '四方',
          '聖母', '幫我撐十秒', 'mmorpg', '@!556463593294528542', '@!699478459021524992',
          '十六', '和人', '封弊']
USER_ID = {'ray': 540149116374614016, 'justin': 540149446596493359, 'pg': 556463593294528542, '標槍': 699478459021524992}
SERVER_ID = {'poke': 878300201541062656, 'jennifer': 843761765174607882, 'ouo': 679353041165746176}

PREFIX = '!'
bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())
slash = SlashCommand(bot)


@bot.event
async def on_ready():
    dt = datetime.datetime.now()
    print(f'Logged in as {bot.user} at {dt.strftime("%Y/%m/%d %H:%M:%S")}')
    game = discord.Game(f'執法中｜{PREFIX}help')
    await bot.change_presence(status=discord.Status.online, activity=game)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.guild.id == SERVER_ID['poke']:
        return

    dt = datetime.datetime.now()
    print(f'{dt.strftime("%Y/%m/%d %H:%M:%S")}: {message.author} in {message.guild.name}')
    print(message.content)

    if message.guild.id == SERVER_ID['jennifer']:
        if '涓涓' in message.content:
            await message.channel.send('是Ray可愛的小寶貝')

    elif message.guild.id == SERVER_ID['ouo']:
        await message.add_reaction('<:gagalove:879008993626947625>')

        if message.content == '噓':
            await message.channel.send('噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓')

        if '嘎' in message.content:
            await message.channel.send(f'<@!{USER_ID["justin"]}> 臭甲')
            await message.channel.send(file=discord.File('./img/gagalove.png'))

        text = ''.join(message.content.split(' '))
        for ban in banned:
            if ban in text.lower():
                await message.channel.send(f'<@!{message.author.id}> 噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓')

    await bot.process_commands(message)


@slash.slash(name="test")
async def _test(ctx: SlashContext):
    embed = discord.Embed(title="embed test")
    await ctx.send(content="test", embeds=[embed])


@bot.command()
async def say(ctx, arg):
    if ctx.message.author.id == USER_ID['ray']:
        await ctx.send(arg)


@bot.command()
async def newrole(ctx, arg):
    if ctx.message.author.id in (USER_ID['ray'], USER_ID['justin']):
        await ctx.guild.create_role(name=arg)
        await ctx.send(f'Role {arg} created')


@bot.command(pass_context=True)
async def giverole(ctx, user: discord.Member, role: discord.Role):
    if ctx.message.author.id in (USER_ID['ray'], USER_ID['justin']):
        await user.add_roles(role)
        await ctx.send(f"{ctx.author.name}, {user.name} has been giving a role called: {role.name}")


@bot.command()
async def course(ctx, *, arg):
    if not path.exists('./out'):
        makedirs('./out')
    if not path.exists('./save_csv'):
        makedirs('./save_csv')

    lines = arg.split('\n')
    schedule = [[0] * 15 for i in range(7)]
    try:
        name = lines[0]
        fields = lines[1]
        for i in range(2, 9):
            raw = lines[i]
            if len(raw) > 1:
                periods = raw[1:].split(',')
                for period in periods:
                    schedule[i - 2][class_map[period.strip()]] = 1
        dpts = []
        for i in range(9, len(lines)):
            dpts.append(lines[i])
        print(name + ' imported')

    except IndexError:
        await ctx.send('格式錯誤')
        return

    if not path.exists('./out/' + name + '.xlsx'):
        open('./out/' + name + '.xlsx', 'w')
    writer = pd.ExcelWriter('./out/' + name + '.xlsx')

    try:
        general_filter(name, writer, schedule, fields)
        language_filter(name, writer, schedule)
        pe_filter(name, writer, schedule)
        for dpt in dpts:
            department_filter(name, dpt, writer, schedule)

    except requests.exceptions.ConnectionError:
        await ctx.send('課程網死了')
        return
    except ValueError:
        await ctx.send('系所代碼錯誤')
        return
    except Exception as e:
        print(e)
        await ctx.send(f'不知道為什麼反正錯了, {e}')
        return

    writer.save()
    print(f'{name}.xlsx save success')
    await ctx.send(file=discord.File(f'./out/{name}.xlsx'))


@bot.command()
async def reset(ctx):
    if ctx.message.author.id == USER_ID['ray']:
        shutil.rmtree('./save_csv')
        shutil.rmtree('./new_csv')
        shutil.rmtree('./out')
        await ctx.send('Reset')


@bot.command()
async def show(ctx, arg):
    text = arg.lower()
    for t in text:
        if t == 'a':
            await ctx.send('https://play.pokemonshowdown.com/sprites/ani/unown.gif')
        elif t == ' ':
            await ctx.send(file=discord.File('./img/space.png'))
        elif t == '?':
            await ctx.send('https://play.pokemonshowdown.com/sprites/ani/unown-question.gif')
        elif 'b' <= t <= 'z':
            await ctx.send(f'https://play.pokemonshowdown.com/sprites/ani/unown-{t}.gif')
        else:
            await ctx.send(t)
        time.sleep(0.1)


bot.run(TOKEN)

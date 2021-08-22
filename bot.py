#!/usr/bin/python3

import datetime
import discord
from os import makedirs
import shutil
from url_to_df import *

token_file = open('token.txt', 'r')
TOKEN = token_file.read()

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)
dt = datetime.datetime.now()


def course_helper(text):
    if not path.exists('./out'):
        makedirs('./out')
    if not path.exists('./save_csv'):
        makedirs('./save_csv')

    lines = text.split('\n')
    name = lines[1]
    fields = lines[2]
    schedule = [[0] * 15 for i in range(7)]
    for i in range(3, 10):
        raw = lines[i]
        if len(raw) > 1:
            periods = raw[1:].split(',')
            for period in periods:
                schedule[i - 3][class_map[period]] = 1
    dpts = []
    for i in range(10, len(lines)):
        dpts.append(lines[i])
    print(name + ' imported')
    if not path.exists('./out/' + name + '.xlsx'):
        open('./out/' + name + '.xlsx', 'w')
    writer = pd.ExcelWriter('./out/' + name + '.xlsx')

    general_filter(name, writer, schedule, fields)
    language_filter(name, writer, schedule)
    pe_filter(name, writer, schedule)
    for dpt in dpts:
        department_filter(name, dpt, writer, schedule)

    writer.save()
    print(name + '.xlsx save success')
    return './out/' + name + '.xlsx'


@client.event
async def on_ready():
    print(f'Logged in as {client.user} at {dt.strftime("%Y/%m/%d %H:%M:%S")}')
    game = discord.Game('執法中')
    await client.change_presence(status=discord.Status.online, activity=game)


banned = ['星爆', '星報', 'sao', '興報', '艾恩格朗特', '雜燴', '標槍', 'sbs', '876', 'kirito',
          'urst', '585', '師大巴士', '斬', '流擊', '封閉者', '同仁', '闡釋者', '心爆', '桐谷',
          '核仁', '星和爆', '嘎', '砸慧', 'Sword', '閃耀', 'vu/', '化成', '刀劍神域', '流展',
          '四方', '聖母', ':', '幫我撐十秒', 'mmorpg', '@!556463593294528542', '@!699478459021524992',
          '十六', '和人', '封弊']


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(f'{dt.strftime("%Y/%m/%d %H:%M:%S")}: {message.author} in {message.guild.name}')
    print(message.content)

    if message.guild.name == '涓涓小教室':
        if message.content == '涓涓':
            await message.channel.send('是Ray可愛的小寶貝')

    elif message.guild.name == 'ouo':
        if message.channel.name == '隨便拉':
            if message.content.startswith('!course'):
                try:
                    file = course_helper(message.content)
                    # await message.channel.send('成功')
                    await message.channel.send(file=discord.File(file))
                except requests.exceptions.ConnectionError:
                    await message.channel.send('課程網死了')
                except IndexError:
                    await message.channel.send('格式錯誤')
                except Exception as e:
                    print(e)
                    await message.channel.send('不知道為什麼反正錯了', e)

            elif message.content.startswith('!reset') and '#4581' in message.author:
                shutil.rmtree('./save_csv')
                shutil.rmtree('./out')
                await message.channel.send('Reset')

        if message.content == '噓':
            await message.channel.send('噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓')

        text = ''.join(message.content.split(' '))
        for ban in banned:
            if ban in text.lower():
                await message.channel.send('噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓噓')


client.run(TOKEN)

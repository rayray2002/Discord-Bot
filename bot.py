#!/usr/bin/python3

import configparser
import datetime
import os
import shutil
import time

import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow

from url_to_df import *

banned = ['星爆', '星報', 'sao', '興報', '艾恩格朗特', '雜燴', '標槍', 'sbs', '876', 'kirito',
          'urst', '585', '師大巴士', '斬', '流擊', '封閉者', '同仁', '闡釋者', '心爆', '桐谷',
          '核仁', '星和爆', '砸慧', 'Sword', '閃耀', 'vu/', '化成', '刀劍神域', '流展', '四方',
          '聖母', '幫我撐十秒', 'mmorpg', '@!556463593294528542', '@!699478459021524992',
          '十六', '和人', '封弊']
USER_ID = {'ray': 540149116374614016, 'justin': 540149446596493359, 'pg': 556463593294528542, '標槍': 699478459021524992}
SERVER_ID = {'poke': 878300201541062656, 'jennifer': 843761765174607882, 'ouo': 679353041165746176}

PREFIX = '&'
bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    dt = datetime.datetime.now()
    print(f'Logged in as {bot.user} at {dt.strftime("%Y/%m/%d %H:%M:%S")}')
    game = discord.Game(f'執法中｜{PREFIX}help')
    await bot.change_presence(status=discord.Status.online, activity=game)


@slash.slash(name="ping")
async def _ping(ctx):  # Defines a new "context" (ctx) command called "ping."
    await ctx.send(f"{bot.latency * 1000}ms")


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


@slash.slash(name='say',
             description='Say Something')
async def _say(ctx, text):
    if ctx.author.id == USER_ID['ray']:
        await ctx.send(text)


@slash.slash(name='show',
             description="Show something")
async def _show(ctx, text):
    text = text.lower()
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


def get_config(user_id, name='course'):
    config = configparser.ConfigParser()
    if os.path.exists(f'configs/{user_id}.ini'):
        config.read(f'configs/{user_id}.ini')
    else:
        config['general'] = {}
        print(name)
        config['general']['name'] = str(name)
        config['general']['field'] = ''
        config['general']['department'] = ''
        config['schedule'] = {}
        for i in range(7):
            config['schedule'][str(i)] = ','.join(['0' for j in range(15)])
    return config


@slash.subcommand(base='course',
                  name='name',
                  description="設定名字")
async def _course_name(ctx, name):
    user = await bot.fetch_user(ctx.author.id)
    config = get_config(ctx.author.id, user.name)
    config['general']['name'] = name
    with open(f'configs/{ctx.author.id}.ini', 'w') as f:
        config.write(f)
        await ctx.send('設定完成')


@slash.subcommand(base='course',
                  name='schedule',
                  description="設定課表",
                  options=[
                      create_option(
                          name="星期",
                          description="This is the first option we have.",
                          option_type=4,
                          required=True,
                          choices=[
                              create_choice(
                                  name="一",
                                  value=0
                              ),
                              create_choice(
                                  name="二",
                                  value=1
                              ),
                              create_choice(
                                  name="三",
                                  value=2
                              ),
                              create_choice(
                                  name="四",
                                  value=3
                              ),
                              create_choice(
                                  name="五",
                                  value=4
                              ),
                              create_choice(
                                  name="六",
                                  value=5
                              ),
                              create_choice(
                                  name="日",
                                  value=6
                              ),
                          ]
                      )
                  ])
async def _course_schedule(ctx, 星期):
    # await ctx.send(content=f"星期{星期}")
    select = create_select(
        options=[  # the options in your dropdown
            create_select_option("沒課", value="-1", emoji="🆓"),
            create_select_option("0", value="0", emoji="0️⃣"),
            create_select_option("1", value="1", emoji="1️⃣"),
            create_select_option("2", value="2", emoji="2️⃣"),
            create_select_option("3", value="3", emoji="3️⃣"),
            create_select_option("4", value="4", emoji="4️⃣"),
            create_select_option("5", value="5", emoji="5️⃣"),
            create_select_option("6", value="6", emoji="6️⃣"),
            create_select_option("7", value="7", emoji="7️⃣"),
            create_select_option("8", value="8", emoji="8️⃣"),
            create_select_option("9", value="9", emoji="9️⃣"),
            create_select_option("10", value="10", emoji="🔟"),
            create_select_option("A", value="11", emoji="🅰️"),
            create_select_option("B", value="12", emoji="🅱️"),
            create_select_option("C", value="13", emoji="🅲"),
            create_select_option("D", value="14", emoji="🅳"),
        ],
        placeholder="設定課表",  # the placeholder text to show when no options have been chosen
        custom_id=f'schedule-{ctx.author.id}-{星期}',
        min_values=1,
        max_values=15,
    )
    # print(ctx.author.id)
    await ctx.send("設定課表", components=[create_actionrow(select)])


@slash.subcommand(base='course',
                  name='field',
                  description="設定通識領域")
async def _course_field(ctx):
    select = create_select(
        options=[  # the options in your dropdown
            create_select_option("全部", value="-1", emoji="🈵"),
            create_select_option("1", value="1", emoji="1️⃣"),
            create_select_option("2", value="2", emoji="2️⃣"),
            create_select_option("3", value="3", emoji="3️⃣"),
            create_select_option("4", value="4", emoji="4️⃣"),
            create_select_option("5", value="5", emoji="5️⃣"),
            create_select_option("6", value="6", emoji="6️⃣"),
            create_select_option("7", value="7", emoji="7️⃣"),
            create_select_option("8", value="8", emoji="8️⃣"),
        ],
        placeholder="設定通識領域",  # the placeholder text to show when no options have been chosen
        custom_id=f'field-{ctx.author.id}',
        min_values=1,
        max_values=8,
    )
    # print(ctx.author.id)
    await ctx.send("設定通識領域", components=[create_actionrow(select)])


@bot.event
async def on_component(ctx: ComponentContext):
    # print(ctx.component)
    if 'schedule' in ctx.component['custom_id']:
        # print(ctx.selected_options)
        info = ctx.component['custom_id'].split('-')
        # await ctx.send(content=f"{info[1]}星期{info[2]}{ctx.selected_options}")
        user = await bot.fetch_user(info[1])
        config = get_config(info[1], user.name)
        config['schedule'][info[2]] = ','.join(['1' if str(i) in ctx.selected_options else '0' for i in range(15)])
        with open(f'configs/{info[1]}.ini', 'w') as f:
            config.write(f)
            await ctx.send('設定完成')

    if 'field' in ctx.component['custom_id']:
        # print(ctx.selected_options)
        info = ctx.component['custom_id'].split('-')
        # await ctx.send(content=f"{info[1]} {ctx.selected_options}")

        user = await bot.fetch_user(info[1])
        config = get_config(info[1], user.name)
        field_list = ['1' if str(i) in ctx.selected_options or '-1' in ctx.selected_options else '0' for i in
                      range(1, 9)]

        fields = ''
        for i, f in enumerate(field_list):
            if f == '1':
                fields += str(i + 1)
        config['general']['field'] = fields

        with open(f'configs/{info[1]}.ini', 'w') as f:
            config.write(f)
            await ctx.send('設定完成')


@slash.subcommand(base='course',
                  name='department',
                  description="設定系所")
async def _course_field(ctx, departments):
    department = departments.split(',')
    for i, d in enumerate(department):
        department[i] = d.strip()

    user = await bot.fetch_user(ctx.author.id)
    config = get_config(ctx.author.id, user.name)
    config['general']['department'] = ','.join(department)
    with open(f'configs/{ctx.author.id}.ini', 'w') as f:
        config.write(f)
        await ctx.send('設定完成')


@slash.subcommand(base='course',
                  name='profile',
                  description="查看資訊")
async def _course_profile(ctx):
    user = await bot.fetch_user(ctx.author.id)
    config = get_config(ctx.author.id, user.name)
    name = config['general']['name']
    fields = 'A' + config['general']['field']
    schedule = []
    for i in range(7):
        schedule.append(config['schedule'][f'{i}'].split(','))

    dept = 'None'
    if config['general']['department'] != '':
        dept = config['general']['department'].split(',')

    schedule_vertical = []
    for i in range(15):
        if i == 11:
            row = ['A']
        elif i == 12:
            row = ['B']
        elif i == 13:
            row = ['C']
        elif i == 14:
            row = ['D']
        else:
            row = [i]
        for j in range(7):
            if schedule[j][i] == '0':
                row.append(' ')
            else:
                row.append('●')
        schedule_vertical.append(row)

    s = ['        一    二     三    四    五    六    日']
    # This needs to be adjusted based on expected range of values or   calculated dynamically
    for data in schedule_vertical:
        s.append('|'.join([str(item).center(5, ' ') for item in data]))
    d = '```' + '\n'.join(s) + '```'

    embed = discord.Embed(title="選課資訊", color=discord.Color.blue())
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.add_field(name="名字", value=name, inline=True)
    embed.add_field(name="通識領域", value=fields, inline=True)
    embed.add_field(name="系所", value=dept, inline=True)
    embed.add_field(name="課表", value=d, inline=False)
    embed.set_footer(text="台大選課小幫手")
    await ctx.send(embed=embed)


@slash.subcommand(base='course',
                  name='run',
                  description="輸出結果")
async def _course_run(ctx):
    config = get_config(ctx.author.id)
    name = config['general']['name']
    fields = config['general']['field']
    schedule = []
    for i in range(7):
        schedule.append([int(s) for s in config['schedule'][f'{i}'].split(',')])
    dpts = config['general']['department'].split(',')
    # print(name, fields, schedule, dpts)
    await ctx.send('執行中')

    if not path.exists(f'./out/{name}.xlsx'):
        open(f'./out/{name}.xlsx', 'w')
    writer = pd.ExcelWriter(f'./out/{name}.xlsx')

    try:
        general_filter(name, writer, schedule, fields)
        language_filter(name, writer, schedule)
        pe_filter(name, writer, schedule)
        for dpt in dpts:
            if len(dpt) > 0:
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


@slash.slash(name='reset',
             description='Reset CSVs')
async def _reset(ctx):
    if ctx.message.author.id == USER_ID['ray']:
        shutil.rmtree('./save_csv')
        shutil.rmtree('./new_csv')
        shutil.rmtree('./out')
        await ctx.send('Reset')


# @bot.command()
# async def course(ctx, *, arg):
#     if not path.exists('./out'):
#         os.makedirs('./out')
#     if not path.exists('./save_csv'):
#         os.makedirs('./save_csv')
#
#     lines = arg.split('\n')
#     schedule = [[0] * 15 for i in range(7)]
#     try:
#         name = lines[0]
#         fields = lines[1]
#         for i in range(2, 9):
#             raw = lines[i]
#             if len(raw) > 1:
#                 periods = raw[1:].split(',')
#                 for period in periods:
#                     schedule[i - 2][class_map[period.strip()]] = 1
#         dpts = []
#         for i in range(9, len(lines)):
#             dpts.append(lines[i])
#         print(name + ' imported')
#
#     except IndexError:
#         await ctx.send('格式錯誤')
#         return
#
#     if not path.exists('./out/' + name + '.xlsx'):
#         open('./out/' + name + '.xlsx', 'w')
#     writer = pd.ExcelWriter('./out/' + name + '.xlsx')
#
#     try:
#         general_filter(name, writer, schedule, fields)
#         language_filter(name, writer, schedule)
#         pe_filter(name, writer, schedule)
#         for dpt in dpts:
#             department_filter(name, dpt, writer, schedule)
#
#     except requests.exceptions.ConnectionError:
#         await ctx.send('課程網死了')
#         return
#     except ValueError:
#         await ctx.send('系所代碼錯誤')
#         return
#     except Exception as e:
#         print(e)
#         await ctx.send(f'不知道為什麼反正錯了, {e}')
#         return
#
#     writer.save()
#     print(f'{name}.xlsx save success')
#     await ctx.send(file=discord.File(f'./out/{name}.xlsx'))


token_file = open('./token.txt', 'r')
TOKEN = token_file.read()
bot.run(TOKEN)

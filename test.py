import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.context import MenuContext, ComponentContext
from discord_slash.model import ContextMenuType
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow
import configparser
import os

bot = commands.Bot(command_prefix="&", intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@slash.slash(name="ping")
async def _ping(ctx):  # Defines a new "context" (ctx) command called "ping."
    await ctx.send(f"{bot.latency * 1000}ms")


def get_config(user_id, name='course'):
    config = configparser.ConfigParser()
    if os.path.exists(f'configs/{user_id}.ini'):
        config.read(f'configs/{user_id}.ini')
    else:
        config['general'] = {}
        print(name)
        config['general']['name'] = str(name)
        config['general']['field'] = ','.join(['0' for i in range(8)])
        config['schedule'] = {}
        for i in range(7):
            config['schedule'][str(i)] = ','.join(['0' for j in range(13)])
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
        ],
        placeholder="設定課表",  # the placeholder text to show when no options have been chosen
        custom_id=f'schedule-{ctx.author.id}-{星期}',
        min_values=1,
        max_values=13,
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
        config['schedule'][info[2]] = ','.join(['1' if str(i) in ctx.selected_options else '0' for i in range(13)])
        with open(f'configs/{info[1]}.ini', 'w') as f:
            config.write(f)
            await ctx.send('設定完成')

    if 'field' in ctx.component['custom_id']:
        # print(ctx.selected_options)
        info = ctx.component['custom_id'].split('-')
        # await ctx.send(content=f"{info[1]} {ctx.selected_options}")

        user = await bot.fetch_user(info[1])
        config = get_config(info[1], user.name)
        config['general']['field'] = ','.join(
            ['1' if str(i) in ctx.selected_options or '-1' in ctx.selected_options else '0' for i in range(1, 9)])
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
    config = get_config(ctx.author.id)
    name = config['general']['name']
    field = config['general']['field'].split(',')
    fields = 'A'
    for i, f in enumerate(field):
        if f == '1':
            fields += str(i + 1)
    schedule = []
    for i in range(7):
        schedule.append(config['schedule'][f'{i}'].split(','))
    dept = config['general']['department'].split(',')
    print(name, fields, schedule, dept)

    schedule_vertical = []
    for i in range(13):
        if i == 11:
            row = ['A']
        elif i == 12:
            row = ['B']
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
    embed.add_field(name="系所", value=config['general']['department'], inline=True)
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
        schedule.append(config['schedule'][f'{i}'].split(','))
    dept = config['general']['department'].split(',')
    print(name, fields, schedule, dept)
    await ctx.send('run')


token_file = open('./token.txt', 'r')
TOKEN = token_file.read()
bot.run(TOKEN)

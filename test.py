import discord
import time
from discord.ext import commands

token_file = open('./token.txt', 'r')
TOKEN = token_file.read()

client = discord.Client()
bot = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    game = discord.Game('執法中')
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.content)


@bot.command()
async def foo(ctx, arg):
    print('foo')
    await ctx.send(arg)


# client.run(TOKEN)
bot.run(TOKEN)

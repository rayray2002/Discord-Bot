import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@slash.slash(name="test", description="Sends message.")
async def test(ctx: SlashContext):
    print('test')
    embed = discord.Embed(title="embed test")
    await ctx.send(content="test", embeds=[embed])


token_file = open('./token.txt', 'r')
TOKEN = token_file.read()
bot.run(TOKEN)

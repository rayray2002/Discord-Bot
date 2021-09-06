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


bot.run("ODc1NDE0OTYyOTM0MjY3OTc2.YRVLtw.VsBiyXCeNlgSpFk71K8RH2GBLZw")

import discord
from discord.ext.commands.bot import Bot
import CantocheBotPDF
from discord.ext import commands

with open('BotToken.txt', 'r') as f:
    TOKEN = f.readline()
    f.close()

PREFIX = '!'
INTENTS = discord.Intents.default()
bot = commands.Bot(command_prefix=PREFIX, intents=INTENTS)

client = discord.Client()

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')

@bot.command()
async def cantoche(ctx):
    res = CantocheBotPDF.DownloadPDF()
    if (res == 0):
        CantocheBotPDF.generatePNG()
        CantocheBotPDF.getPartPNG()
        with open('MenuDuJour.png', 'rb') as f:
            picture = discord.File(f)
            await ctx.send("Voici le menu du jour: ", file = picture)
    else:
        await ctx.send("Nous sommes le week-end, vous êtes libre de manger ce que vous voulez")
bot.run(TOKEN)
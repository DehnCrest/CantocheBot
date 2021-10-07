import discord
import datetime
from discord.ext.commands.bot import Bot
import CantocheBotPDF
from discord.ext import commands

with open('BotToken.txt', 'r') as f:
    TOKEN = f.readline()
    f.close()

PREFIX = '!'
INTENTS = discord.Intents.default()
bot = commands.Bot(command_prefix=PREFIX, intents=INTENTS, case_insensitive=True) #case_insensitive to fix caps issue

# Dictionnary to manage weekday parameter
days = { 'lundi':0, 'mardi':1, 'mercredi':2, 'jeudi':3, 'vendredi':4, 'samedi':5, 'dimanche':6 }

client = discord.Client()

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')

@bot.command()
async def cantoche(ctx, day: str=None):
    if (day is None):
        day = datetime.datetime.today().weekday()
    else:
        day = day.lower()
        if(day in days.keys()):
            day = days[day]
        elif day == 'semaine':
            CantocheBotPDF.DownloadPDF()
            CantocheBotPDF.generatePNG()
            with open('Menu_Semaine.png', 'rb') as f:
                picture = discord.File(f)
                await ctx.send("Voici le menu de la semaine: ", file = picture)
        else:
            await ctx.send("Votre jour n'a pas été compris, merci de réessayer")    

    if(day in [5,6]):
        await ctx.send("Les jours de week-end, vous êtes libre de manger des oeufs")
    else:
        CantocheBotPDF.DownloadPDF()
        CantocheBotPDF.generatePNG()
        CantocheBotPDF.getPartPNG(day)
        with open('MenuDuJour.png', 'rb') as f:
            picture = discord.File(f)
            await ctx.send("Voici le menu du jour: ", file = picture)

bot.run(TOKEN)
# BY ADU - 23/11/21
# 
# Licence : CC-BY-NC-SA

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
language = ""
versionmsg = "Bot: CantocheBot - Version 1.0.2\nPython version: 3.10\nOS: Debian 10 Buster (AMD64)"


# Dictionnary to manage weekday parameter
daysfr = { 'lundi':0, 'mardi':1, 'mercredi':2, 'jeudi':3, 'vendredi':4 }
daysen = { 'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4 }

client = discord.Client()

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')

@bot.command()
async def cantoche(ctx, day: str=None):
    if (day is None):
        day = datetime.datetime.today().weekday()
        CantocheBotPDF.DownloadPDF()
        CantocheBotPDF.generatePNG()
        CantocheBotPDF.getPartPNG(day)
        with open('MenuDuJour.png', 'rb') as f:
            picture = discord.File(f)
            await ctx.send("Voici le menu du jour : ", file = picture)
            return
    else:
        day = day.lower()
        if(day == 'version'):
            await ctx.send(versionmsg)
            return
        if(day == 'demain'):
            if(datetime.datetime.today().weekday() == 6):
                day = 'lundi'
            elif(datetime.datetime.today().weekday() == 5):
                day = 'dimanche'
            elif(datetime.datetime.today().weekday() == 4):
                day = 'samedi'
            else:
                day = list(daysfr.keys())[list(daysfr.values()).index(datetime.datetime.today().weekday() + 1)]
        elif(day == 'tomorrow'):
            if(datetime.datetime.today().weekday() == 6):
                day = 'monday'
            elif(datetime.datetime.today().weekday() == 5):
                day = 'sunday'
            elif(datetime.datetime.today().weekday() == 4):
                day = 'saturday'
            else:
                day = list(daysen.keys())[list(daysen.values()).index(datetime.datetime.today().weekday() + 1)]
        if(day in ['samedi', 'dimanche']):
            await ctx.send("Les jours de week-end, vous êtes libre de manger des oeufs")
            return
        elif(day in ['saturday', 'sunday']):
            await ctx.send("On week-end days, you are free to eat eggs")
            return
        if(day in daysfr.keys() or day in daysen.keys()):
            if (day in ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi']):
                language = "fr"
                daymsg = day
                day = daysfr[day]
            elif (day in ['monday','tuesday','wednesday','thursday','friday']):
                language = "en"
                daymsg = day
                day = daysen[day]
            CantocheBotPDF.DownloadPDF()
            CantocheBotPDF.generatePNG()
            CantocheBotPDF.getPartPNG(day)
            with open('MenuDuJour.png', 'rb') as f:
                picture = discord.File(f)
                if(language == "fr"):
                    await ctx.send("Voici le menu du " + daymsg + ":", file = picture)
                    return
                elif(language == "en"):
                    await ctx.send("Here's the menu of " + daymsg + ":", file = picture)
                    return
        elif day == 'semaine' or day == 'week':
            CantocheBotPDF.DownloadPDF()
            CantocheBotPDF.generatePNG()
            with open('Menu_Semaine.png', 'rb') as f:
                picture = discord.File(f)
                # If the parameter is "week" or "semaine"
                if (day == "semaine"):
                    await ctx.send("Voici le menu de la semaine: ", file = picture)
                    return
                elif (day == "week"):
                    await ctx.send("Here's the menu of the week: ", file = picture)
                    return
        else:
            await ctx.send(":flag_fr: Votre jour n'a pas été compris, merci de réessayer\n:flag_gb: Your day hasn't been understood, please retry") # This should never be printed, but just in case
            return
        

bot.run(TOKEN)

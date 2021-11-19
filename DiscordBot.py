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

# Dictionnary to manage weekday parameter
days = { 'lundi':0, 'mardi':1, 'mercredi':2, 'jeudi':3, 'vendredi':4,
         'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4,
         'test':5
}

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
            await ctx.send("Voici le menu du jour: ", file = picture)
            return
    else:
        day = day.lower()
        if(day in ['samedi', 'dimanche']):
            await ctx.send("Les jours de week-end, vous êtes libre de manger des oeufs")
            return
        elif(day in ['saturday', 'sunday']):
            await ctx.send("On week-end days, you are free to eat eggs")
            return
        if(day in days.keys()):
            if (day in ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi']): language = "fr"
            elif (day in ['monday','tuesday','wednesday','thursday','friday']): language = "en"
            daymsg = day
            egg = 0
            day = days[day]
            CantocheBotPDF.DownloadPDF()
            pages = CantocheBotPDF.getEggs()
            pages.lower()
            CantocheBotPDF.generatePNG()
            CantocheBotPDF.getPartPNG(day)
            with open('MenuDuJour.png', 'rb') as f:
                picture = discord.File(f)
                if(pages.find('oeuf') != -1 or pages.find('œuf') != -1):
                    egg = 1
                if(language == "fr"):
                    if(egg == 1):
                        await ctx.send("Cette semaine il y aura des oeufs !\n J'adore les oeufs !!\n Voici le menu du " + daymsg + ":", file = picture)
                    else:
                        await ctx.send("Voici le menu du " + daymsg + ":", file = picture)
                    return
                elif(language == "en"):
                    if(egg == 1):
                        await ctx.send("This week you'll have eggs !\n I love eggs !!!! !!\n Here's the menu of " + daymsg + ":", file = picture)
                    else:
                        await ctx.send("Here's the menu of " + daymsg + ":", file = picture)
                    return
        elif day == 'semaine' or day == 'week':
            CantocheBotPDF.DownloadPDF()
            CantocheBotPDF.generatePNG()
            pages = CantocheBotPDF.getEggs()
            pages.lower()
            if(pages.find('oeuf') != -1 or pages.find('œuf') != -1):
                egg = 1
            with open('Menu_Semaine.png', 'rb') as f:
                picture = discord.File(f)
                if (day == "semaine"):
                    if(egg == 1):
                        await ctx.send("Il y a des oeufs cette semaine !\n Voici le menu de la semaine: ", file = picture)
                    else:
                        await ctx.send("Voici le menu de la semaine: ", file = picture)
                    return
                elif (day == "week"):
                    if(egg == 1):
                        await ctx.send("There's eggs this week !\n Here's the menu of the week: ", file = picture)
                    else:
                        await ctx.send("Here's the menu of the week: ", file = picture)
                    return
        else:
            await ctx.send("Votre jour n'a pas été compris, merci de réessayer") 
            return
        

bot.run(TOKEN)

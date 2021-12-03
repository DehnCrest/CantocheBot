# LAST UPDATED AKOE - 29/11/21
# ADU - Daily counter 03/12/21
# Licence : CC-BY-NC-SA

import discord
import datetime
from discord.ext.commands.bot import Bot
import CantocheBotPDF
from discord.ext import commands
import random
import os.path

with open('BotToken.txt', 'r') as f:
    TOKEN = f.readline()
    f.close()

PREFIX = '!'
INTENTS = discord.Intents.default()
bot = commands.Bot(command_prefix=PREFIX, intents=INTENTS, case_insensitive=True) #case_insensitive to fix caps issue

# Is printed when !cantoche help is called
helpmsg = "Aide pour la version française :\
```\
!cantoche ou !ct [jour]     -> Affiche le menu du jour spécifié \n\
!cantoche ou !ct            -> Affiche le menu du jour actuel\n\
!cantoche ou !ct demain     -> Affiche le menu du lendemain\n\
!cantoche ou !ct semaine    -> Affiche le menu de la semaine```\n\
Help for the english version :\
```\
!cantoche or !ct [day]     -> Print the specified day's menu \n\
!cantoche or !ct           -> Print the actual day's menu\n\
!cantoche or !ct tomorrow  -> Print next day's menu\n\
!cantoche or !ct week      -> Print the menu of the week```"

# Is printed when !cantoche version is called
versionmsg = "Bot: CantocheBot - Version 1.5 Beta\nPython version: 3.10\nOS: Debian 10 Buster (amd64)"

# Dictionnaries to manage weekday parameter
daysfr = { 'lundi':0, 'mardi':1, 'mercredi':2, 'jeudi':3, 'vendredi':4, 'samedi':5, 'dimanche':6 }
daysen = { 'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5, 'sunday':6 }
daysentofr = { 'monday':'lundi', 'tuesday':'mardi', 'wednesday':'mercredi', 'thursday':'jeudi', 'friday':'vendredi', 'saturday':'samedi', 'sunday':'dimanche' }

# Dictionnary of food emojis
emoji = { 
    0:':hotdog:', 
    1:':hamburger:', 
    2:':fries:', 
    3:':pizza:', 
    4:':stuffed_pita:', 
    5:':egg:', 
    6:':cooking:',
    7:':ramen:',
    8:':taco:',
    9:':carrot:',
    10:':poultry_leg:',
    11:':sushi:',
    12:':burrito:',
    13:':cake:',
    14:':doughnut:',
    15:':cookie:'
    }

client = discord.Client()

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')

@bot.command(aliases=['ct'])
async def cantoche(ctx, day: str=None):

    # Read the daily counter
    f = open('dailycount.txt', 'r')
    cntr = f.readlines()
    f.close

    # Picks a random emoji between 0 and 15
    randomemoji = random.randint(0, 15)

    # Defines today's int
    todayint = datetime.datetime.today().weekday()
    
    # Generates all files if PDF isn't in folder
    if(not (os.path.isfile('./Menu_Semaine.pdf'))):
        CantocheBotPDF.generateAllFiles()
        await ctx.send(":flag_fr: Les fichiers n'étaient pas présent, ils viennent d'être téléchargés \n:flag_gb: Files weren't present, they have been dowloaded")
    # Compare the PDF week with the current week int, if it differs, downloads the new PDF
    else:
        pdfweeknbr = CantocheBotPDF.getWeek()
        if(pdfweeknbr != int(datetime.datetime.now().strftime("%W"))):
            CantocheBotPDF.generateAllFiles()
            if(pdfweeknbr != int(datetime.datetime.now().strftime("%W"))):
                await ctx.send(":flag_fr: Menu retéléchargé, mais il s'agit toujours du menu de la semaine dernière :x:\n:flag_gb: Menu redownoaded, but it's still the previous week's menu :x:")
                return
            else:
                await ctx.send(":flag_fr: Menu retéléchargé, il s'agit de celui de cette semaine :white_check_mark:\n:flag_gb: Menu redownloaded, it's this week's menu :white_check_mark:")

    # This is checking if the parameter is given or not
    if (day is None):
        day = todayint
        # If the command is run a saturday or a sunday, without parameter
        if(day in [5,6]):
            await ctx.send(":flag_fr: Les jours de week-end, vous êtes libre de manger des oeufs :egg: \n:flag_gb: On week-end days, you are free to eat eggs :egg:")
            return
        # If the command is run on any other day, without parameter
        else:
            day = list(daysfr.keys())[list(daysfr.values()).index(day)]
            with open(f'MenuDu{day}.png', 'rb') as f:
                picture = discord.File(f)
                await ctx.send(f":flag_fr: Voici le menu du jour {emoji[randomemoji]} :\n:flag_gb: Here's the menu of the day {emoji[randomemoji]} :", file = picture)
                return
    else:
        day = day.lower()
        match day:
            # Can be used if the bot is locked on an old version, when the new is available on the server (shouldn't arrive)
            case 'forcedownload':
                CantocheBotPDF.generateAllFiles()
                await ctx.send(f":flag_fr: Tous les fichiers ont été téléchargés\n:flag_gb: All files have been downloaded")
                return
            # If the paraleter is help or aide, prints a useful guide for the bot
            case 'help' | 'aide':
                await ctx.send(helpmsg)
                return
            # If the parameter is 'version', send information about the bot
            case 'version':
                await ctx.send(versionmsg)
                return
            # If the parameter is 'stats', send daily stats
            case 'stats':
                await ctx.send(f"Le bot a été utilisé : {cntr} fois aujourd'hui.")
                # Open and close the file : it clears it (read mode)
                open("dailycount.txt", "w").close()
                # Increment the value
                f = open('dailycount.txt', 'w')
                print(cntr =+ 1, file=f)
                f.close()
                return
            # If the parameter is 'demain', get the day name of today + 1
            case 'demain':
                match todayint:
                    # If we are sunday, set the day to monday
                    case 6:
                        await ctx.send("Nous sommes dimanche, le menu n'est pas à jour pour que je puisse vous proposer le menu de demain")
                        return
                    # On any other day, get day name of today + 1
                    case _:
                        day = list(daysfr.keys())[list(daysfr.values()).index(todayint + 1)]
            # Same as above, for the english version
            case 'tomorrow':
                match todayint:
                    # If we are sunday, set the day to monday
                    case 6:
                        await ctx.send("It's sunday, the menu isn't up to date to propose tomorrow's menu")
                        return
                    # On any other day, get day name of today + 1
                    case _:
                        day = list(daysen.keys())[list(daysen.values()).index(todayint + 1)]
        match day:
            # This is the check for the french parameter
            case 'lundi' | 'mardi' | 'mercredi' | 'jeudi' | 'vendredi' | 'samedi' | 'dimanche' | 'semaine':
                match day:                  
                    # If the parameter is 'samedi' or 'dimanche', no menu as it's the weekend
                    case 'samedi' | 'dimanche':
                        await ctx.send("Les jours de week-end, vous êtes libre de manger des oeufs :egg:")
                        return
                    # If parameter is 'semaine', send the full menu of the week
                    case 'semaine':
                        with open('Menu_Semaine.png', 'rb') as f:
                            picture = discord.File(f)
                            await ctx.send(f"Voici le menu de la semaine {emoji[randomemoji]} : ", file = picture)
                            return                   
                    # On any other day, get the menu of the specific day
                    case _:
                        daymsg = day
                        day = daysfr[day]
                        with open(f'MenuDu{daymsg}.png', 'rb') as f:
                            picture = discord.File(f)
                            await ctx.send(f"Voici le menu du {daymsg} {emoji[randomemoji]}:", file = picture)
                            return
            # This is the check for the english parameter
            case 'monday' | 'tuesday' | 'wednesday' | 'thursday' | 'friday' | 'saturday' | 'sunday' | 'week':
                match day:                    
                    # If the parameter is 'saturday' or 'sunday', no menu as it's the weekend
                    case 'saturday' | 'sunday':
                        await ctx.send("On week-end days, you are free to eat eggs :egg:")
                        return
                    # If parameter is 'week', send the full menu of the week
                    case 'week':
                        with open('Menu_Semaine.png', 'rb') as f:
                            picture = discord.File(f)
                            await ctx.send(f"Here's the menu of the week {emoji[randomemoji]} :", file = picture)
                            return
                    # On any other day, get the menu of the specific day
                    case _:
                        daymsg = day
                        day = daysen[day]
                        with open(f'MenuDu{daysentofr[daymsg]}.png', 'rb') as f:
                            picture = discord.File(f)
                            await ctx.send(f"Here's the menu of {daymsg} {emoji[randomemoji]} :", file = picture)
                            return
            # In case where the parameter isn't recognized, print a message
            case _:
                await ctx.send(":flag_fr: Votre jour n'a pas été compris, merci de réessayer\n:flag_gb: Your day hasn't been understood, please retry")
                return

bot.run(TOKEN)
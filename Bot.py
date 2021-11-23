#!/usr/bin/python3

#Imports
import datetime
import discord
import Utils
from discord import guild
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option


#Create context for the bot
client = commands.Bot(command_prefix="!")
slash = SlashCommand(client, sync_commands=True)

#Read the token to start the bot
with open('BotToken.txt', 'r') as f:
    TOKEN = f.readline()
    f.close()

#Dict to transform the int of the day, into a string
daystr = {
    #French
    "lundi":0,
    "mardi":1,
    "mercredi":2,
    "jeudi":3,
    "vendredi":4,
    "semaine":7,

    # English
    "monday":10,
    "tuesday":11,
    "wednesday":12,
    "thursday":13,
    "friday":14,
    "week":17
}

guildlist = []

#Print quick debug when the bot starts
@client.event
async def on_ready():
    print(f'Logged in as: "{client.user.name}" with ID "{client.user.id}"')
    for guildname in client.guilds:
        guildlist.append(guildname.id)
        print(f'Bot on guild "{guildname}" with guildID "{guildname.id}"')
    print(f'Guilds: {guildlist}')

#Cantoche command parameters
@slash.slash(
    name="cantoche",
    description="Command to get the menu of the cantoche",
    guild_ids=guildlist,
    options=[
        create_option(
            name="day",
            description="Select your day",
            required="False",
            option_type=3,
            choices=[
                create_choice(
                    name="Lundi",
                    value="lundi"
                ),
                create_choice(
                    name="Mardi",
                    value="mardi"
                ),
                create_choice(
                    name="Mercredi",
                    value="mercredi"
                ),
                create_choice(
                    name="Jeudi",
                    value="jeudi"
                ),
                create_choice(
                    name="Vendredi",
                    value="vendredi"
                ),
                create_choice(
                    name="Semaine",
                    value="semaine"
                ),
                create_choice(
                    name="Monday",
                    value="monday"
                ),
                create_choice(
                    name="Tuesday",
                    value="tuesday"
                ),
                create_choice(
                    name="Wednesday",
                    value="wednesday"
                ),
                create_choice(
                    name="Thursday",
                    value="thursday"
                ),
                create_choice(
                    name="Friday",
                    value="friday"
                ),
                create_choice(
                    name="Week",
                    value="week"
                ),
            ]
        )
    ]
)
async def _cantoche(ctx:SlashContext, day:str=None):
    if(day is None):
        day = datetime.datetime.today().weekday()
        daymsg = list(daystr.keys())[list(daystr.values()).index(day)]
    else:
        daymsg = day
        day = daystr[day]
    eggs = Utils.checkEggs() # Downloads the PDF and checks if "oeuf" is a word in the menu
    if(day in [0,1,2,3,4]): # Checks for french version of weekday
        Utils.generatePNG()
        Utils.getPartPNG(day)
        with open('MenuDuJour.png', 'rb') as f:
            picture = discord.File(f)
            if(eggs): # If the word "oeuf" was found in the PDF file
                await ctx.send(f'Cette semaine il y aura des oeufs !\nJ\'adore les oeufs !!\nVoici le menu du {daymsg} :', file = picture)
            else:
                await ctx.send(f'Voici le menu du {daymsg} :', file = picture)
            return
    elif(day in [10,11,12,13,14]): # Checks for english version of weekday
        Utils.generatePNG()
        Utils.getPartPNG(day-10)
        with open('MenuDuJour.png', 'rb') as f:
            picture = discord.File(f)
            if(eggs): # If the word "oeuf" was found in the PDF file
                await ctx.send(f'There will be eggs this week !\nI love eggs !!\nHere\'s the menu of {daymsg} :', file = picture)
            else:
                await ctx.send(f'Here\'s the menu of {daymsg} :', file = picture)
            return
    elif(day in [5,6]): # If /cantoche is run during the week-end
        await ctx.send("Les jours de week-end, vous êtes libre de manger des oeufs")
        return
    elif(day == 7): # If the parameter is "semaine"
        Utils.generatePNG()
        with open('Menu_Semaine.png', 'rb') as f:
            picture = discord.File(f)
            if(eggs): # If the word "oeuf" was found in the PDF file
                await ctx.send("Il y a des oeufs cette semaine !\nVoici le menu de la semaine: ", file = picture)
            else:
                await ctx.send("Voici le menu de la semaine: ", file = picture)
            return
    elif(day==17): # If the parameter is "week"
        Utils.generatePNG()
        with open('Menu_Semaine.png', 'rb') as f:
            picture = discord.File(f)
            if(eggs): # If the word "oeuf" was found in the PDF file
                await ctx.send("There's eggs this week !\nHere's the menu of the week: ", file = picture)
            else:
                await ctx.send("Here's the menu of the week: ", file = picture)
            return
    else:
        await ctx.send("Le jour spécifié n'a pas été compris, veuillez réessayer") # This should never be printed, but just in case

client.run(TOKEN)
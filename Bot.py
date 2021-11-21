#!/usr/bin/python

import datetime
import discord
import Utils
from discord import guild
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option


client = commands.Bot(command_prefix="!")
slash = SlashCommand(client, sync_commands=True)

with open('BotToken.txt', 'r') as f:
    TOKEN = f.readline()
    f.close()

daystr = {
    0:"lundi",
    1:"mardi",
    2:"mercredi",
    3:"jeudi",
    4:"vendredi"
}

guildlist = []

@client.event
async def on_ready():
    print(f'Logged in as: "{client.user.name}" with ID "{client.user.id}"')
    for guildname in client.guilds:
        guildlist.append(guildname.id)
        print(f'Bot on guild "{guildname}" with guildID "{guildname.id}"')
    print(f'Guilds: {guildlist}')

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
                    value="0"
                ),
                create_choice(
                    name="Mardi",
                    value="1"
                ),
                create_choice(
                    name="Mercredi",
                    value="2"
                ),
                create_choice(
                    name="Jeudi",
                    value="3"
                ),
                create_choice(
                    name="Vendredi",
                    value="4"
                ),
                create_choice(
                    name="Semaine",
                    value="7"
                ),
            ]
        )
    ]
)
async def _cantoche(ctx:SlashContext, day:str=None):
    if(day is None):
        day = datetime.datetime.today().weekday()
    day = int(day)
    eggs = Utils.checkEggs()
    if(day in [0,1,2,3,4]):
        Utils.generatePNG()
        Utils.getPartPNG(day)
        with open('MenuDuJour.png', 'rb') as f:
            picture = discord.File(f)
            if(eggs):
                await ctx.send("Cette semaine il y aura des oeufs !\nJ'adore les oeufs !!\nVoici le menu du " + daystr[day] + ":", file = picture)
            else:
                await ctx.send("Voici le menu du " + daystr[day] + ":", file = picture)
            return
    elif(day in [5,6]):
        await ctx.send("Les jours de week-end, vous êtes libre de manger des oeufs")
        return
    elif(day == 7):
        Utils.generatePNG()
        with open('Menu_Semaine.png', 'rb') as f:
            picture = discord.File(f)
            if(eggs):
                await ctx.send("Il y a des oeufs cette semaine !\nVoici le menu de la semaine: ", file = picture)
            else:
                await ctx.send("Voici le menu de la semaine: ", file = picture)
            return
    else:
        await ctx.send("Le jour spécifié n'a pas été compris, veuillez réessayer")

client.run(TOKEN)
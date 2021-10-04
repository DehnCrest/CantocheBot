#!/usr/bin/python
#

# Lundi: (150, 1100, 8000, 2000)
# Mardi: (150, 2000, 8000, 2750)
# Mercredi: (150, 2750, 8000, 3550)
# Jeudi: (150, 3550, 8000, 4350)
# Vendredi: (150, 4350, 8000, 5150)

import datetime
from pdf2image import convert_from_path
from PIL import Image
import urllib.request

def DownloadPDF():
    url = 'https://webdfd.mines-ales.fr/restau/Menu_Semaine.pdf'
    urllib.request.urlretrieve(url, "Menu_Semaine.pdf")

# Transforme le fichier PDF en fichier PNG pour le traiter plus facilement
def generatePNG():
    pages = convert_from_path('Menu_Semaine.pdf', 500)
    pages[0].save('Menu_Semaine.png', 'PNG')

# Récupère l'image du menu du jour
def getPartPNG():
    im = Image.open("Menu_Semaine.png")
    today = datetime.datetime.today().weekday()
    rectdict = {
        0:(150, 1100, 8000, 2000),
        1:(150, 2000, 8000, 2750),
        2:(150, 2750, 8000, 3550),
        3:(150, 3550, 8000, 4350),
        4:(150, 4350, 8000, 5150)
    }
    crop_rectangle = rectdict[today]
    cropped_im = im.crop(crop_rectangle)
    cropped_im.save('MenuDuJour.png', 'PNG')

#DownloadPDF()
#generatePNG()
#getPartPNG()
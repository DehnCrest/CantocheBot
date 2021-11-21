#!/usr/bin/python

# Lundi (50, 350, 2450, 600),
# Mardi(50, 600, 2450, 825),
# Mercredi(50, 825, 2450, 1075),
# Jeudi (50, 1075, 2450, 1300),
# Vendredi (50, 1300, 2450, 1550)

import datetime
from pdf2image import convert_from_path
from PIL import Image
import urllib.request
import pdfplumber

# Télécharge le fichier situé sur le serveur des mines
def downloadPDF():
    url = 'https://webdfd.mines-ales.fr/restau/Menu_Semaine.pdf'
    urllib.request.urlretrieve(url, "Menu_Semaine.pdf")

def checkEggs():
    downloadPDF()
    with pdfplumber.open('Menu_Semaine.pdf') as pdf:
        pages = pdf.pages
        page = pages[0].extract_text().lower()
        if(page.find('oeuf') != -1 or page.find('œuf') != -1):
            return True
        else:
            return False


# Transforme le fichier PDF en fichier PNG pour le traiter plus facilement
def generatePNG():
    pages = convert_from_path('Menu_Semaine.pdf', dpi=150)
    pages[0].save('Menu_Semaine.png', 'PNG')

# Récupère l'image du menu du jour
def getPartPNG(day):
    im = Image.open("Menu_Semaine.png")
    rectdict = {
        0:(50, 350, 2450, 600),
        1:(50, 600, 2450, 825),
        2:(50, 825, 2450, 1075),
        3:(50, 1075, 2450, 1300),
        4:(50, 1300, 2450, 1550)
    }
    crop_rectangle = rectdict[day]
    cropped_im = im.crop(crop_rectangle)
    cropped_im.save('MenuDuJour.png', 'PNG')
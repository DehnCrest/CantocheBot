# BY ADU - 23/11/21
# AKOE - dl_optimization
# Licence : CC-BY-NC-SA

#!/usr/bin/python
#

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

days = {
    0:'Lundi',
    1:'Mardi',
    2:'Mercredi',
    3:'Jeudi',
    4:'Vendredi'
}

monthfrtoen = {
    'janvier':'january',
    'fevrier':'february',
    'mars':'march',
    'avril':'april',
    'mai':'may',
    'juin':'june',
    'juillet':'july',
    'aout':'august',
    'septembre':'september',
    'octobre':'october',
    'novembre':'november',
    'decembre':'december'
}

# Downloads the PDF on IMT's web server
def DownloadPDF():
    url = 'https://webdfd.mines-ales.fr/restau/Menu_Semaine.pdf'
    urllib.request.urlretrieve(url, "Menu_Semaine.pdf")

# Transforms the PDF into PNG
def generatePNG():
    pages = convert_from_path('Menu_Semaine.pdf', dpi=150)
    pages[0].save('Menu_Semaine.png', 'PNG')

# Get today's part menu
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
    cropped_im.save(f'MenuDu{days[day]}.png', 'PNG')

def generateAllFiles():
    DownloadPDF()
    generatePNG()
    getPartPNG(0)
    getPartPNG(1)
    getPartPNG(2)
    getPartPNG(3)
    getPartPNG(4)

def getWeek():
    with pdfplumber.open('Menu_Semaine.pdf') as pdf:
        page = pdf.pages[0].extract_text().lower()
        page = page.split('\n')[1].split()
        mth = datetime.datetime.strptime(monthfrtoen[page[2]], "%B")
        month_number = mth.month
        return int(datetime.date(int(page[7]),month_number,int(page[1])).isocalendar().week)
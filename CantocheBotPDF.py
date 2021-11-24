# BY ADU - 23/11/21
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
    cropped_im.save('MenuDuJour.png', 'PNG')
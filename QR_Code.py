# Script permettant de télécharger une image de QR Code, de la corriger puis de renvoyer la clé contenue dedans par le formulaire HTML de la page.
# La correction consiste simplement à ajouter les trois carrés qu'il y a sur les bords de chaque QR Code.
# Il suffit de regarder un autre exemple de QR Code pour remarquer la différence.
# Les pixels se mesurent facilement avec GIMP ou Photoshop.


import cv2, requests, base64, pyzbar.pyzbar
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw

URL = "http://challenge01.root-me.org/programmation/ch7/"
session = requests.Session()
path = "./image_decodee_3.png"
path_image_correcte = "./image_correcte.png"


##########################################################
# TÉLÉCHARGEMENT ET DÉCODAGE
##########################################################

# Ce bloc télécharge la page HTML du challenge, récupère les données encodées en Base64 qu'il y a dans la balise <img>, décode ces données, puis les sauvegarde dans un fichier local.
# Faire gaffe à bien être connecté sur le site pour pouvoir télécharger l'image sous peine de systématiquement recevoir un fichier vide !

page_html = session.get(URL).text
img_tag = BeautifulSoup(page_html, "html.parser").find("img")
image_base64 = str(img_tag).replace('<img src=\"data:image/png;base64,', "").replace('\"/>',"") # On isole les données

fichier_png = open(path, "wb") # 'wb' = 'write' + 'binary'
fichier_png.write(base64.b64decode(image_base64))
fichier_png.close()


##########################################################
# CORRECTION DE L'IMAGE
##########################################################

# Ce bloc corrige le QR Code fourni pour le challenge.
# On dessine un grand carré noir, puis un sous-carré blanc (n-1, n-1) puis un sous-sous-carré noir (n-2, n-2).
# On répète cette procédure trois fois puisqu'il y a trois bords à remplir.
# Chaque unité du QR Code fait 9x9 pixels.
# Les grands carrés à ajouter mesurent 7 unités (63 * 63).
# Le sous-carré blanc démarre 1 unité après le bord du grand carré noir.
# Le sous-sous-carré noir démarre 2 unités après le bord du grand carré noir.


with Image.open(path) as image:

    draw = ImageDraw.Draw(image)

    carre_1 = (18, 18)      # Coordonnées déduites sur GIMP avec l'outil de mesure
    carre_2 = (18, 216)     # Coordonnées déduites sur GIMP avec l'outil de mesure
    carre_3 = (216, 18)     # Coordonnées déduites sur GIMP avec l'outil de mesure

    NOIR = (0,0,0)
    BLANC = (255,255,255)

    # 1
    draw.rectangle([carre_1,(carre_1[0]+63,carre_1[1]+63)], fill = NOIR)
    draw.rectangle([(carre_1[0]+9,carre_1[1]+9),(carre_1[0]+54,carre_1[1]+54)], fill = BLANC)
    draw.rectangle([(carre_1[0]+18,carre_1[1]+18),(carre_1[0]+45,carre_1[1]+45)], fill = NOIR)
    # 2
    draw.rectangle([carre_2,(carre_2[0]+63,carre_2[1]+63)], fill = NOIR)
    draw.rectangle([(carre_2[0]+9,carre_2[1]+9),(carre_2[0]+54,carre_2[1]+54)], fill = BLANC)
    draw.rectangle([(carre_2[0]+18,carre_2[1]+18),(carre_2[0]+45,carre_2[1]+45)], fill = NOIR)
    # 3
    draw.rectangle([carre_3,(carre_3[0]+63,carre_3[1]+63)], fill = NOIR)
    draw.rectangle([(carre_3[0]+9,carre_3[1]+9),(carre_3[0]+54,carre_3[1]+54)], fill = BLANC)
    draw.rectangle([(carre_3[0]+18,carre_3[1]+18),(carre_3[0]+45,carre_3[1]+45)], fill = NOIR)

    image.save(path_image_correcte, format="PNG")


##########################################################
# EXTRACTION DU QR CODE ET ENVOI DE LA CLÉ
##########################################################

image = cv2.imread(path_image_correcte)
resultat = pyzbar.pyzbar.decode(image) # Ligne qui lit le QR Code et en retourne la valeur
key = str(resultat[0].data).strip("b'The key is ").strip("\'") # On isole la clé

reponse_flag = session.post(URL, data={'metu': key}) # "metu" est le nom du formulaire HTML
print(reponse_flag)
print(reponse_flag.content)


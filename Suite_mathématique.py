# Script permettant de récupérer une suite mathématique sur une page web, de la résoudre rapidement puis de renvoyer le résultat.
# Il faut parfois le relancer, la hauteur du terme à retrouver est aléatoire, change à chaque rechargement et peut monter assez haut.
# Quand ce terme est trop haut, on dépasse un peu la limite de temps du challenge et on se prend un timeout.

import requests
from bs4 import BeautifulSoup

session = requests.Session()
url_flag = "XXX.php?result="

page_html = session.get("XXX.php").text
body = BeautifulSoup(page_html, "html.parser").find("body")

#############################################################
# BOUCLES UTILISÉES AU PRÉALABLE POUR CARTOGRAPHIER LE HTML #
#############################################################
"""
tags = BeautifulSoup(page_html, "html.parser").find_all()
for tag in tags:
    print(tag)
"""

"""
for i in range(len(body)):
    print("CONTENT NUMÉRO " + str(i) + " : ")
    print(body.contents[i])
"""
#########################################

U0 = str(body.contents[10]).strip('= ')
branche_gauche = str(body.contents[4])
branche_droite = str(body.contents[6])
N = str(body.contents[13]).strip("<sub>").strip("</sub>")

branche_gauche_pure = branche_gauche.replace("[ ","").replace(" ]", "").replace("= ", "")
branche_droite_pure = branche_droite.replace("[ ","").replace(" ]", "")

Un = U0
for i in range (int(N)):
    Un = (branche_gauche_pure.replace("U", str(Un)) + branche_droite_pure.replace("n", str(i))).replace("\n","")
    Un = int(eval(Un)) # Résultat final de la suite

    # Faire gaffe à la fonction 'eval()' !
    # Elle est pratique pour convertir du texte en opérateurs et en nombres rapidement mais elle est très dangereuse.
    # Éviter de l'utiliser dans un projet où on ne contrôle pas les données entrantes.

url_flag += str(Un)

cookie = session.cookies.get_dict() # Le challenge exige un cookie
reponse_flag = session.get(url_flag, data=cookie)
print(reponse_flag.text)



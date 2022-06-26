#!/bin/bash

# Script permettant d'afficher une chaîne sous plusieurs formats utiles
# Créé initialement pour un challenge qui nécessitait de convertir de l'hexadécimal en GSM
# Wireshark ne parvenait pas à afficher correctement le contenu des trames de SMS interceptés

import os, sys

if ((len(sys.argv) != 2) or not (os.path.isfile(sys.argv[1]))):
    print("Fichier introuvable ou invalide." + "\n")
    print("Utilisation : Traducteur.py [Fichier]"+ "\n")
    sys.exit(2)

#############################################################
### Bloc d'épuration des mauvais caractères du fichier
### Au cas où il y ait des espaces ou des retours à la ligne

chaine_propre = ""
with open(sys.argv[1]) as fichier:
    for ligne in fichier:
        for char in ligne:
            if(not(char.isspace())):
                chaine_propre += char

#############################################################

print("Chaine originale : " + chaine_propre + "\n")

#############################################################
# Conversion en binaire
# ".zfill(size)" permet de compléter avec des zéros à gauche jusqu'à atteindre la longueur voulue
# Évite le problème des zéros qui disparaissent au début en cas de premier(s) octet(s) nul(s)

chaine_binaire = bin(int(chaine_propre, 16))[2:] # "[2:]" permet de retirer le "0b"
chaine_binaire_complete = chaine_binaire.zfill(len(chaine_propre * 4))

#############################################################

print("Chaine originale binaire : " + chaine_binaire_complete + "\n")

#############################################################
### Boucle permettant d'inverser octet par octet une chaîne hexadécimale
### Ex : "ABCDEF" donnera "EFCDAB"

chaine_inverse = ""
for i in range(len(chaine_propre), 0 , -2):
    chaine_inverse += chaine_propre[i-2:i]

#############################################################

print("Chaîne inverse : " + chaine_inverse + "\n")

#############################################################
# Conversion en binaire de la chaîne inverse
# Même principe que plus haut

chaine_inverse_binaire = bin(int(chaine_inverse, 16))[2:]
chaine_inverse_binaire_complete = chaine_inverse_binaire.zfill(len(chaine_inverse * 4))

#############################################################

print("Chaîne inverse binaire : " + chaine_inverse_binaire_complete + "\n")

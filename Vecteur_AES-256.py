# Script permettant de retrouver un vecteur d'initialisation perdu (AES-256 CBC)

import base64
from Crypto.Cipher import AES

# Vecteur d'initialisation = Nombre aléatoire utilisé une fois par session en combinaison de la clé de chiffrement pour complexifier le tout
# CBC = Cipher Block Chaining => Le vecteur d'initialisation fait la même taille qu'un bloc
# AES-256 => Blocs de 128 bits

# [Texte clair] = [Vecteur] XOR [Texte déchiffré]
# [Vecteur] = [Texte clair] XOR [Texte déchiffré]

longueur_bloc = 128/8

cipher_text_b64 = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
cipher_text = base64.b64decode(cipher_text_b64)[:(int(longueur_bloc))]

key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
key = base64.b64decode(key)

texte_clair = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
vecteur = (texte_clair[:(int(longueur_bloc))]).encode("utf-8")



print("Texte chiffré : \n", cipher_text, "\n")
print("Texte clair : \n", texte_clair, "\n")
print("Vecteur : \n", vecteur, "\n")
print("Clé :", key, "\n")

aes = AES.new(key, AES.MODE_CBC, vecteur)

print ("Vecteur initial : ", aes.decrypt(cipher_text), "\n")
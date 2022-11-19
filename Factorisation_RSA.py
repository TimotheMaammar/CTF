####################################################################################################
### Script permettant de reconstruire une clé privée RSA à partir d'une clé publique RSA et d'une factorisation connue
#
# Voir : https://fr.wikipedia.org/wiki/Chiffrement_RSA
# Résumé des étapes pour la génération des clés en RSA : 
# 	1) Choisir P et Q, deux nombres premiers distincts
#	2) N = P * Q = Module de chiffrement
#	3) Phi(N) = (P - 1)(Q - 1) = Valeur de l'indicatrice d'Euler au point N
#	4) E = Exposant de chiffrement = Entier naturel, arbitrairement choisi, inférieur à Phi(N) et premier avec Phi(N)
# 	5) D = Exposant de déchiffrement = Inverse modulaire de E pour la multiplication modulo Phi(N) = Nombre tel que E * D ≡ 1 (mod Phi(N))
#
# Clé publique = (E, N)
# Clé privée = (D, N)
####################################################################################################


import base64
import rsa # pip install rsa
from Crypto.PublicKey import RSA # pip install pycryptodome
from Crypto.Util.number import inverse
from factordb.factordb import FactorDB # pip install factordb-pycli


ciphertext_b64 = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
ciphertext = base64.b64decode(ciphertext_b64)

# Clé publique fournie au format PEM (Privacy Enhanced Mail)
public_key_PEM = '''-----BEGIN PUBLIC KEY-----
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
-----END PUBLIC KEY-----'''


# Autre moyen d'extraire les informations de la clé sur Linux : 
# 	=> "openssl rsa -in clé_publique.pem -pubin -text -modulus -noout"

public_key = RSA.importKey(public_key_PEM)
n = public_key.n
e = public_key.e
print("Module de la clé publique : \n N = ", n, "\n") 
print("Exposant de la clé publique : \n E = ", e, "\n") # Exposant public = Chiffre choisi arbitrairement = En général 65537 (0x010001)


# FactorDB est une base de données contenant des factorisations répertoriées
# C'est un peu l'équivalent de CrackStation mais pour les factorisations
# Dans notre cas, le nombre se retrouve aussi dans un article Wikipedia parce qu'il est relativement connu : 
# https://fr.wikipedia.org/wiki/Nombre_RSA#RSA-576

print("Recherche des facteurs sur FactorDB \n")

f = FactorDB(n)
f.connect()

p = f.get_factor_list()[0]
q = f.get_factor_list()[1]
d = inverse(e, ((p - 1) * (q - 1)))

print("Premier facteur : \n P : ", p, "\n")
print("Deuxième facteur : \n Q : ", q, "\n")
print("Inverse modulaire (de E) : \n D : ", d, "\n") 

private_key = RSA.construct((n, e, d, p, q)) # Reconstruction de la clé privée à partir de tous les nombres obtenus


# Bien utiliser la fonction "exportKey()" si on veut afficher ou enregistrer la clé au format PEM
# "print(private_key)" donne simplement une bête description de la clé ("Private RSA key at 0x2A147637290")

print("Clé privée obtenue : \n ", private_key.exportKey(), "\n")


# Utilisation de l'autre module RSA pour le déchiffrement parce que le premier posait problème
# Autre manière de faire sur Linux avec OpenSSL :
# 	=> "openssl rsautl -decrypt -in chiffré.txt -out clair.txt -inkey clé_privée.pem"

private_key = rsa.PrivateKey(n, e, d, p, q)
flag = rsa.decrypt(ciphertext, private_key)
print("Flag : ", flag)
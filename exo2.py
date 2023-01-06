import sys
import math
import random

# TP Métaheuristiques
# Oriol CAMPS PÉREZ
# 21908040

# EXERCICE 2 : Voyageur de commerce (Travelling Salesman Problem TSP)

# CONFIGURATION PAR DEFAUT
MAX_DEPL    = 10
MAX_ESSAIS  = 10

# recupération des données n et villes[]
if(len(sys.argv) < 2):
    print("Usage: python3 "+sys.argv[0]+" <path_to_file>")
    exit(1)
with open(sys.argv[1], "r") as fichier:
    if fichier.readable():
        villes=fichier.readlines()
        n=int(villes[0])
        villes=villes[1:]
        for i in range(0, len(villes)):
            villes[i]=villes[i].split()[1:] # on enlève l'identifiant de la ville
            for j in range(len(villes[i])):
                villes[i][j]=int(villes[i][j])
        print("Nombre de villes: "+str(n))
        print("Villes: "+str(villes))
        print()
        assert(len(villes)==n)

# QUESTION 2.1
def random_sol(n=n): # methode itérative (échange aléatoire)
    sol = [i for i in range(1, n+1)]
    for i in range(0, n):
        j = random.randint(0, n-1)
        sol[i], sol[j] = sol[j], sol[i]
    return sol
initX = random_sol()
print("Solution initiale: "+str(initX))
print()

# QUESTION 2.2
def distance(ville1, ville2):
    return math.sqrt((ville1[0]-ville2[0])**2 + (ville1[1]-ville2[1])**2)

def f(X):
    localisation_initiale = [0, 0]
    # On part jusqu'à la première ville
    dist = distance(localisation_initiale, villes[X[0]-1])
    # On parcourt les villes
    for i in range(0, len(X)-1):
        dist += distance(villes[X[i]-1], villes[X[i+1]-1])
    # On revient à la localisation initiale
    dist += distance(villes[X[-1]-1], localisation_initiale)    
    return dist

# QUESTION 2.3
def meilleur_voisin(X):
    meilleur = X.copy()
    for i in range(0, len(X)-1):
        for j in range(0+i, len(X)-1):
            voisinX = X.copy()
            voisinX[i], voisinX[j+1] = voisinX[j+1], voisinX[i]
            
            if f(voisinX) < f(meilleur):
                meilleur = voisinX
    return meilleur  
            
# QUESTION 2.4 
def steepest_hill_climbing(X, max_depl=MAX_DEPL): # pris de l'exercice 1
    Xp = X.copy()
    nb_depl = 0
    stop = False
    while nb_depl < max_depl and not stop:
        mvX = meilleur_voisin(Xp)
        if f(mvX) < f(Xp):
            Xp = mvX
        else:
            stop = True
        nb_depl += 1
    return Xp, nb_depl

def steepest_hill_climbing_redemarrage(X, max_depl=MAX_DEPL, max_essais=MAX_ESSAIS): # pris de l'exercice 1
    nb_essais = 0
    nb_depl = 0
    Xp = X.copy()
    while nb_essais < max_essais:
        mvX, nb_depl_tmp = steepest_hill_climbing(random_sol(), max_depl)
        nb_depl += nb_depl_tmp
        if f(mvX) < f(Xp):
            Xp = mvX
        nb_essais += 1
    return Xp, nb_depl

# QUESTION 2.5
def trouver_voisins(X): # même algo que dans meilleur_voisin, mais on retourne tous les voisins
    voisins = []
    for i in range(0, len(X)-1):
        for j in range(0+i, len(X)-1):
            voisinX = X.copy()
            voisinX[i], voisinX[j+1] = voisinX[j+1], voisinX[i]
            voisins.append(voisinX)
    return voisins

def trouver_voisins_non_tabous(voisins, tabou): # on retourne les voisins non tabous
    non_tabous = []
    for voisin in voisins:
        if voisin not in tabou:
            non_tabous.append(voisin)
    return non_tabous

def meilleur_voisin_non_tabou(X, voisins_non_tabous): # on retourne le meilleur voisin non tabou
    meilleur = X.copy()
    for voisin in voisins_non_tabous:
        if f(voisin) < f(meilleur):
            meilleur = voisin
    return meilleur

def recherche_tabou(X, taille, max_depl=MAX_DEPL): 
    Xp = X.copy()
    tabou = []
    nb_depl = 0
    stop = False
    meilleurX = Xp
    while nb_depl < max_depl and not stop:
        voisins = trouver_voisins(Xp)
        voisins_non_tabous = trouver_voisins_non_tabous(voisins, tabou)

        if len(voisins_non_tabous) > 0:
            mvX = meilleur_voisin_non_tabou(Xp, voisins_non_tabous)
        else:
            stop = True # plus de voisin non tabou

        tabou.append(Xp)
        if len(tabou) > taille:
            tabou.pop(0)

        if f(mvX) < f(meilleurX):
            meilleurX = mvX # stockage meilleure solution courante
        Xp = mvX
        nb_depl += 1

    return meilleurX, nb_depl


# AFFICHAGE DES RÉSULTATS

shc, nb_depl_shc = steepest_hill_climbing(initX)
print("SHC sans redemarrage:\t"+str(shc)+"\n")
shc_red, nb_depl_shc_red = steepest_hill_climbing_redemarrage(initX)
print("SHC avec redemarrage:\t"+str(shc_red)+"\n")

rech_tabou_small, nb_depl_rech_tabou_small = recherche_tabou(initX, 10)
print("R Tabou (len=10):\t"+str(rech_tabou_small)+"\n")
rech_tabou_big, nb_depl_rech_tabou_big = recherche_tabou(initX, 1000)
print("R Tabou (len=1000):\t"+str(rech_tabou_big)+"\n")

print()
print("Solution initiale\t"+"f(X) = "+str(f(initX)))

print("SHC sans redemarrage\t"+"f(X) = "+str(f(shc))+ "\tNombre de déplacements:\t"+str(nb_depl_shc))
print("SHC avec redemarrage\t"+"f(X) = "+str(f(shc_red))+ "\tNombre de déplacements:\t"+str(nb_depl_shc_red))
# Résultats SHC (avec options par défaut) pour le fichier tsp5.txt
#   sans redémarrage: 2 solutions différentes de f(X)
#       f(X) = 196.12466980422548
#       f(X) = 194.04052963659356
#   avec redémarrage: 1 solution de f(X)
#       f(X) = 194.04052963659356

print("R Tabou (len=10)=\t"+"f(X) = "+str(f(rech_tabou_small))+ "\tNombre de déplacements:\t"+str(nb_depl_rech_tabou_small))
print("R Tabou (len=1000)=\t"+"f(X) = "+str(f(rech_tabou_big))+ "\tNombre de déplacements:\t"+str(nb_depl_rech_tabou_big))
# Résultats Tabou (avec options par défaut) pour le fichier tsp5.txt
#   Résultats similaires à ceux de SHC sans redémarrage (aussi deux resultats)


# Résultats pour le fichier tsp101.txt
#   Les algorithmes SHC et Tabou donnent des résultats similaires
#   et sont très lents (plusieurs minutes au total), notamment le SHC avec 
#   redémarrage. Cependant, ce dernier done des résultats légèrement 
#   meilleurs que les autres:
#       SHC sans redémarrage:   f(X) = 2843.142044372415, 2814.993624582888, 2929.3125267085147, entre autres
#       les autres deux:        f(X) = 2969.9263560655336, 3032.190042327892, 3053.724937533383, entre autres
import sys
import math
import random

# TP Métaheuristiques
# Oriol CAMPS PÉREZ
# 21908040

# EXERCICE 2 : Voyageur de commerce (Travelling Salesman Problem TSP)

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
        assert(len(villes)==n)

# QUESTION 2.1
def sol_init(n=n): # methode itérative (échange aléatoire)
    sol = [i for i in range(1, n+1)]
    for i in range(0, n):
        j = random.randint(0, n-1)
        sol[i], sol[j] = sol[j], sol[i]
    return sol
Xinit = sol_init()
print("Solution initiale: "+str(Xinit))

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
    print(X)
    meilleur = X.copy()
    for i in range(0, len(X)-1):
        for j in range(0+i, len(X)-1):
            voisinX = X.copy()
            voisinX[i], voisinX[j+1] = voisinX[j+1], voisinX[i]
            
            if f(voisinX) < f(meilleur):
                meilleur = voisinX
    return meilleur

        
            

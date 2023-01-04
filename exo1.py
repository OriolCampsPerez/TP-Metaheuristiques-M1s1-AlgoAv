import random
import sys

# TP Métaheuristiques
# Oriol CAMPS PÉREZ
# 21908040

# EXERCICE 1 : Unconstrained Binary Quadratic Problem

# recupération des données Q, n et p
def strList_to_intList(l):
    for i in range(len(l)):
        l[i] = int(l[i])
    return l

def list_to_sqMatrix(list, sqrSize, padding=0):
    r=[]
    i=0
    while i < len(list):
        a=[]
        for j in range(sqrSize):
            if i<len(list):
                a.append(list[i])
            else:
                a.append(padding)
            i+=1
        r.append(a)

    return r

# QUESTION 1.6 (partie séléction du fichier)
if(len(sys.argv) < 2):
    print("Usage: python3 "+sys.argv[0]+" <path_to_file>")
    exit(1)
with open(sys.argv[1], "r") as fichier:
    if fichier.readable():
        n=int(fichier.read(1)) # = "6"
        p=int(fichier.read(2)[1]) # = "62" [1] = "2"
        Q=list_to_sqMatrix(strList_to_intList(fichier.read()[3:].split()), n)

# fonction f(x) de l'enoncé
def f(X, q=Q): # paramètre q ajouté pour pouvoir faire des tests
    r=0
    for i in range(n-1):
        for j in range(n-1):
            r+= q[i][j] * X[i]*X[j]
    return r

# QUESTION 1.1
def random_sol():
    r=[]
    for _ in range(n):
        r.append(random.randint(0, 1))
    return r

randX = random_sol()
#print(randX)

# QUESTION 1.2
res12 = f(randX)
#print(res12)

# verifier avec enoncé
def tests12():
    # basé sur l'example de l'enoncé
    Qmatrix_t12 = [[-17, 10, 10, 10, 0, 20], [10, -18, 10, 10, 10, 20], [10, 10, -29, 10, 20, 20], [10, 10, 10, -19, 10, 10], [0, 10, 20, 10, -17, 10], [20, 20, 20, 10, 10, -28]]
    Qlist_t12 = [-17, 10, 10, 10, 0, 20, 10, -18, 10, 10, 10, 20, 10, 10, -29, 10, 20, 20, 10, 10, 10, -19, 10, 10, 0, 10, 20, 10, -17, 10, 20, 20, 20, 10, 10, -28]
    n_t12 = 6
    X_t12 = [1, 1, 0, 1, 0, 0]
    with open("txt/partition6.txt", "r") as fichier_t12:
        if fichier_t12.readable():
            Qtext_t12=fichier_t12.read()[3:].split()

    assert strList_to_intList(Qtext_t12) == Qlist_t12
    assert list_to_sqMatrix(Qlist_t12, n_t12) == Qmatrix_t12
    assert f(X_t12, list_to_sqMatrix(Qlist_t12, n_t12)) == 6
    return True
tests12()

# QUESTION 1.3
def meilleur_voisin(X):
    meilleur= X.copy()
    for i in range(len(X)):
        voisinX = X.copy()
        voisinX[i] = 1 - voisinX[i]
        if f(voisinX) < f(meilleur): # si meilleur (inférieur), on le garde
            meilleur = voisinX
        elif f(voisinX) == f(meilleur): # si égalité, on choisi aléatoirement
            if random.randint(0, 1) == 1:
                meilleur = voisinX
    return meilleur

# QUESTION 1.4
def steepest_hill_climbing(X, max_depl=1000):
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
    return Xp

# QUESTION 1.5
def steepest_hill_climbing_redemarrage(X, max_depl=1000, max_essais=1000):
    nb_essais = 0
    Xp = X.copy()
    while nb_essais < max_essais:
        mvX = steepest_hill_climbing(random_sol(), max_depl)
        if f(mvX) < f(Xp):
            Xp = mvX
        nb_essais += 1
    return Xp

# QUESTION 1.6 (partie affichage)
print("n = "+str(n))
print("p = "+str(p))
print("Q = "+str(Q)+"\n")
print("X de départ = \t\t\t"+str(randX)+"\t"+"f(X) = "+str(f(randX)))
shc_red= steepest_hill_climbing_redemarrage(randX)
print("SHC avec redemarrage de X = \t"+str(shc_red)+"\t"+"f(X) = "+str(f(shc_red)))

# Résultats: 
#   partition6.txt = -29 
#   graphe12345.txt = 


# REFERENCES
# https://www.freecodecamp.org/espanol/news/python-abre-archivo-como-leer-un-archivo-de-texto-linea-por-linea/
# https://www.pythoncentral.io/cutting-and-slicing-strings-in-python/
# https://www.w3schools.com/python/ref_string_split.asp
# https://www.geeksforgeeks.org/python-random-module/
# https://blog.devgenius.io/5-different-ways-to-copy-list-in-python-9478bc6d8f02
# https://python-para-impacientes.blogspot.com/2014/02/ejecutar-programas-con-argumentos.html
# 

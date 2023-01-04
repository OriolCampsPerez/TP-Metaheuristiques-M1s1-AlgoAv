import random

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

with open("txt/partition6.txt", "r") as fichier:
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
    for i in range(n):
        r.append(random.randint(0, 1))
    return r

randX = random_sol()

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



# REFERENCES
# https://www.freecodecamp.org/espanol/news/python-abre-archivo-como-leer-un-archivo-de-texto-linea-por-linea/
# https://www.pythoncentral.io/cutting-and-slicing-strings-in-python/
# https://www.w3schools.com/python/ref_string_split.asp
# https://www.geeksforgeeks.org/python-random-module/
#

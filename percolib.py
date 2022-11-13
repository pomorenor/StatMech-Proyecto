import numpy as np
import matplotlib.pyplot as plt
from random import *
#from random import random, randrange

### En este archivo pongan las implementaciones que vayan haciendo
### para los clusters y los params que debemos calcular.

def fill_lattice(A,L,M):
    random_nums = [i for i in range(0,L*M)]
    for i in range(0,L):
        for j in range(0,M):
            A[i,j] = choice(random_nums)
            random_nums.remove(A[i,j])
    return A

#RanMtz genera una matriz con tamaño dado, con 0 y 1 y recibe el tamaño
#la probabilidad de que una celda tenga un 1
def RanMtz(p, size):
    M=np.zeros((size[0],size[1]))
    for ii in range(len(M)):
        for jj in range(len(M[0])):
            q=random()
            if q<=p:
                M[ii,jj]=1
    return M

#HK recibe una matriz (en principio de 0 y 1) y devuelve una matriz de
#enteros donde cada cluster está clasificado

def HK(Ma):
    M=np.copy(Ma)
    N=1
    for ii in range(len(M)):
        for jj in range(len(M[0])):
            if M[ii,jj]!=0:
                if ii==0 and jj==0:
                    M[ii,jj]=N
                    N+=1
                elif ii==0:
                    if M[ii,jj-1]!=0:
                        M[ii,jj]=M[ii,jj-1]
                    else:
                        M[ii,jj]=N
                        N+=1
                elif jj==0:
                    if M[ii-1,jj]!=0:
                        M[ii,jj]=M[ii-1,jj]
                    else:
                        M[ii,jj]=N
                        N+=1
                else:
                    if M[ii-1,jj]!=0:
                        M[ii,jj]=M[ii-1,jj]
                    elif M[ii,jj-1]!=0:
                        M[ii,jj]=M[ii,jj-1]
                    else:
                        M[ii,jj]=N
                        N+=1
    for ii in range(len(M)):
        for jj in range(len(M[0])):
            if M[ii,jj-1]!=0 and M[ii,jj]!=0:
                if M[ii,jj-1]!=M[ii,jj] and jj!=0:
                    V=M[ii,jj-1]
                    U=M[ii,jj]
                    for i in range(len(M)):
                        for j in range(len(M[0])):
                            if M[i,j]==V:
                                M[i,j]=U

    return M

#CL recibe una matriz (de 0 y 1 o ya clasificada) y cuenta sus clusters

def CL(Ma):
    M=HK(Ma)
    MM=set(M.flatten())
    N=len(MM)-1
    return N

#Percolador recibe una matriz (de 0 y 1 o ya clasificada) y devuelve
#una matriz con los clusters percolantes
def Percolador(Ma):
    M=HK(Ma)
    M0=set(M[0])
    MF=set(M[len(M)-1])
    percolantes= list(M0 & MF -{0})
    Z=np.zeros((len(M),len(M[0])))

    if len(percolantes)!=0:
        for V in percolantes:
            for ii in range(len(M)):
                for jj in range(len(M[0])):
                    if M[ii,jj]==V:
                        Z[ii,jj]+=M[ii,jj]
    return Z



if __name__ == '__main__':
    M=RanMtz(0.5,size=(100,100))
    fig, ax =plt.subplots(1,3)
    ax[0].imshow(M)
    ax[1].imshow(HK(M))
    ax[2].imshow(Percolador(M))
    print("Número de Clusters:",CL(M))
    print("Número de Clusters Percolantes:",CL(Percolador(M)))
    plt.show()


### Función que retorna los indices y los valores de los vecinos de una celda del cluster

def closest_neighbours(A,i,j, L, M):

    pn = [[i-1,j], [i+1,j], [i,j-1], [i,j+1]]

    for i, t in enumerate(pn):
        if t[0] < 0 or t[1] < 0 or t[0] >= L or t[1] >= M:
            pn[i] = None
    indices = [c for c in pn if c is not None]

    neighbours = []
    for j in indices:
        neighbours.append(A[j[0]][j[1]])

    return indices, neighbours

def start_invasive_percolation(A,L,M):

    #La siguiente lista tendra como elementos
    #los neighbours de cada
    #celda en la que el líquido se encuentre

    list_of_closest_neighbours = []

    #Calculamos el lugar por donde se empieza
    #la filtración

    start_cell =A.min(axis = 1)[0]
    i, j = np.where(A == start_cell)

    list_of_closest_neighbours.append([closest_neighbours(A,i,j,L,M)])

    return i,j

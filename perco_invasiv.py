import numpy as np
import matplotlib.pyplot as plt
from random import *
from matplotlib import animation as anim
import imageio

### En este archivo pongan las implementaciones que vayan haciendo
### para los clusters y los params que debemos calcular.

def fill_lattice(A,L):
    random_nums = [i for i in range(1,L*L+1)]
    for i in range(0,L):
        for j in range(0,L):
            A[i,j] = choice(random_nums)
            random_nums.remove(A[i,j])
    return A

def closest_neighbours(A,element,L):
    l, m = np.where(A == element)

    i = l[0]
    j = m[0]

    pn = [[i-1,j], [i+1,j], [i,j-1], [i,j+1]]

    for i, t in enumerate(pn):
        if t[0] < 0 or t[1] < 0 or t[0] >= L or t[1] >= L:
            pn[i] = None
    indices = [c for c in pn if c is not None]

    neighbours = []
    for j in indices:
        neighbours.append(A[j[0]][j[1]])

    vecinos = np.array(neighbours)

    return indices, vecinos


def cross_element(A,element)-> None:
    l, m = np.where(A == element)

    i = l
    j = m

    A[i,j] = 0

def compute_coordinates(A,element):
    l, m = np.where(A == element)

    i = l
    j = m

    return i


#def invasion_percolation(A,L)->None:

def invasion_percolation(A,L):

    animation_list = []
    list_of_closest_neighbours = [list(closest_neighbours(A,i,L)[1]) for i in range(1,L*L+1)]
    closest_neighbours_of_crossed_elements = []
    list_of_crossed_elements = []
    next_element = 0
    auxiliary_list = []
    iterations = 0

    start_cell =A.min(axis = 1)[0]
    l, m = np.where(A == start_cell)
    i, j = l[0], m[0]
    start = A[i][j]

    list_of_crossed_elements.append(start)
    next_element = start

    closest_neighbours_of_crossed_elements = list_of_closest_neighbours[int(start)-1]
    list(closest_neighbours_of_crossed_elements)
    cross_element(A,start)

    C = np.copy(A)


    finish_flag = True


    while(finish_flag):



        #print("Elemento a eliminar: \t",next_element)


        if(0 in closest_neighbours_of_crossed_elements):
                    closest_neighbours_of_crossed_elements.remove(0)

        next_element = min(closest_neighbours_of_crossed_elements)
        #list_of_crossed_elements.append(next_element)

        #print("cnoce: \t", closest_neighbours_of_crossed_elements)

        closest_neighbours_of_crossed_elements += list(closest_neighbours(A,next_element,L)[1])

        closest_neighbours_of_crossed_elements = list(set(closest_neighbours_of_crossed_elements))

        closest_neighbours_of_crossed_elements.remove(next_element)
        cross_element(A,next_element)

        #print(A,"\n")
        iterations +=1

        k = compute_coordinates(C,next_element)[0]

        #print(k)
        if(k == L-1 ):
            finish_flag = False


        plot_mat = np.zeros([L,L])
        for i in range(0,L):
            for j in range(0,L):
                #if (A[i][j] != 0):
                plot_mat[i][j] = A[i][j]

        animation_list.append(plot_mat)




    return A,int(iterations), animation_list






### Aqui iniciaria el algoritmo ###





L = 50

B = np.zeros([L,L])
fill_lattice(B,L)
print(B)
C, iter, P = invasion_percolation(B,L)




fig, axs = plt.subplots()


def animate(frame):

    plt.cla()
    plt.grid()
    plt.xlabel("x")
    plt.ylabel("y")
    #plt.xlim(0,6)
    #plt.ylim(0,6)


    #plt.fill(np.arange(0,6,0.1), PD[frame], color = 'purple')
    plt.imshow(P[frame])


    plt.tight_layout()

movie = anim.FuncAnimation(fig, animate, frames = iter , interval = 250 ,repeat = True)
movie.save("IP.gif")
#plt.show()

#plt.figure()
#plt.imshow(plot_mat)
#plt.show()

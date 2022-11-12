import random
import numpy as np

### En este archivo pongan las implementaciones que vayan haciendo
### para los clusters y los params que debemos calcular.

def fill_lattice(A,L,M):
    random_nums = [i for i in range(0,L*M)]
    for i in range(0,L):
        for j in range(0,M):
            A[i,j] = random.choice(random_nums)
            random_nums.remove(A[i,j])
    return A

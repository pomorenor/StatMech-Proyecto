from percolib import *
M=RanMtz(0.58,size=(100,100))
fig, ax =plt.subplots(1,3)

ax[0].imshow(M)
ax[1].imshow(HK(M))
ax[2].imshow(Percolador(M))
print("Número de Clusters:",CL(M))
print("Número de Clusters Percolantes:",CL(Percolador(M)))
plt.show()
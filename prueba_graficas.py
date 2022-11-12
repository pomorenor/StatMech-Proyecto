from percolib import *
M=np.random.randint(2, size=(20,60))
fig, ax =plt.subplots(1,3)

ax[0].imshow(M)
ax[1].imshow(HK(M))
ax[2].imshow(Percolador(M))
print("Número de Clusters:",CL(M))
print("Número de Clusters Percolantes:",CL(Percolador(M)))
plt.show()
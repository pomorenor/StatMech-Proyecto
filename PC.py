from percolib import *
from scipy import stats
from scipy.optimize import curve_fit

#queremos ver la probabilidad de que se cree un cluster percolante, 
#en función de la probabilidad de ocupación de los sites


#PrPe recibe un tamaño y una lista de probalidades de ocupacion y
#retorna una de probabilidades de percolación
def PrPe(SZ,P):
    PP=[]
    for p in P:
        rep=80
        N=0
        for r in range(rep):
            M=RanMtz(p,size=(SZ,SZ))
            if CL(Percolador(M))!=0:
                N+=1
        PP.append(N/rep)
    return PP

#calcula la probabilidad crítica
def PC(P):
    SZ=35 #entre más grande, más preciso
    PP=PrPe(SZ,P)
    I0=[i for i,x in enumerate(PP) if x==0][-1]
    If=PP.index(1)
    PC=(P[If]+P[I0])/2
    return PC

#PrPe recibe un tamaño y una lista de probalidades de ocupacion y
#retorna una del parametro de orden
def PaOr(P,SZ):
    PO=[]
    for p in P:
        rep=120
        R=[]
        for i in range(rep): 
            N=0
            M=RanMtz(p,size=(SZ,SZ))
            MP=Percolador(M)
            if CL(MP)!=0:    
                for ii in range(len(MP)):
                    for jj in range(len(MP[0])):
                        if MP[ii,jj]!=0:
                            N+=1 
            R.append(N/(SZ*SZ))
            
        PO.append(np.mean(R))  
    return PO
#función para el ExCr
def Curva(x,a,b):
  return b*(x-0.59)**a

#calcula el exponente crítico
def ExCr(P,Pc):
    Po=PaOr(P,60)
    ep=0.01
    for p in range(len(P)):
        if np.fabs(P[p]-round(Pc,2))<ep:
            break 
    PrRz=np.copy(P[p+2:p+12])
    PORz=np.copy(Po[p+2:p+12])
    popt, pcov = curve_fit(Curva,PrRz,PORz)
    
    return Po,popt



if __name__ == '__main__':  
    P=np.arange(0.4,0.8,0.01)
    Pc=PC(P)
    AB=ExCr(P,Pc)
    Po=AB[0]
    popt=AB[1]
    plt.scatter(P,Po,color="m",label="simulado")
    plt.plot(P,Curva(P,popt[0],popt[1]),color="red",label="regresión")
    plt.text(0.45,0.6,"$Pc={:}$".format(round(Pc,3)))
    plt.text(0.45,0.4,"$Po={:}(P-Pc)**{:}$".format(round(popt[1],2),round(popt[0],2)))
    plt.grid()
    plt.legend()
    plt.xlabel("Probabilidad de ocupación")
    plt.ylabel("Parametro de orden")
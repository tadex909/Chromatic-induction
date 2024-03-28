#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 16:17:53 2019

@author: nicolasvattuone
"""

"""
Created on Thu Oct 24 13:30:00 2019

@author: nicolasvattuone
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from scipy.optimize import curve_fit



namelist= open("./namelist.dat","r").read().split("\n")
namelist.pop()

data=[]
"""Extract all the the data on the file namelist"""
for name in namelist:
    subject=[]
    print(name+"\n")
    results= open("./Results/"+name+".dat","r").read().split("\n")
    results.pop()
    results.pop(0)
    
    for a in results:
        subject.append( np.array( a.split("\t"), dtype=float))
    data.append(np.array(subject).T)




sigmas=[]
sigmaerr=[]
bias=[]
for i in range(len(namelist)):
    plt.xlabel("S coordinate")
    plt.ylabel("S Threshold")
    sigmas.append( data[i][1]+data[i][3])
    sigmaerr.append(  np.sqrt( (data[i][1]-data[i][3])**2/2 +    data[i][2]**2+ data[i][4]**2     ) )
    bias.append(data[i][1]-data[i][3])    
    plt.errorbar(data[i][0], sigmas[i], yerr=sigmaerr[i], fmt="-o",capsize=1 )

sigmas=np.array(sigmas)
sigmaerr= np.array(sigmaerr)
meterr= sigmaerr/sigmas**2

plt.savefig("results-crot.png",dpi=120)
plt.show()




""" Calculo las métricas para cada uno"""
s0=data[0][0][0]
sf=data[0][0][7]
x=np.linspace(s0,sf,50)
secante=  (data[0][0]-s0)/(sf-s0)

subjmet=[]
coefposta=[]
errorsubj=[]
for i in range(len(namelist)):
    metric=[]
    errormet=[]
    for j in range(1,9):
        metric.append(np.trapz( 1/sigmas[i][0:j],x=data[i][0][0:j]) )
        errormet.append(np.trapz(meterr[i][0:j]**2, x=data[i][0][0:j]) )
    coefposta.append(metric[7])
    subjmet.append(metric/metric[7])
    errorsubj.append(errormet/metric[7]**2)
    plt.errorbar(data[0][0],metric/metric[7],yerr= np.sqrt(errormet)/metric[7],fmt="-o",label= namelist[i])
plt.legend()
plt.plot(data[0][0],secante,"--")
plt.show()


materr=np.zeros((5,8,8))
for k in range(5):
    for i in range(8):
        for j in range(8):
            materr[k][i][j]= errorsubj[k][min([i,j])]





z2=[]

colors= ["C0", "C1", "C2", "C3", "C4"]



def parasym(x, a):
    s0=0.617799
    sf=2.28246
    return a*4*(x-s0)*(x-sf)/((s0-sf)**2)


fitteda=[]
errorfits=[]
for i in range(len(namelist)):
   fitscomp=curve_fit( parasym,  data[0][0], subjmet[i] - secante, sigma= materr[i]+ 1e-16 , p0=-0.05, bounds=(-1,0), absolute_sigma= True )
   fit2= fitscomp[0]
   errorfit= np.sqrt(fitscomp[1])
   fitteda.append(fit2)
   errorfits.append(errorfit[0])
   
   plt.xlabel("S coordinate")
   plt.ylabel("Deviation of Metric from identity")
   plt.errorbar( data[0][0],  subjmet[i]- secante, yerr= errorsubj[i],fmt="o", label=namelist[i] , color = colors[i])
   plt.plot(x,parasym(x,fit2)  ,color = colors[i])
   plt.title("One parameter fit")
plt.legend()
plt.savefig("./Figures/Metrics.png",dpi=300)
plt.show()


def funcsigma(x, a, c):
    s0=0.617799
    sf=2.28246
    return (  1/ (c*(1 + 8*a*( (x- (sf+s0)/2)/(sf-s0))) )  )





for i in range(len(namelist)):
    plt.xlabel("S coordinate")
    plt.ylabel("S Threshold")
    plt.errorbar(data[0][0], sigmas[i],yerr= sigmaerr[i],fmt="o",color=colors[i],capsize=2)
    plt.plot( x, funcsigma(x, fitteda[i],coefposta[i]/(sf-s0) ) ,  label=namelist[i],color=colors[i]) 
        
plt.savefig("./Figures/Datawithfit.png",dpi=300)
plt.show()
    

outmetric= open("./metricoefs.dat","w" )


stout="Coefs de la métrica de la forma sqrt(g)= A + B*x\n"
stout2=""
for i in range(len(namelist)):
    A= coefposta[i]/(sf-s0)*(1 -4*fitteda[i]*(sf+s0)/(sf-s0) )
    B=  8*fitteda[i]*coefposta[i]/((sf-s0)**2)
    stout= stout + str(A[0])+"\t"+str(B[0])+"\n"
    errorA=  np.sqrt( np.abs(coefposta[i]/(sf-s0)*(4*errorfits[i]*(sf+s0)/(sf-s0) ))**2 + (np.std(1/sigmas[i])/((sf-s0)*(sf-s0)*np.sqrt(8)))**2 )
    errorB=  8*errorfits[i]*coefposta[i]/((sf-s0)**2)  + 8*fitteda[i]*(np.std(1/sigmas[i])/(((sf-s0)**3)*np.sqrt(8)) )
    stout2= stout2 + str(np.round(A[0],1) ) +" \pm " + str(np.round(errorA[0],1))+"\t"
    stout2= stout2+ str( np.round(B[0],1) )+ " \pm " + str(np.round(errorB[0],1))+"\n" 
    
    plt.errorbar(data[0][0], 1/sigmas[i],yerr= sigmaerr[i]/(sigmas[i])**2,fmt="o",color=colors[i],capsize=2)
    plt.plot( x,  A+B*x  ,color=colors[i]) 
    
plt.show()


outmetric.write(stout)
outmetric.close()


out2= open("./forlatex.dat","w")
out2.write(stout2)
out2.close()



    
    
    

        


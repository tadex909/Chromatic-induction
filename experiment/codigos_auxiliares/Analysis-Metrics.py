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



""" This creates the file of the sigmas properly interpolated for the adaptation experiments """


adapt=[]

for i in range(len(namelist)):
    newout = open("./For_Adaptation/"+namelist[i],"w")
    a= list(sigmas[i])
    a.pop(-1)
    a.insert(6, (sigmas[i][6]+sigmas[i][5])/2 )
    adapt.append(a)
    b= list(data[i][0])
    b.pop(-1)
    b.insert(6, (data[i][0][6]+data[i][0][5])  /2 )
    strout=""
    for j in range(8):
        strout= strout + str(b[j])+ "\t"+str(a[j]) + "\n"
        
    newout.write(strout)
    newout.close()




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






for i in range(len(namelist)):
    plt.plot( np.log(data[0][0]),  np.log(subjmet[i]), "-o", label=namelist[i] )
    
plt.legend()
plt.show()



for i in range(len(namelist)):
    plt.plot( data[0][0],  subjmet[i]-np.linspace(0,1,8), "-o", label=namelist[i] )
    


    

    
plt.legend()
plt.show()
z2=[]

colors= ["Blue", "Orange", "Green", "Red", "Purple"]



for i in range(len(namelist)):
   fit2= np.polyfit(  data[0][0], subjmet[i] - secante, 3 )
   z2.append( np.poly1d(fit2))
   plt.errorbar( data[0][0],  subjmet[i]-secante,fmt="o", label=namelist[i] , color = colors[i])
   plt.plot(x,z2[i](x),color = colors[i])
   plt.title("Degree 3, with free parameters polynomial")
plt.legend()
plt.show()
plt.close()



def parasym(x, a):
    s0=0.617799
    sf=2.28246
    return a*4*(x-s0)*(x-sf)/((s0-sf)**2)



fitteda=[]
errorfits=[]
for i in range(len(namelist)):
   fitscomp=curve_fit( parasym,  data[0][0], subjmet[i] - secante, sigma= np.sqrt(materr[i]+ 1e-16) , p0=-0.05, bounds=(-1,0) )
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



def rational(x, b,c):
    return ( 1/(b+c*x) )


"""Fiteo la función racional"""
params=[]
for i in range(len(namelist)):
    (b,c), cov=curve_fit(rational, data[0][0], sigmas[i], sigma= sigmaerr[i])
    print( (c/b))
    plt.errorbar(data[0][0], sigmas[i],yerr= sigmaerr[i],fmt="o",color=colors[i],capsize=2)
    plt.plot( x, rational(x,b,c), color=colors[i])
    params.append( np.array([b,c]))
    
plt.show()

""" Fiteo más metrica"""
def integrat(x, a, b):
    return a*x+b*(x**2)/2


for i in range(len(namelist)):
    (a0,b0) = params[i]
    plt.plot(x, (integrat(x,a0,b0) - integrat(s0,a0,b0))/(integrat(sf,a0,b0) - integrat(s0,a0,b0)) - (x-s0)/(sf-s0)   , color= colors[i])
    plt.plot( data[0][0],  subjmet[i]- secante , "o", label=namelist[i] , color = colors[i])
    print( b0/(a0+b0*1.48))
    print("\n")
plt.show()
    

plt.close()
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


""" Más fácil"""


def fl( x, *A):
    A= np.array(A).ravel()
    return A[0]+ A[1]*x
p0=[1,-1]
x=data[0][0]
newpar=[]
for i in range(5):
    y = 1/sigmas[i]
    yrr= sigmaerr[i]/sigmas[i]**2
    par, cov= curve_fit(fl,x,y,sigma=yrr,p0=p0)
    newpar.append(par)
    print(par,"+-", np.sqrt(np.diag(cov)))
    plt.errorbar(x,y,yerr=yrr, fmt="o",color=colors[i])
    plt.plot(x,fl(x,par),"-",color=colors[i])
    
plt.show()
for i in range(5):
    a0,b0= newpar[i]
    plt.plot(x, (integrat(x,a0,b0) - integrat(s0,a0,b0))/(integrat(sf,a0,b0) - integrat(s0,a0,b0)) - (x-s0)/(sf-s0)   , color= colors[i])
    plt.errorbar( data[0][0],  subjmet[i]- secante , yerr= errorsubj[i]/10, fmt="o", label=namelist[i] , color = colors[i])
    
    
    
    

        


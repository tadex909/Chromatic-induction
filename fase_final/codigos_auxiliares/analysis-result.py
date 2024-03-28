#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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








for i in range(len(namelist)):
    plt.xlabel("S coordinate")
    plt.ylabel("S Threshold")
    plt.errorbar(data[i][0], data[i][1], yerr=data[i][2], fmt="-o" )
    plt.errorbar(data[i][0],data[i][3],yerr=data[i][4],fmt="-o")
plt.show()


sigmas=[]
sigmaerr=[]
bias=[]
for i in range(len(namelist)):
    plt.xlabel("S coordinate")
    plt.ylabel("S Threshold")
    sigmas.append( data[i][1]+data[i][3])
    sigmaerr.append(data[i][2]+data[i][4])
    bias.append(data[i][1]-data[i][3])    
    plt.errorbar(data[i][0], sigmas[i], yerr=sigmaerr[i], fmt="-o",capsize=1 )

sigmas=np.array(sigmas)
plt.show()






Acoefs=[]
for i in range(len(namelist)):
    plt.xlabel("S coordinate")
    plt.ylabel("S Threshold/mean")
    Acoefs.append(1/np.mean(sigmas[i]))
    plt.errorbar(data[i][0], sigmas[i]*Acoefs[i], yerr=sigmaerr[i]*Acoefs[i], fmt="o",capsize=1 )

plt.show()



""" All normalized"""
for i in range(len(namelist)):
    plt.xlabel("S coordinate/mean")
    plt.ylabel("S Threshold/mean")
    plt.errorbar((data[i][0]-1.48)/np.mean(data[i][1]+data[i][3]), (data[i][1]+data[i][3])/np.mean(data[i][1]+data[i][3]), yerr=data[i][2]+data[i][4], fmt="-o" )
    
plt.show()

meanresp= np.zeros((5,8))
for i in range(len(namelist)):
    meanresp= meanresp+ np.array(data[i])

meanresp= meanresp/5
firstchi=0
meanerror1=0


for i in range(len(namelist)):
    firstchi= firstchi + (((meanresp[3]+meanresp[1]) - np.array(data[i][1]+data[i][3]))/np.array(data[i][1]+data[i][3]))**2
    meanerror1= meanerror1 + ((meanresp[3]+meanresp[1]) - np.array(data[i][1]+data[i][3]))/np.array(data[i][1]+data[i][3])




plt.plot( meanresp[0], meanresp[1]+meanresp[3],"-o")
plt.show()


plt.show()


""" Comparación entre los coeficienes usados y el de componentes principales"""
"""
usedcoefs=[]
pcacoefs=[]
for i in range(len(namelist)):
    usedcoefs.append(  np.mean(data[i][1]+data[i][3]  )/np.mean( meanresp[1]+meanresp[3]) )
    pcacoefs.append( np.dot(data[i][1] +data[i][3],meanresp[1] +meanresp[3])/np.dot(meanresp[1] +meanresp[3],meanresp[1] +meanresp[3])  ) 


print(usedcoefs)
print(pcacoefs)

plt.ylim((0.9,1.1))
plt.plot(np.ones(5),"-")
plt.plot(usedcoefs/np.array(pcacoefs),"o")
plt.show()


for i in range(len(namelist)):
    chisquare= chisquare+  (( normalmean -((data[i][1]+data[i][3])/np.mean(data[i][1]+data[i][3])))/((data[i][1]+data[i][3])/np.mean(data[i][1]+data[i][3])) )**2
    meanerror2= meanerror2+ (( normalmean -((data[i][1]+data[i][3])/np.mean(data[i][1]+data[i][3])))/((data[i][1]+data[i][3])/np.mean(data[i][1]+data[i][3])) )

chisquare=0
meanerror2=0



print("chi1="+str(np.sum(firstchi)/(8*5)))
print("chi2="+str(np.sum(chisquare)/(8*5)))
print("meanerror1="+str(np.sum(meanerror1)/(8*5) ) )
print("meanerror2="+str(np.sum(meanerror2)/(8*5) ) )



"""


"""Calculo el promedio usando los gráficos renormalizados por valor medio y pesando por error"""
normalmean=np.zeros(8)
normalerror=((np.array(sigmaerr).T*np.array(Acoefs)).T)
normalsigma= ((np.array(sigmas).T*np.array(Acoefs)).T)
totcoefs= np.zeros((len(namelist),8))
toterror= np.sum(1/ (normalerror)**2,axis=0)


for i in range(len(namelist)):
    totcoefs[i]= Acoefs[i]/(toterror*(normalerror[i])**2) 
    normalmean=  normalmean + sigmas[i]*totcoefs[i]
    
intersubjvar =  np.sqrt(np.sum( (normalmean - normalsigma)**2, axis=0 )/5)

print(intersubjvar)


z=np.polyfit( data[0][0], normalmean, 3, w= 1/intersubjvar)
p= np.poly1d(z)
dp=np.poly1d((z*[3,2,1,0])[np.array([0,1,2])])
x=np.linspace(0.38,2.4,100)
plt.errorbar(data[0][0],normalmean, yerr=intersubjvar, fmt="o")
plt.plot(x,p(x),"red")

plt.show()






for i in range(len(namelist)):
    plt.xlabel("S coordinate")
    plt.ylabel("S Threshold")
    plt.errorbar(data[i][0], sigmas[i], yerr=sigmaerr[i], fmt="o",capsize=1,color= [0.2*i%1,0.2*(i+2)%1,0.2*(i+4)%1] )
    plt.plot( x, p(x)/Acoefs[i],color= [0.2*i%1,0.2*(i+2)%1,0.2*(i+4)%1]  )

plt.savefig("./Figures/Finalresult.png",dpi=300)

plt.show()
compdf=np.zeros(8)
for i in range(5):
    compdf= compdf - totcoefs[i]*4*bias[i]/sigmas[i]


x2=np.linspace(0.6,2.3,100)
plt.plot(meanresp[0],compdf,"-o")
plt.plot(x2,dp(x2))
plt.show()

output= open("./fit.dat","w")
s="Polynomials coefs"+"\n" + str(z)+"\n"+"Subjects mean"+"\n"+str(1/np.array(Acoefs))
output.write(s)
output.close()



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
subjmet=[]
coefposta=[]
for i in range(len(namelist)):
    metric=[]
    for j in range(1,9):
        metric.append(integrate.simps( sigmas[i][0:j],x=data[i][0][0:j]) )
    coefposta.append(metric[7])
    subjmet.append(metric/metric[7])
    plt.plot(data[0][0],metric/metric[7],"-o",label= namelist[i])
plt.legend()
plt.plot(data[0][0],np.linspace(0,1,8),"--")
plt.show()

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

x= np.linspace( 0.61777,2.28246,100 )

for i in range(len(namelist)):
   fit2= np.polyfit(  data[0][0], subjmet[i] - np.linspace(0,1,8), 3 )
   z2.append( np.poly1d(fit2))
   plt.plot( data[0][0],  subjmet[i]-np.linspace(0,1,8), "o", label=namelist[i] , color = colors[i])
   plt.plot(x,z2[i](x),color = colors[i])
   plt.title("Degree 3, with free parameters polynomial")
plt.legend()
plt.show()




def parasym(x, a):
    s0=0.617799
    sf=2.28246
    return a*4*(x-s0)*(x-sf)/((s0-sf)**2)


for i in range(len(namelist)):
   fit2= curve_fit( parasym,  data[0][0], subjmet[i] - np.linspace(0,1,8), p0=0.05, bounds=(0.001,1) )[0]
   print(fit2)
   plt.plot( data[0][0],  subjmet[i]-np.linspace(0,1,8), "o", label=namelist[i] , color = colors[i])
   plt.plot(x,parasym(x,fit2),color = colors[i])
   plt.title("One parameter fit")
plt.legend()
plt.show()





def rational(x, b,c):
    return ( 1/(b+c*x) )


for i in range(len(namelist)):
    (b,c), cov=curve_fit(rational, data[0][0], sigmas[i])
    print( (c/b))
    plt.errorbar(data[0][0], sigmas[i],yerr= sigmaerr[i],fmt="o",color=colors[i],capsize=2)
    plt.plot( data[0][0], rational(data[0][0],b,c), color=colors[i])







""" Fiteos individuales """
"""
fits=[]
polys=[]
for i in range(len(namelist)):
    fits.append( np.polyfit(data[0][0], sigmas[i],3)  )
    polys.append( np.poly1d(fits[i]))
    plt.plot(data[0][0], sigmas[i],"o")
    plt.plot(x, polys[i](x),"Red")
    plt.show()
"""




#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 16:50:58 2020

@author: nicolasvattuone
"""

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
from scipy.stats import chi2





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
    subject.sort(key= lambda x: x[0]   )
    data.append( np.array(subject).T)



        




colors= ["Blue", "Orange", "Green", "Red", "Purple"]



sigmas=[]
sigmaerr=[]
bias=[]
for i in range(len(namelist)):
    plt.xlabel("S coordinate")
    plt.ylabel("S Threshold")
    plt.title("Just the sigma for each subject")
    sigmas.append( data[i][1]+data[i][3])
    sigmaerr.append(data[i][2]+data[i][4])
    bias.append(data[i][3]-data[i][1])    
    plt.errorbar(data[i][0], sigmas[i], yerr=sigmaerr[i], fmt="-o",capsize=1, label=namelist[i] )

sigmas=np.array(sigmas)
sigmaerr=np.array(sigmaerr)
bias= np.array(bias)
plt.legend()
plt.show()





""" Bias normalizado por la métrica vieja"""

for i in range(5):
    plt.plot(data[0][0], bias[i]*(A[i]+B[i]*data[0][0]),"o")
    
plt.show()

""" Bias normalizado por la métrica nueva"""

errornorm= sigmaerr*(1/sigmas +  bias/sigmas**2  )
plt.xlabel("S coordinate")
plt.ylabel("Asymmetry/Threshold")
for i in range(5):
    plt.errorbar( data[0][0], bias[i]/sigmas[i], yerr= errornorm[i], fmt="-o", label=namelist[i])

plt.legend()
plt.show()





meannormbias= np.average( bias/sigmas,axis=0, weights= errornorm) 


stdbias= np.sqrt( np.std( bias/sigmas,axis=0)**2 +  np.mean( errornorm, axis=0)**2 )

plt.errorbar( data[0][0], meannormbias,yerr= stdbias, fmt="o")


cc=1.125

def mysign(x,b,c0):
    return c0-b* np.sign(x-cc)

def constant(x,b):
    return b

fff= curve_fit( mysign, data[0][0], meannormbias, sigma= stdbias   )


xx= np.linspace(0.6,2.2,100)
plt.plot(xx, mysign(xx, fff[0][0],fff[0][1]),"-")

f2= curve_fit( constant, data[0][0], meannormbias, sigma= stdbias )
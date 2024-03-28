#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 14:56:48 2019

@author: nicovattuone
"""

import rgb2sml
import matplotlib.pyplot as plt
import numpy as np


calib= rgb2sml.calibration(rgb2sml.openfile()) # Load the parameters of the calibration file
transf= rgb2sml.transformation(calib.A0(), calib.AMatrix(), calib.Gamma()) # Creates an object transf that has as methods all the needed transformations
Stimuli = transf.listS()
Stimuli.sort(key= lambda x: transf.rgb2sml(x)[0])  # This list constains all the possible values to be used as stimuli
Sstim = []
Mstim= []
Lstim=[]
for a in Stimuli:
    Sstim.append( transf.rgb2sml(a)[0])
    Mstim.append(transf.rgb2sml(a)[1])
    Lstim.append(transf.rgb2sml(a)[2])
difS=[]
difM=[]
difL=[]

sm= np.mean(Sstim)
newlist=[]
for a in Stimuli:
    if np.abs(transf.rgb2sml(a)[0] - sm) < 0.005:
        newlist.append(a)

newMstim=[]
newSstim=[]
newLstim=[]
for a in newlist:
    newMstim.append( transf.rgb2sml(a)[1] )
    newSstim.append( transf.rgb2sml(a)[0] )


for j in range(len(Sstim)-1):
    difS.append( Sstim[j+1] -  Sstim[j] )
    difM.append( Mstim[j+1]- Mstim[j])
    difL.append( Lstim[j+1]- Lstim[j])
    
plt.plot(Sstim[:-1] ,difS*np.power(Sstim[:-1],-1) )

plt.show()
plt.plot(Mstim[:-1],difM*np.power(Mstim[:-1],-1)) 
plt.show()

plt.plot(Lstim[:-1],difL*np.power(Lstim[:-1],-1) )

plt.show()


maux= (np.array(Mstim) - np.mean(Mstim))/ 0.2
saux=(np.array(Sstim)-np.mean(Sstim))/ 0.1
laux= (np.array(Lstim) - np.mean(Lstim))/ np.mean(Lstim)
fig = plt.figure()
ax= fig.add_subplot(111)
ax.plot( maux[30:50], saux[30:50] ,"o")
ax.set_aspect(aspect=0.5)
plt.show()
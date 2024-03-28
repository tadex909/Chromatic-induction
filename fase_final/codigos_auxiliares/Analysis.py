#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 10:25:56 2019

@author: nicovattuone
"""

from scipy.optimize import curve_fit
import numpy as np
import random
import matplotlib.pyplot as plt

global Nr,Nd,Nb
Nr=20
Nd=15
Nb=8


def extract (name, num):
    a=open("./Subjects/"+name+"/"+name + str(num) +".dat","r")
    data= a.read()
    c=[]
    if data.startswith("Subject"):
        data=data.split("adapted \n")[1]
    b= data.split("\n")
    b.remove('')
    for d in b:
        c+= [ (float(d.split("\t")[0]),float( d.split("\t") [1]), int(d.split("\t")[2])    ) ] 
   # c.sort(key= lambda x: x[0] )
    return c

def buildhist( neg , pos):
    neg=list(neg)
    pos=list(pos)
    tot= neg + pos
    bins = list( set(tot))
    bins.sort()
    y=[]
    for a in bins:
        y.append(neg.count(a))
    return (bins,y)
    
def sigmoidL(x, a, b):
    return( 0.375 + 0.375* np.tanh((x - b )/a )   )

def sigmoidR(x,a,b):
    return( 0.375 - 0.375* np.tanh((x - b )/a )   )


def fitsigmoids( his ):
    global Nr, Nd, Nb
    xdataL = np.array( his[0][0:int((Nd+1)/2)])
    ydataL= np.array( his[1][0:int((Nd+1)/2)])/Nr
    parL, covL = curve_fit( sigmoidL, xdataL, ydataL)
    xdataR = np.array( his[0][int((Nd-1)/2):])
    ydataR= np.array( his[1][int((Nd-1)/2):])/Nr
    parR, covR = curve_fit( sigmoidR, xdataR, ydataR)
    
    
    return ( (parL,covL, parR, covR)   )

def plothis( his, fit, name):
    fig = plt.figure()
    plt.bar( his[0], np.array(his[1])/20 , 0.8*( his[0][0] - his[0][1]) )
    x= np.linspace(his[0][0],his[0][-1],100)
    plt.plot( x , sigmoidL(x, fit[0][0],fit[0][1] ) ,"green", label= "a="+str(np.round(fit[0][0],4))+"\nb="+str(np.round(fit[0][1],4)))
    plt.plot( x, sigmoidR( x, fit[2][0],fit[2][1] ) ,"purple", label="a="+str(np.round(fit[2][0],4))+"\nb="+str(np.round(fit[2][1],4)) )
    legend= plt.legend()
    fig.suptitle(name)
    plt.xlabel('S coordinate')
    plt.ylabel('Error probability')
    plt.show()





name="nvattuone"
 
Ns=1



Resultsx=[]
Resultsy=[]
c=[]
for n in range(Nb):
    caux= extract(name ,n+1)
    c.append(caux)


rev=[]
pos=[]
for d in c:
    x=[]
    y=[]
    z=[]

    
    for j in range(len(d)):
       x.append( d[j][0] )

       if d[j][2] ==0:
           y.append(d[j][1])
       else: 
           z.append(d[j][1])
   
       
    rev.append(y)
    pos.append(z)
          






"""
allrev=[]
m=0
for d in c:
    x=[]
    y=[]
    z=[]
    rev=[]
    pos=[]
    
    for j in range(len(d)):
       x.append( d[j][0] )

       if d[j][2] ==0:
           y.append(d[j][1])
       else: 
           z.append(d[j][1])
   
       if (j+1)% (Nr*Nd)==0:
           rev.append(y)
           y=[]
           pos.append(z)
           z=[]

    sigma=[]
    mu=[]
    error=[]
    for i in range(0,Nb):
      sigma.append( np.std(rev[i] ) )
      mu.append( np.mean(rev[i] )   )
      error.append((np.mean(rev[i])- x[i*Nr*Nd+1] )) 

    Results.append(mu)
    Results.append(sigma)
    plt.plot( mu, sigma,"-o")
    
    if m==0:
        allrev = allrev+ rev
    else:
        for k in range(len(rev)):
            allrev[k]= allrev[k] + rev[k]
    m+=1
plt.show()



for k in range(2):
    plt.plot( Results[2*k],Results[2*k+1],"-o")
    plt.show()

plt.plot(Results[0], (np.array(Results[1])+np.array(Results[3]))/2,"-o")
"""
"""
mu = []
band=[]
for k in range(Nb):
    mu.append(  (np.mean(rev[2*k]) + np.mean(rev[2*k+1]))/2  ) 
    band.append(  np.mean(rev[2*k+1] ) - np.mean(rev[2*k]) )

plt.plot(mu, band,"-ro")

xm=[]
for i in range(len(x)):
    if i%Nr==0:
        xm.append(x[i])

error = mu - np.array(xm)
plt.show()
plt.plot( error, "-ro")

dband=[]
uband=[]
for k in range(Nb):
    dband.append(np.min(rev[2*k]))
    uband.append(np.max(rev[2*k+1]))
    
plt.show()
plt.plot(np.array(uband)-np.array(dband),'ro' )

"""

"""



for k in range(0,Nb):
    plt.hist(  y[Nr*k:Nr*(k+1)],10)
    plt.show()
sigma=[]
mu=[]
error=[]
for i in range(0,Nb):
  sigma.append( np.std(y[ i*Nr : (i+1)*Nr] ) )
  mu.append( np.mean(y[i*Nr  : (i+1)*Nr]  )   )
  error.append((np.mean(y[i*Nr  : (i+1)*Nr]  ) - x[i*Nr+1] ))

plt.plot(mu,'ro')
plt.show()
plt.plot(mu,sigma,'ro')

plt.show()
plt.plot(error ,'ro')
plt.show()

s= np.array(sigma)*np.array(sigma)
fit=np.polyfit(mu[3:8],sigma[3:8],1)
def f(x): return np.polyval(fit,x)

#plt.plot(mu ,sigma*np.power(mu,-1),'o')
#plt.plot(mu[3:8],f(mu[3:8]),'-')
"""
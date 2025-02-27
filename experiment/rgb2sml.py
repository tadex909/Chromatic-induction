#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 14:59:35 2019

This module contains a set of functions designed to read the data from a calibration file named as "  .rgb2lms"
Then, use this information to convert rgb values to sml values ( yeah, in that order)


@author: nicovattuone
"""




import os # necesary to work with your directories
import numpy as np 
import pygame



# This function looks in the directory basepath the file ending with rgb2lms,
# its output is a string with the data in the file
def openfile():
    basepath= 'experiment/'
    with os.scandir(basepath) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith("rgb2lms"):
                file= open(basepath+entry.name,"r")
    return file.read()                         

# the calibration class will contain the information of the matrix necesary to do the transformation which is of the form,
# data is the string that receives from the function openfile() and then turns them to numpy variables
# (s,m,l) = A . (rˠ, gˠ, bˠ) +  A₀
class calibration():
    def __init__(self, data):
        self.data=data
    def A0(self):
        A0=[]
        a= self.data.split("\n")
        for j in range(len(a)):
            if a[j].strip().find("[A0S, A0M, A0L]") != -1:
                for b in a[j+1].strip().split(","):
                    A0.append(float(b))   
        return( np.array(A0))
 
    
    def AMatrix(self):
        A=[]
        v=[]
        a= self.data.split("\n")
        for j in range(len(a)):
            if a[j].strip().find("ArL, AgL, AbL") != -1:
                for k in range(1,4):
                     for c in a[j+k].strip().split(","):
                        v.append(float(c))
                     A.append(v)
                     v=[]
        return(np.matrix(A))
    
    
    def Gamma(self):
         gamma=[]    
         a= self.data.split("\n")
         for j in range(len(a)):
             if a[j].strip().find("[rgamma, ggamma, bgamma]") != -1:
                for b in a[j+1].strip().split(","):
                    gamma.append(float(b))  
         return(np.array(gamma))

# Transformation class will receive  the value of A₀, A and ˠ

class transformation():
    def __init__(self, A0, A, Gamma):
        self.A= np.around(A, decimals=10)
        self.A0=  np.around(A0, decimals=10)
        self.Gamma=  np.around(Gamma, decimals=10)
        self.InvA= np.linalg.pinv(np.around(A, decimals=10))
    #  Converts  (r,g,b) to (s,m,l)
    def rgb2sml(self, rgb):
        rgb= ( rgb[0] %256,  rgb[1] %256,  rgb[2] %256)
        c= np.array( rgb )
        if len(c) >3:
            c=np.resize(c,3)
        return (np.squeeze(np.asarray(np.dot(self.A, np.power(c , self.Gamma)) )) + self.A0)
    #  Converts  (s,m,l) to (r,g,b)    
    def sml2rgb(self, sml):
        c=np.array(sml)
        rgb=  np.power( np.abs( np.squeeze(np.asarray( np.dot( self.InvA ,  (c - self.A0) ) )) )       , 1/(self.Gamma) ) 
        return ( np.array( [ rgb[0] % 256   ,rgb[1] % 256, rgb[2] %256 ] ) )
    
    def truncsml(self,sml):
        return self.rgb2sml( self.sml2rgb(sml) )
    
     
    def center(self):
        vertex1= self.A0
        vertex2= self.rgb2sml((255,0,0))
        vertex3= self.rgb2sml((0,255,0))
        vertex4= self.rgb2sml((0,0,255))
        vertex8= vertex2 + vertex3 + vertex4
        c=  (vertex8+vertex1)/2
        return np.array(c)
    
    
    def isindomain(self,sml):
        sml=np.array(sml)
        s1= np.sum( np.less( np.squeeze(np.asarray( np.dot( self.InvA ,  (sml - self.A0) ) )) ,0  ) ) # it checks if the transformation is invertible 
        s2 =  np.sum( np.greater( np.rint( self.sml2rgb(sml)),255) ) # it checks if the transformation is invertible 
        return (s1+s2==0)
    

    
    def deltasml(self, sml):
        return( self.Gamma * np.squeeze( np.asarray( np.dot( self.A, np.power( np.abs( np.array(self.sml2rgb(sml)) ), self.Gamma -1   ) ) ) ) )            
        
        
    def listS(self):
        c= np.array(self.center())
        listS=[]
        while (self.isindomain(c - 0.2*np.array( ( self.deltasml(c)[0], 0, 0)) )) :
            c = c - 0.2*np.array( ( self.deltasml(c)[0], 0, 0))
        
        while (self.isindomain(c + 0.2* np.array( ( self.deltasml(c)[0], 0, 0)) )) :
            caux=c
            c = c + 0.2* np.array( ( self.deltasml(c)[0], 0, 0))
            if np.sum( np.abs( self.sml2rgb(c) -self.sml2rgb(caux))) > 5:
                return listS
                break
            elif (np.sum(self.sml2rgb(c) != self.sml2rgb(caux)) >0 and  self.truncsml(c)[0]- self.truncsml(caux)[0] > 0.001):
                listS.append( self.sml2rgb(c))
           
        return listS

 
    def listM(self):
        c= np.array(self.center())
        listM=[]
        while (self.isindomain(c + 0.1*np.array( ( 0, self.deltasml(c)[1], 0)) )) :
            c = c + 0.1*np.array(  ( 0, self.deltasml(c)[1], 0))
        c= c- 0.1*np.array(  ( 0, self.deltasml(c)[1], 0))   
        
        while (self.isindomain(c - 0.1* np.array(  ( 0, self.deltasml(c)[1], 0) ) )) :
            caux=c
            c = c - 0.1* np.array(  ( 0, self.deltasml(c)[1], 0))
            if np.sum( np.abs( self.sml2rgb(c) -self.sml2rgb(caux))) > 5:
                listM.sort(key= lambda x: self.rgb2sml(x)[1]) 
                return listM
                break
            elif(np.sum(np.trunc(self.sml2rgb(c)) != np.trunc(self.sml2rgb(caux)) ) >0 ):
                listM.append( np.trunc( self.sml2rgb(c)) )
        listM.sort(key= lambda x: self.rgb2sml(x)[1]) 

        return listM


    def listL(self):
        c= np.array(self.center())
        listL=[]
        while (self.isindomain(c + 0.1*np.array( ( 0, 0,self.deltasml(c)[2])) )) :
            c = c + 0.1*np.array(  ( 0,0, self.deltasml(c)[2]))
        c= c- 0.1*np.array(  ( 0,0, self.deltasml(c)[2]))   
        
        while (self.isindomain(c - 0.1* np.array(  ( 0,0, self.deltasml(c)[2]) ) )) :
            caux=c
            c = c - 0.1* np.array(  ( 0,0, self.deltasml(c)[2]))
            if np.sum( np.abs( self.sml2rgb(c) -self.sml2rgb(caux))) > 5:
                listL.sort(key= lambda x: self.rgb2sml(x)[2]) 
                return listL
                break
            elif (np.sum(np.trunc(self.sml2rgb(c)) != np.trunc(self.sml2rgb(caux)) ) >0 ):
                listL.append( np.trunc(self.sml2rgb(c)) )
        listL.sort(key= lambda x: self.rgb2sml(x)[2]) 

        return listL


    def changeM(self, rgb, deltaM):
        aux= self.rgb2sml(rgb) + np.array([0, deltaM,0])
        return (self.sml2rgb(aux))
    
    def changeL(self, rgb, deltaL):
        aux= self.rgb2sml(rgb) + np.array([0, 0, deltaL])
        return (self.sml2rgb(aux))

    def topS(self):
        c= np.array(self.center())
        i=0
        while( self.isindomain(c +  np.array( ( self.deltasml(c)[0], 0, 0)))  ):
            c = c +  np.array( ( self.deltasml(c)[0], 0, 0))
            print(c)
            print( self.sml2rgb(c))
            
        print(i)
        return(c[0])
    
    def botS(self):
        c= np.array(self.center())
        while (self.isindomain(c - np.array( ( self.deltasml(c)[0], 0, 0)) )) :
            c = c - np.array( ( self.deltasml(c)[0], 0, 0))
            
        return(c[0])
        
   
    def changeS(self, rgb, deltaS):
        aux= self.rgb2sml(rgb) + [deltaS,0,0]
        return( self.sml2rgb(aux))

    def changeSML(self, rgb, amplitude, direction):
        aux = self.rgb2sml(rgb) + amplitude/np.linalg.norm(direction)*np.array(direction)
        return( self.sml2rgb(aux))

    def projection_in_direction_of_variation(self, rgb, direction):
        aux = np.dot(self.rgb2sml(rgb),1/np.linalg.norm(direction)*np.array(direction))
        return aux



from array import array
import pygame # Main module to develope the game
import random # Just a random module
import numpy as np
import os # Module to read and create directories
import rgb2sml # Module that contains the functions necessary to read the calibration file and make the transformations between rgb and sml
import Intro # Module that contains the start scene of the expriments and creates the file systems to save the data
import datetime # MOdule to print the date time of the experiment
 # Initializes the game
pygame.init()
# Monitor Info (height and width)
Monitor= pygame.display.Info();
h= Monitor.current_h
w= Monitor.current_w

global outputfile # These variable will account for the outputfile of the experiment


up = 0
right = 1
down = 2
left = 3
"""Here I load the calibration file (see module rgb2sml), which has to be the only file with the endname rgb2sml in main file directory"""
calib= rgb2sml.calibration(rgb2sml.openfile()) # Load the parameters of the calibration file
transf= rgb2sml.transformation(calib.A0(), calib.AMatrix(), calib.Gamma()) # Creates an object transf that has as methods all the needed transformations
Stimuli = transf.listS() # This list constains all the possible values to be used as stimuli
L= int( len(Stimuli)) 





def colortopygame( color):  # This functions receives an array and returns a pygame Color object
    return pygame.Color( int(color[0]) %256  ,int(color[1]) %256,int(color[2]) %256)


def texturizador(parche_crudo,largo_x,largo_y):

    parche_nuevo = parche_crudo

    for i in range(largo_x):
        for j in range(largo_y):
            color = parche_crudo[i,j,:]
            entero = np.floor(color)
            probs = color - entero
            valores = [1,0]
            probs1 = [probs[0],1-probs[0]]
            probs2 = [probs[1],1-probs[1]]
            probs3 = [probs[2],1-probs[2]]
            cambio1 = np.random.choice(valores,p = probs1)
            cambio2 = np.random.choice(valores,p = probs2)
            cambio3 = np.random.choice(valores,p = probs3)
            cambio = [cambio1,cambio2,cambio3]
            parche_nuevo[i,j,:] = entero + cambio
    return color
    
    
                         

def dist(i,j):
            distancia = float(np.sqrt((i)**2 +(j)**2))
            return distancia


def tex_patches_creator(Nb,Nd,size,k):
    Patches= []
    Paux=[]
    Sincrements= np.array([ 0.006     ,  0.00628571,  0.00757143,  0.00885714,  0.01014286,
        0.01142857,  0.01271429,  0.014     ])
    
    comun = "patches/"

    nombre_k = "k_" + str(k)
    
    os.mkdir(comun+nombre_k)

    
    for i in range(8) :
        for j in range(Nd):
            color = transf.changeS(  Stimuli[int(np.linspace(0.2*L,0.96*L, Nb)[i])], -((Nd-1)/2 - j )*Sincrements[i] )
            back_color = Stimuli[int(np.linspace(0.2*L,0.96*L, Nb)[i])]
            
            pos = [up,down,right,left]

            for position in pos:

                if(position == up or position == down):
                    size_x = int(np.sqrt(2)*size)
                    size_y = int(size)
                    parche = np.zeros((size_x,size_y,3))
                if(position == left or position == right):
                    size_x = int(size)
                    size_y = int(np.sqrt(2)*size)
                    parche = np.zeros(size_x,size_y)
                    
                for n in range(int(size_x)):
                    for m in range(int(size_y)):
                        if pos == up:
                            carpeta = "up/"
                            i_center = int(size_x/2)
                            j_center = size_y
                            screen_center = [i_center, j_center]
                            if np.abs(n-i_center) <= np.abs (m-j_center):
                                parche[n,m,:] = back_color + (color-back_color)*np.sinc(k*dist(n-screen_center[0],m-screen_center[1]))
                            else:
                                parche[n,m,:] = back_color
                            
                        if pos == down:
                            carpeta = "down/"
                            i_center = int(size_x/2)
                            j_center = 0
                            screen_center = [i_center, j_center]
                            if np.abs(n-i_center) <= np.abs (m-j_center):
                                parche[n,m,:] = back_color + (color-back_color)*np.sinc(k*dist(n-screen_center[0],m-screen_center[1]))
                            else:
                                parche[n,m,:] = back_color
                            
                        if pos == right:
                            carpeta = "right/"
                            i_center = 0
                            j_center = int(size_y/2)
                            screen_center = [i_center, j_center]
                            if np.abs (m-j_center) <= np.abs(n-i_center):
                                parche[n,m,:] = back_color + (color-back_color)*np.sinc(k*dist(n-screen_center[0],m-screen_center[1]))
                            else:
                                parche[n,m,:] = back_color
                            
                        if pos == left:
                            carpeta = "left/"
                            i_center = size_x
                            j_center = int(size_y/2)
                            screen_center = [i_center, j_center]
                            if np.abs (m-j_center) <= np.abs(n-i_center):
                                parche[n,m,:] = back_color + (color-back_color)*np.sinc(k*dist(n-screen_center[0],m-screen_center[1]))
                            else:
                                parche[n,m,:] = back_color
                    
                parche = texturizador(parche,size_x,size_y)

                

                nombre_fondo = ''.join(map(lambda x: '_'+ str(x), back_color))

                nombre_estimulo = ''.join(map(lambda x: '_'+ str(x), color)) + ".npy"

                nombre_completo = comun + nombre_k + "/" + nombre_fondo + "/"+ nombre_estimulo

                

                os.mkdir(comun+nombre_k+ "/" + nombre_fondo)


                with open(nombre_completo, 'wb') as f:
                        
                    np.save(f, np.array(color))


                                
    return

tex_patches_creator(8,5,int(h/2),0.01)



        

                
        

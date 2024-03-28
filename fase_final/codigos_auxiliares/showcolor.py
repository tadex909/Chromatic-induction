#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 15:04:39 2019

@author: nicovattuone
"""

import rgb2sml
import numpy as np
import pygame

def colortopygame( color):  # This functions receives an array and returns a pygame Color object
    return pygame.Color( int(color[0]) %256  ,int(color[1]) %256,int(color[2]) %256)


"""Here I load the calibration file (see module rgb2sml) """
calib= rgb2sml.calibration(rgb2sml.openfile()) # Load the parameters of the calibration file
transf= rgb2sml.transformation(calib.A0(), calib.AMatrix(), calib.Gamma()) # Creates an object transf that has as methods all the needed transformations
Stimuli = transf.listS() # This list constains all the possible values to be used as stimuli
L=len(Stimuli)
Nb=8
backs= np.linspace(0.2*L,0.96*L, Nb)
#backs=[ 35 , 70 , 105 , 140, 180, 195, 210, 225, 240 ]


pygame.init()

screen = pygame.display.set_mode((400,400))


done= False
while not done:
     for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done= True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    done= True
           
     screen.fill( colortopygame(  Stimuli[int(backs[7]  ) ] ) )
   
     pygame.display.flip()

for i in range(Nb):
    screen.fill( colortopygame(  Stimuli[int(backs[i]  ) ] ) )
    pygame.image.save(screen,"./Backs/Back"+str(i)+".png")





pygame.quit()
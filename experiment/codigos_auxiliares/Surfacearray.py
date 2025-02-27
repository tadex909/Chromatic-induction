#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 12:46:36 2019

@author: nicovattuone
"""
import pygame
import numpy as np


    


def  convexvalues(rgb): # This functions receives rgb values and returns the matrix of vectors A and vector b of coordinates for the convex combination. rgb=np.dot(b,A)
    rgb=np.array(rgb)
    ref = np.round(rgb)
    delta = rgb - ref
    C=np.zeros((3,3))
    C[0] = ref + np.sign(delta[0]) *np.array([1,0,0])
    C[1] = ref + np.sign(delta[1]) *np.array([0,1,0])
    C[2] = ref + np.sign(delta[2]) *np.array([0,0,1])
    O =  ref + np.sign(delta) 
    delta = np.abs(delta)
    deltaO = delta.min()
    ind= list(delta).index(delta.min())
    if np.sum(delta) <1:
        return (  np.append([ref],C ,axis=0), np.append(1- np.sum(delta), delta )  )
    else:
        delta = delta - delta[ind]
        delta[ind] = deltaO
        C[ind] = O
        return( np.append([ref],C,axis=0), np.append(1- np.sum(delta), delta )  ) 
        
    
   
def surfarray(size , rgb ):
    C, prob = convexvalues(rgb)
    index= np.random.choice([0,1,2,3],p=prob, size= (size,size))
    return C[index]


pygame.init()
display = pygame.display.set_mode((350, 350))

rgb= [120.5,43.5,80.5]
size=350

c=surfarray(size,rgb)
            

surf = pygame.surfarray.make_surface(c) 
pygame.image.save(surf, "image2.jpg")
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    display.blit(surf, (0, 0))
    pygame.display.update()
pygame.quit()


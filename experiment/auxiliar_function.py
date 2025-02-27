from array import array
import pygame # Main module to develope the game
import random # Just a random module
from scipy.special import jv
import numpy as np
import os # Module to read and create directories
import rgb2sml # Module that contains the functions necessary to read the calibration file and make the transformations between rgb and sml
import Intro # Module that contains the start scene of the expriments and creates the file systems to save the data
import datetime # MOdule to print the date time of the experiment

def dist(i,j):
            distancia = float(np.sqrt((i)**2 +(j)**2))
            return distancia

def colortopygame( color):  # This functions receives an array and returns a pygame Color object
    return pygame.Color( int(color[0]) %256  ,int(color[1]) %256,int(color[2]) %256)

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
    print(np.append([ref],C,axis=0))
    if np.sum(delta) <1:
        return (  np.append([ref],C ,axis=0), np.append(1- np.sum(delta), delta )  )
    else:
        delta = delta - delta[ind]
        delta[ind] = deltaO
        C[ind] = O
        return( np.append([ref],C,axis=0), np.append(1- np.sum(delta), delta )  ) 
        
def surfarray(size , rgb ): # Creates the surface array
    C, prob = convexvalues(rgb)
   
    index= np.random.choice([0,1,2,3],p=prob, size= (int(size),int(size)))

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
    print(np.append([ref],C,axis=0))
    if np.sum(delta) <1:
        return (  np.append([ref],C ,axis=0), np.append(1- np.sum(delta), delta )  )
    else:
        delta = delta - delta[ind]
        delta[ind] = deltaO
        C[ind] = O
        return( np.append([ref],C,axis=0), np.append(1- np.sum(delta), delta )  ) 
        
def surfarray(size , rgb ): # Creates the surface array
    C, prob = convexvalues(rgb)
   
    index= np.random.choice([0,1,2,3],p=prob, size= (int(size),int(size)))
    
    

    return C[index]


def get_direction():
    # Get a single input line containing three values separated by spaces
    input_line = input("Enter the coordinates SML coordinates of the direction vector separated by spaces: ")

    # Split the input line into individual values based on spaces
    values = input_line.split()

    # Ensure that there are exactly three values
    if len(values) != 3:
        print("Please enter exactly three values separated by spaces.")
        return None
    else:
        # Create a list from the separated values
        my_list = [int(x) for x in values]
        return my_list

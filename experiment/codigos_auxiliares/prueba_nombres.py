
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

carpeta = "prueba_nombre/"

fondo = [123,234,123]


nombre_fondo = ''.join(map(lambda x: '_'+ str(x), fondo))

nombre_estimulo = ''.join(map(lambda x: '_'+ str(x), fondo)) + ".npy"

nombre_completo = carpeta + nombre_fondo + "/"+ nombre_estimulo


os.mkdir(carpeta+nombre_fondo)

with open(nombre_completo, 'wb') as f:
    np.save(f, np.array(estimulo))
with open(nombre_completo, 'rb') as f:
    a = np.load(f)  

print (a)
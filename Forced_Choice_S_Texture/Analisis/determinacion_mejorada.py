from matplotlib import pyplot as plt
import numpy as np
import math
import os
from scipy.optimize import root_scalar
#esta funcion saca los datos útiles del archivo

def fun_data_util(datos):
    datos_utiles = []
    cond = False
    for j in range(len(datos)):
    
        if cond == True:
         b = []
         for a in datos[j].strip().split('\t'):
             b.append(float(a))
         datos_utiles.append(b)
         
        if datos[j] == 'adapted ':
            cond = True
    datos_utiles = np.array(datos_utiles)
    return datos_utiles

class Estimador():
    def __init__(self, datos_utiles):
        fondo = datos_utiles[:,0]
        estimulo = datos_utiles[:,1]
        resultados = datos_utiles[:,2]
        delta_color = np.abs(fondo - estimulo)
        
        indices_aciertos = np.where(resultados == 1)
        indices_fallos = np.where(resultados == 0)
    
        self.c_aciertos = delta_color[indices_aciertos]
        self.c_fallos = delta_color[indices_fallos]
    
    def estimador(self, h):
        f = np.sum(self.c_fallos)-3/4*np.sum(np.exp(-self.c_aciertos/h)*self.c_aciertos/(1-3/4*np.exp(-self.c_aciertos/h)))
        return f
    
    def error_estimador(self, h):
        p_0 = 3/4*np.exp(-self.c_aciertos/h)
        p_1 = 1-3/4*np.exp(-self.c_aciertos/h)
        dlnP_dh = np.sum(p_0/p_1*(1-p_0/p_1)*self.c_aciertos**2/h**4)
        error = np.sqrt(1/(2*dlnP_dh))
        return error
    
    def h_0(self):
        h_0 = root_scalar(self.estimador, x0=0.01, x1=0.04).root
        return h_0
    
    def error_h_0(self):
        error_h_0 = self.error_estimador(self.h_0())
        return error_h_0


#f = open("Subjects\\tade\\tade5.dat", "r")

#datos = f.read().split("\n")
#datos = datos[:-1]


#datos_utiles = fun_data_util(datos)

#estimador = Estimador(datos_utiles)

#h_0 = estimador.h_0()
#error_h_0 = estimador.error_h_0()

#print("El valor es de: ",h_0," y su error es: ", error_h_0)

#Tadeo-----------------------
# k = 0.0125, h = 0.0208, error = 0.003
# k = 0.25, h = 0.0164, error = 0.0023
# k = 0.5, h = 0.0156, error = 0.0023
# k = 1, h = 0.02, error = 0.003

#Distancia de la mirada a la pantalla 48cm aprox

#k = 1 es  angulo = arctan (0.93/48) = 0.019 radianes y en grados es 1.1
#k*angulo = 7.015 entonces k es 7.015/1.1 = 6.4
#k = 0.5 es angulo = arctan(1.92/48) = 0.038 radianes y en grados es 2.2
#k*angulo = 7.015 entonces k es 7.015/2.2 = 3.2

#ancho de la pantalla, 34.5cm
#Ines------------------------
#k = 0.5, h = 0.038, error = 0.006
# k = 0.75, h = 0.041, error = 0.005
# k = 1, h = 0.024, error = 0.003
# k = 1.25, h = 0.053, error = 0.012
# k = 1.5, h = 0.065, error = 0.018
#distancia de la mirada a la pantalla 35cm aprox

#k = 1 es  angulo = arctan (0.93/35) = 0.026 radianes y en grados es 1.5
#k*angulo = 7.015 entonces k es 7.015/1.5 = 4.7

#Ines------------------------

k_tadeo = (6.4/7.015)*np.array([0.0125,0.25,0.5,1])
k_ines = (4.7/7.015)*np.array([0.5,0.75,1,1.25,1.5])
plt.figure(figsize=(8, 6), dpi=80)





#plt.plot(k_ines,[0.038,0.041,0.024,0.053,0.065], 'o') #Ines
#plt.errorbar(k_ines,[0.038,0.041,0.024,0.053,0.065], yerr = [0.006,0.005,0.003,0.012,0.018], label = "Likelihood exponencial",capsize = 5) #Ines


#plt.plot(k_ines,[0.0424,0.0421,0.0316,0.0503,0.0577], 'o') #Ines
#plt.errorbar(k_ines,[0.0424,0.0421,0.0316,0.0503,0.0577], yerr = [0.004,0.003,0.003,0.006,0.007],capsize = 5,color = '#60435F' ,label = "Sujeto 2") #Ines
plt.plot(k_tadeo,[0.0208,0.0164,0.0156,0.02], '-o') #Tadeo
plt.errorbar(k_tadeo,[0.0208,0.0164,0.0156,0.02], yerr = [0.003,0.0023,0.0023,0.003],capsize = 5,color = '#2282c4' ,label = "Sujeto 1") #Tadeo
plt.xlabel("Frecuencia espacial $k$ (1/°)", fontsize = 16)
plt.ylabel("Umbral de discriminación $h$",size = 16)
plt.legend(prop={'size': 16})
plt.tick_params(labelsize=16)
plt.grid(which = 'major')
plt.show()
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

def generador_estimador(datos_utiles):
    fondo = datos_utiles[:,0]
    estimulo = datos_utiles[:,1]
    resultados = datos_utiles[:,2]
    delta_color = np.abs(fondo - estimulo)
    
    indices_aciertos = np.where(resultados == 1)
    indices_fallos = np.where(resultados == 0)

    c_aciertos = delta_color[indices_aciertos]
    c_fallos = delta_color[indices_fallos]

    def estimador(h):
        salida = []
        for h_ in h:
            f = np.sum(c_fallos)-3/4*np.sum(np.exp(-c_aciertos/h_)*c_aciertos/(1-3/4*np.exp(-c_aciertos/h_)))
            salida.append(f)
        return np.array(salida)

    def error_estimador(h):
        salida = []
        for h_ in h:
            p_0 = 3/4*np.exp(-c_aciertos/h_)
            p_1 = 1-3/4*np.exp(-c_aciertos/h_)
            dlnP_dh = -np.sum(p_0/p_1*(1-p_0/p_1)*c_aciertos**2/h_**4)
            error = np.sqrt(1/(2*dlnP_dh))
            salida.append(error)
        return np.array(salida)
    
    return estimador, error_estimador

    






f = open("j0sqrt(k)\ines_1.txt", "r")

datos = f.read().split("\n")
datos = datos[:-1]


datos_utiles = fun_data_util(datos)

estimador, error = generador_estimador(datos_utiles)

h = np.linspace(0.001,0.1,5000)

f = estimador(h)

h_root = root_scalar(estimador,x0 = 0.1,x1 = 0.5)

error_h = error([h_root.root])

print(h_root.root)
print(error_h)

#plt.plot(h,f)
#plt.grid(True)
#plt.show()



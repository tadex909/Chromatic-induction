from matplotlib import pyplot as plt
import numpy as np
import math
import os
from scipy.optimize import root_scalar
from scipy.signal import find_peaks

np.random.seed()


#def generador_de_muestra(epsilon,h):
#    prob = 3/4*np.exp(-(epsilon/h))
#    muestra = np.random.choice([0,1], p = [prob,1-prob])
#    return muestra


def generador_de_muestra(epsilon,h):
    prob = 3/4*np.exp(-(epsilon/h)**2)
    muestra = np.random.choice([0,1], p = [prob,1-prob])
    return muestra




class Estimador():
    def __init__(self):
        self.c_aciertos = np.array([])
        self.c_fallos = np.array([])
        
            

    def actualizar(self,resultado,epsilon):
        if resultado:
            self.c_aciertos = np.append(self.c_aciertos,epsilon)
        else:
            self.c_fallos = np.append(self.c_fallos,epsilon)
    
    #def estimador(self, h):
    #    f = np.sum(self.c_fallos)-(3/4)*np.sum(np.exp(-self.c_aciertos/h)*self.c_aciertos/(1-3/4*np.exp(-self.c_aciertos/h)))
    #    return f
    
    def estimador(self,h):
        a_acierto = np.exp(-(self.c_aciertos/h)**2)
        a_fallo = np.exp(-(-self.c_fallos/h)**2)

        f = np.sum((a_acierto*self.c_aciertos**2)/(1-3/4*a_acierto)) - np.sum((a_fallo*self.c_fallos**2)/(3/4*a_fallo))

        return f 
    
    def estimador_integrado(self,h):
        f = np.sum(np.log(3/4)-(self.c_fallos/h)) + np.sum(np.log(1-3/4*np.exp(-self.c_aciertos/h)))
        return f
    
    
    def error_estimador(self, h):
        p_0 = 3/4*np.exp(-self.c_aciertos/h)
        p_1 = 1-3/4*np.exp(-self.c_aciertos/h)
        dlnP_dh = np.sum(p_0/p_1*(1-p_0/p_1)*self.c_aciertos**2/h**4)
        #print("valor de la suma es: ", dlnP_dh)
        error = np.sqrt(1/(2*dlnP_dh))
        #print("el error es ",error)
        return error
    
    def h_0(self):
        h_0 = root_scalar(self.estimador, x0=0.1, x1=0.3).root
        return h_0
    
    def h_1(self):
        x = np.linspace(0.1,1,10000)
        y = [self.estimador_integrado(x_) for x_ in x]
        i = find_peaks(y)[0]
        return x[i]

    

    
    def error_h_0(self):
        error_h_0 = self.error_estimador(self.h_0())
        return error_h_0
    
    def aciertos(self):
        return self.c_aciertos
    def fallos(self):
        return self.c_fallos
    


class metodo_uniforme():
    def __init__(self,h):
        self.h_real = h
        self.h_estimado = np.array([])
        self.error_h = np.array([])
        self.n_aciertos = 0
        self.n_errores = 0
        self.estimador = Estimador()


    def iterar(self,n):
        for i in range(n):
            epsilon = np.random.choice([0.2,0.4,0.6,0.8,1])
            muestra = generador_de_muestra(epsilon,self.h_real)
            if muestra:
                self.n_aciertos += 1
            else:
                self.n_errores += 1
            self.estimador.actualizar(muestra,epsilon)
            nuevo_valor = self.estimador.h_0()
            #if i < 10:
            #    nuevo_error = 0
            #else:
            nuevo_error = self.estimador.error_h_0()
            self.h_estimado = np.append(self.h_estimado,nuevo_valor)
            self.error_h = np.append(self.error_h,nuevo_error)


    def valores(self):
        return self.h_estimado
    
    def errores(self):
        return self.error_h
    
    def clear(self):
        self.h_estimado = np.array([])
        self.error_h = np.array([])
    
    def valor_estimador(self,h):
        return self.estimador.estimador_integrado(h)
    
    
    def aciertos_y_errores(self):
        return [self.estimador.aciertos(),self.estimador.fallos()]

        

h = 0.5

pasos = 2000

repeticiones = 2
valores1 = 0

errores1 = 0

metodo1 = metodo_uniforme(h)
datos = np.empty([repeticiones,pasos])
errores = np.empty([repeticiones,pasos])

for i in range(repeticiones):

    
    metodo1.iterar(pasos)

    datos[i,:] = metodo1.valores()

    valores1 = metodo1.valores()
    
    errores[i,:] = metodo1.errores()

    metodo1.clear()


np.save('Simulacion/datos_metodo_uniforme_h_0_5.npy',datos)
np.save('Simulacion/errores_metodo_uniforme_h_0_5.npy',errores)



a = np.load('Simulacion/datos_metodo_uniforme_h_0_5.npy')
b = np.load('Simulacion/errores_metodo_uniforme_h_0_5.npy')




#-----------------Gráfico del estimador para ambos métodos---------------------------
#x = np.linspace(0.1,1,1000)

#y_unif = [metodo1.valor_estimador(i) for i in x]


#plt.plot(x,y_unif,label = 'metodo uniforme')


#plt.axvline(x = h, color = 'k', lw = 1, label = 'valor real')
#plt.legend()

#plt.show()
#------------------------------------------------------------------------------------





#------------------Gráfico de la estimación en función del número de pasos------------
#plt.errorbar(np.arange(pasos),valores1, yerr=metodo1.errores(), label='metodo uniforme')
plt.plot(np.arange(pasos),valores1)

plt.axhline(y = h, color = 'k', lw = 1, label = 'valor real')

plt.ylim([0, 1])

plt.legend()

plt.show()
#-------------------------------------------------------------------------------------


#-------------Valores de amplitud de fallos y aciertos para cada método---------------

#aciertos1, fallos1 = metodo1.aciertos_y_errores()
#aciertos2, fallos2 = metodo2.aciertos_y_errores()

#resultados1 = np.array([])

#resultados2 = np.array([])
#resultados2 = np.append(resultados2,fallos2)
#resultados2 = np.append(resultados2,aciertos2)

#plt.scatter([0]*len(fallos2)+[1]*len(aciertos2),resultados2)
#plt.show()

    

    

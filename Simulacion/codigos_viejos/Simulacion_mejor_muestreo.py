from matplotlib import pyplot as plt
import numpy as np
import math
import os
from scipy.optimize import root_scalar
from scipy.signal import find_peaks

np.random.seed()

def generador_de_muestra(epsilon,h):
    prob = 3/4*np.exp(-epsilon/h)
    muestra = np.random.choice([0,1], p = [prob,1-prob])
    return muestra




class Estimador():
    def __init__(self, resultado,epsilon):
        
        if resultado:
            self.c_aciertos = np.array([epsilon])
            self.c_fallos = np.array([])
        else:
            self.c_aciertos = np.array([])
            self.c_fallos = np.array([epsilon])
            

    def actualizar(self,resultado,epsilon):
        if resultado:
            self.c_aciertos = np.append(self.c_aciertos,epsilon)
        else:
            self.c_fallos = np.append(self.c_fallos,epsilon)
    
    def estimador(self, h):
        f = np.sum(self.c_fallos)-(3/4)*np.sum(np.exp(-self.c_aciertos/h)*self.c_aciertos/(1-3/4*np.exp(-self.c_aciertos/h)))
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
        h_0 = root_scalar(self.estimador, x0=0.2, x1=0.3).root
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
        epsilon = np.random.choice([0.2,0.4,0.6,0.8,1])
        muestra = generador_de_muestra(epsilon,h)
        if muestra:
            self.n_aciertos = 1
        else:
            self.n_errores = 1
        self.estimador = Estimador(muestra,epsilon)
        self.h_estimado = np.append(self.h_estimado,self.estimador.h_0())
        self.error_h = np.append(self.error_h,0)

    def iterar(self,n):
        for i in range(n):
            epsilon = np.random.uniform(low = 0.2, high = 0.8)
            muestra = generador_de_muestra(epsilon,self.h_real)
            if muestra:
                self.n_aciertos += 1
            else:
                self.n_errores += 1
            self.estimador.actualizar(muestra,epsilon)
            nuevo_valor = self.estimador.h_0()
            if i < 10:
                nuevo_error = 0
            else:
                nuevo_error = self.estimador.error_h_0()
            self.h_estimado = np.append(self.h_estimado,nuevo_valor)
            self.error_h = np.append(self.error_h,nuevo_error)
            #print("el numero de aciertos es: ",self.n_aciertos)
            #print("el numero de errores es: ",self.n_errores)


    def valores(self):
        return self.h_estimado
    
    def errores(self):
        return self.error_h
    
    def clear(self):
        self.h_estimado = np.array([0])
        self.error_h = np.array([0])
    
    def valor_estimador(self,h):
        return self.estimador.estimador_integrado(h)
    
    
    def aciertos_y_errores(self):
        return [self.estimador.aciertos(),self.estimador.fallos()]


class metodo_actualizado():
    def __init__(self,h):
        self.h_real = h
        self.h_estimado = np.array([])
        self.error_h = np.array([])
        epsilon = np.random.choice([0.2,0.4,0.6,0.8,1])
        self.n_aciertos = 0
        self.n_errores = 0

        
        muestra = generador_de_muestra(epsilon,h)
        self.estimador = Estimador(muestra,epsilon)
        self.h_estimado = np.append(self.h_estimado,self.estimador.h_0())
        self.error_h = np.append(self.error_h,0)


    def valores(self):
        return self.h_estimado
    
    def errores(self):
        return self.error_h
    
    def iterar(self,n):
        for i in range(n):
            if i<10:
                
                epsilon = np.random.choice([0.2,0.4,0.6,0.8,1])
                error_nuevo = 0
            else:
                ruido = 0
                #ruido = np.random.normal(0,0.5/np.sqrt(n))
                epsilon = 1.*self.h_estimado[-1] + ruido
                error_nuevo = self.estimador.error_h_0()

            muestra = generador_de_muestra(epsilon,self.h_real)
            self.estimador.actualizar(muestra,epsilon)
            self.h_estimado = np.append(self.h_estimado,self.estimador.h_0())
            self.error_h = np.append(self.error_h,error_nuevo)

            

            #print("el numero de aciertos es ",self.n_aciertos)
            #print("el numero de errores es ",self.n_errores)

    def clear(self):
        self.h_estimado = np.array([0])
        self.error_h = np.array([0])

    
    def valor_estimador(self,h):
        return self.estimador.estimador_integrado(h)
    
    def aciertos_y_errores(self):
        return [self.estimador.aciertos(),self.estimador.fallos()]
            

h = 0.5

pasos = 100

repeticiones = 10
valores1 = 0
valores2 = 0
errores1 = 0
errores2 = 0
metodo1 = metodo_uniforme(h)
metodo2 = metodo_actualizado(h)

for _ in range(repeticiones):

    
    metodo1.iterar(pasos)
    valores1 += metodo1.valores()/repeticiones
    errores1 += metodo1.errores()/repeticiones
    metodo1.clear()

    metodo2.iterar(pasos)
    valores2 += metodo2.valores()/repeticiones
    errores2 += metodo2.valores()/repeticiones
    metodo2.clear()

#metodo1.graficar()
#metodo2.graficar()










#-----------------Gráfico del estimador para ambos métodos---------------------------
x = np.linspace(0.1,1,1000)

y_unif = [metodo1.valor_estimador(i) for i in x]

y_mejor = [metodo2.valor_estimador(i) for i in x]

plt.plot(x,y_unif,label = 'metodo uniforme')

plt.plot(x,y_mejor,label = 'metodo óptimo')

plt.axvline(x = h, color = 'k', lw = 1, label = 'valor real')

plt.show()
#------------------------------------------------------------------------------------





#------------------Gráfico de la estimación en función del número de pasos------------
plt.figure(figsize=(8, 6), dpi=80)
plt.plot(range(pasos+1),valores1, label='metodo uniforme')

plt.plot(range(pasos+1),valores2, label = 'metodo adaptativo')

plt.axhline(y = h, color = 'k', lw = 1, label = 'valor real')

plt.ylim([0, 1])

plt.ylabel("Umbral de discriminación $h$", fontsize = 15)
plt.xlabel("Paso",size = 15)
plt.legend(prop={'size': 12})
plt.tick_params(labelsize=15)
plt.grid(which = 'major')

plt.show()
#-------------------------------------------------------------------------------------


#-------------Valores de amplitud de fallos y aciertos para cada método---------------

aciertos1, fallos1 = metodo1.aciertos_y_errores()
aciertos2, fallos2 = metodo2.aciertos_y_errores()

resultados1 = np.array([])

resultados2 = np.array([])
resultados2 = np.append(resultados2,fallos2)
resultados2 = np.append(resultados2,aciertos2)

plt.scatter([0]*len(fallos2)+[1]*len(aciertos2),resultados2)
plt.show()

    

    

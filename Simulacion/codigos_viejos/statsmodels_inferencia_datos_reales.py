import numpy as np
import statsmodels.api as sm
from scipy.stats import bernoulli
from statsmodels.base.model import GenericLikelihoodModel


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

f = open("Forced_Choice_S_Texture/j0sqrt(k)/ines_1_5.txt", "r")

datos = f.read().split("\n")
datos = datos[:-1]


datos_utiles = fun_data_util(datos)

e = np.abs(datos_utiles[:,1] - datos_utiles[:,0])

data = datos_utiles[:,2]



# Generate data
#def generate_data(h, e):
#    p_0 = 3/4 * np.exp(-e/h)
#    p_1 = 1 - p_0
#    data = bernoulli.rvs(p=p_1, size=len(e))
#    return data

# Define custom model
class CustomModel(GenericLikelihoodModel):
    
    def __init__(self, endog, exog, **kwds):
        super().__init__(endog, exog, **kwds)
    
    def loglike(self, params):
        h = params[0]
        e = self.exog[:,0]
        p_0 = 3/4 * np.exp(-(e/h)**2)
        p_1 = 1 - p_0
        ll = self.endog*np.log(p_1) + (1-self.endog)*np.log(p_0)
        return ll.sum()

# Set true values of h and e
#h_true = 0.5
#e_true = np.random.choice([0.2, 0.4, 0.6, 0.8], size=100)

# Generate data
#data = generate_data(h_true, e_true)

# Fit model to data
exog = e.reshape(-1,1)
endog = data
model = CustomModel(endog, exog)
result = model.fit()

# Print results
print(result.summary())
#print("True value of h: ", h_true)
print("Estimated value of h: ", result.params[0])
import numpy as np
import statsmodels.api as sm
from scipy.stats import bernoulli
from statsmodels.base.model import GenericLikelihoodModel
from matplotlib import pyplot as plt

# Define custom model
class CustomModel(GenericLikelihoodModel):
    
    def __init__(self, endog, exog, p0, **kwds):
        self.p0 = p0
        super().__init__(endog, exog, **kwds)
    
    def loglike(self, params):
        h = params[0]
        e = self.exog[:,0]
        p_0 = self.p0(h, e)
        p_1 = 1 - p_0
        ll = self.endog*np.log(p_1) + (1-self.endog)*np.log(p_0)
        return ll.sum()

# Define function to generate data
def generate_data(h, e, p0):
    p_0 = p0(h, e)
    p_1 = 1 - p_0
    data = bernoulli.rvs(p=p_1, size=len(e))
    return data

# Set true values of h and e
h_true = 0.5
e_true = np.random.choice([0.2, 0.4, 0.6, 0.8], size=10)

# Define custom function for p_0
def p0_gaussian(h, e):
    return 3/4*np.exp(-(e/h)**2)

def p0_exp(h,e):
    return 3/4*np.exp(-e/h)

# Generate data
estimations_unif=[]
errors_unif = []


for i in range(50):
    data = generate_data(h_true, e_true, p0_exp)
    
    # Fit model to data
    exog = e_true.reshape(-1,1)
    endog = data
    model = CustomModel(endog, exog, p0_exp)
    result = model.fit(start_params = np.array([1]))
    
    # Save estimations and errors


    estimations_unif.append(result.params[0])
    errors_unif.append(result.bse[0])
    e_true = np.append(e_true,np.random.choice([0.2, 0.4, 0.6, 0.8]))


estimations = []
errors = []

for _ in range(50):
    data = generate_data(h_true, e_true, p0_exp)
        
    # Fit model to data
    exog = e_true.reshape(-1, 1)
    endog = data
    model = CustomModel(endog, exog, p0_exp)
    result = model.fit(start_params=np.array([1]))
        
    # Save estimations and errors
    e_true = np.append(e_true, 1.73 * result.params[0])
        
    estimations.append(result.params[0])
    errors.append(result.bse[0])


plt.figure(figsize=(8, 6), dpi=80)
#plt.plot(range(50)[::3],estimations_unif[::3], label = 'Muestreo uniforme',marker ='o')
plt.errorbar(range(50)[::3],estimations_unif[::3],errors_unif[::3], label= "Muestreo uniforme",capsize=3,marker ='o')

#plt.plot(range(50)[::3],estimations[::3], label = 'Muestreo actualizado',marker = 'o')
plt.errorbar(range(50)[::3],estimations[::3],errors[::3], label= "Mustreo actualizado",capsize=3,marker ='o')

plt.axhline(y = h_true, color = 'k', lw = 1, label = 'valor real')
plt.xlabel("Pasos", fontsize = 15)
plt.ylabel("Umbral de discriminación $h$",size = 15)
plt.legend(prop={'size': 15})
plt.tick_params(labelsize=15)
plt.grid(which = 'major')
plt.show()
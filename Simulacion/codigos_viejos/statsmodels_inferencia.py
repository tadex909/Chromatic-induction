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
e_true = np.random.choice([0.2, 0.4, 0.6, 0.8], size=50)

# Define custom function for p_0
def p0_gaussian(h, e):
    return 3/4*np.exp(-(e/h)**2)

def p0_exp(h,e):
    return 3/4*np.exp(-e/h)

# Generate data
estimations=[]
errors = []

estimations_square = []
errors_square = []

for i in range(1000):
    data = generate_data(h_true, e_true, p0_gaussian)
    
    # Fit model to data
    exog = e_true.reshape(-1,1)
    endog = data
    model = CustomModel(endog, exog, p0_gaussian)
    result = model.fit(start_params = np.array([1]))
    
    # Save estimations and errors
    estimations_square.append(result.params[0])
    errors_square.append(result.bse[0])

for i in range(1000):
    data = generate_data(h_true, e_true, p0_exp)
    
    # Fit model to data
    exog = e_true.reshape(-1,1)
    endog = data
    model = CustomModel(endog, exog, p0_exp)
    result = model.fit(start_params = np.array([1]))
    
    # Save estimations and errors
    estimations.append(result.params[0])
    errors.append(result.bse[0])

# Save estimations and errors to a file
#np.savetxt("estimations_uniforme.txt", np.array(estimations))
#np.savetxt("errors_uniforme.txt", np.array(errors))

# Print results of the last estimation
#print(result.summary())
#print("True value of h: ", h_true)
#print("Estimated value of h: ", result.params[0])


mean_exp = np.mean(estimations)
mean_gaussian = np.mean(estimations_square)

# Calculate the standard deviation (first method)
std_dev_exp = np.std(estimations)
std_dev_gaussian = np.std(estimations_square)


plt.hist(estimations_square, density=True,label = "Likelihood gaussiana")
plt.hist(estimations,alpha = 0.7, density=True, label= "Likelihood exponencial")
plt.axvline(x = h_true, color = 'k', lw = 1, label = 'valor real')
plt.xlabel("Umbral de discriminación $h$", fontsize = 15)
plt.ylabel("N",size = 15)
plt.legend(prop={'size': 12})
plt.tick_params(labelsize=15)
plt.grid(which = 'major')
plt.show()
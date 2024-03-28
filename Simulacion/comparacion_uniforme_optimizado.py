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
        e = self.exog[:, 0]
        p_0 = self.p0(h, e)
        p_1 = 1 - p_0
        ll = self.endog * np.log(p_1) + (1 - self.endog) * np.log(p_0)
        print(ll.sum())
        return ll.sum()

# Define function to generate data
def generate_data(h, e, p0):
    p_0 = p0(h, e)
    p_1 = 1 - p_0
    data = bernoulli.rvs(p=p_1, size=e.size)
    return data

# Set true values of h and e
h_true = 0.5
#e_true = np.random.choice([0.2, 0.4, 0.6, 0.8], size=10)

# Define custom function for p_0
def p0_custom(h, e):
    return 3 / 4 * np.exp(-(e / h)**2)
    #return 3 / 4 * np.exp(- np.abs((e / h)))
#alphas = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.25, 1.3, 1.38, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2]
#alphas = [1.3,1.35,1.45]
#alphas = [1.0, 1.1, 1.2, 1.25, 1.3, 1.32, 1.38, 1.45, 1.5, 1.6, 1.7]
#alphas = [0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.5, 1.6, 1.73, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6]
#num_iterations = 500

#estimations = []
#errors = []


alpha = 1.3174


n_reps = 10

time_steps = 35

h_mean_opt = np.zeros(time_steps)
errors_mean_opt = np.zeros(time_steps)
h_mean_unif = np.zeros(time_steps)
errors_mean_unif = np.zeros(time_steps)



for i in range(n_reps):

    h_optimal = []
    errors_optimal = []

    e_true = np.random.choice([0.2, 0.4, 0.6, 0.8, 1], size=15)
    data = generate_data(h_true, e_true, p0_custom)
    
    for _ in range(time_steps):
    
        # Fit model to data
        exog = e_true.reshape(-1, 1)
        endog = data
        model = CustomModel(endog, exog, p0_custom)
        result = model.fit(start_params=np.array([1]))
        
    #guardo la historia de cada iteración
        h_optimal = np.append(h_optimal,result.params[0])
        errors_optimal = np.append(errors_optimal,result.bse[0])
    # Save estimations and errors
        new_e = np.array(alpha * result.params[0])
        e_true = np.append(e_true,new_e)
        new_trial = generate_data(h_true,new_e, p0_custom)
        data = np.append(data,new_trial)

    h_mean_opt = h_mean_opt + h_optimal

    errors_mean_opt = errors_mean_opt + errors_optimal

h_optimal = h_mean_opt/n_reps

errors_optimal = errors_optimal/n_reps

data_optimal = np.column_stack((h_optimal, errors_optimal))

for i in range(n_reps):
    h_uniform = []
    errors_uniform = []

    e_true = np.random.choice([0.2, 0.4, 0.6, 0.8, 1], size=15)
    data = generate_data(h_true, e_true, p0_custom)

    for _ in range(time_steps):    
        
        # Fit model to data
        exog = e_true.reshape(-1, 1)
        endog = data
        model = CustomModel(endog, exog, p0_custom)
        result = model.fit(start_params=np.array([1]))
        
        #guardo la historia de cada iteración
        h_uniform = np.append(h_uniform,result.params[0])
        errors_uniform = np.append(errors_uniform,result.bse[0])
        # Save estimations and errors
        new_e = np.array(np.random.choice([0.2, 0.4, 0.6, 0.8, 1]))
        e_true = np.append(e_true,new_e)
        new_trial = generate_data(h_true,new_e, p0_custom)
        data = np.append(data,new_trial)

    h_mean_unif = h_mean_unif + h_uniform
    errors_mean_unif = errors_mean_unif + errors_uniform

h_uniform = h_mean_unif/n_reps
errors_optimal = errors_mean_unif/n_reps

plt.figure(figsize=(8, 6))  # Adjust the figure size

# Plotting the error bars
plt.errorbar(range(15, 15 + time_steps), h_uniform, errors_uniform, fmt='o', capsize=5, label='Método uniforme')
plt.errorbar(range(15, 15 + time_steps), h_optimal, errors_optimal, fmt='o', capsize=5, label='Método adaptativo')
plt.axhline(y = 0.5)
plt.xlabel('Número de trial', fontsize = 16)
plt.ylabel('Estimación del umbral de discriminación h', fontsize = 16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Adding grid and legend
plt.grid(True, alpha=0.7)
plt.legend(fontsize = 14)

# Show the plot
plt.show()

# Plot with improved aesthetics

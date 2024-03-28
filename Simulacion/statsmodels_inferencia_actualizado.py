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
    data = bernoulli.rvs(p=p_1, size=len(e))
    return data

# Set true values of h and e
h_true = 0.5
#e_true = np.random.choice([0.2, 0.4, 0.6, 0.8], size=10)

# Define custom function for p_0
def p0_custom(h, e):
    #return 3 / 4 * np.exp(-(e / h)**2)
    return 3 / 4 * np.exp(- np.abs((e / h)))
#alphas = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.25, 1.3, 1.38, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2]
#alphas = [1.3,1.35,1.45]
#alphas = [1.0, 1.1, 1.2, 1.25, 1.3, 1.32, 1.38, 1.45, 1.5, 1.6, 1.7]
alphas = [0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.5, 1.6, 1.73, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6]
num_iterations = 500

estimations = []
errors = []

for alpha in alphas:
    alpha_estimations = []
    alpha_errors = []
    
    for i in range(1400,1400+num_iterations):

        h_estimations = []
        h_errors = []

        e_true = np.random.choice([0.2, 0.4, 0.6, 0.8], size=15)

        for _ in range(35):

            data = generate_data(h_true, e_true, p0_custom)
        
        # Fit model to data
            exog = e_true.reshape(-1, 1)
            endog = data
            model = CustomModel(endog, exog, p0_custom)
            result = model.fit(start_params=np.array([1]))
        
        #guardo la historia de cada iteración
            h_estimations = np.append(h_estimations,result.params[0])
            h_errors = np.append(h_errors,result.bse[0])
        # Save estimations and errors
            e_true = np.append(e_true, alpha * result.params[0])

        
        h_data = np.column_stack((h_estimations, h_errors))

        filename = f"Simulacion/resultados_de_estimacion_lineal/h_estimations_alpha_{alpha}_iteration_{i}.txt"
        np.savetxt(filename, h_data, delimiter="\t")



        alpha_estimations.append(result.params[0])
        alpha_errors.append(result.bse[0])


    estimations.append(alpha_estimations)
    errors.append(alpha_errors)

# Save estimations and errors to files
np.savetxt("Simulacion/estimations_uniforme.txt", np.array(estimations))
np.savetxt("Simulacion/errors_uniforme.txt", np.array(errors))

# Print results of the last estimation for each alpha
for i, alpha in enumerate(alphas):
    print(f"Results for alpha = {alpha}")
    print(result.summary())
    print("True value of h: ", h_true)
    print("Estimated value of h: ", estimations[i][-1])
    print("------------------------")


errores_medio = np.std(np.std(estimations,axis=1))

print("La media de la estimación para cada valor de h es: ",np.mean(estimations,axis=1))
print("La desviación de la estimación para cada valor de h es: ",np.std(estimations,axis=1))
print("La media de los errores en la estimación para cada valor de h es:",np.mean(errors,axis = 1))


# Plot with improved aesthetics
plt.figure(figsize=(10, 6))  # Adjust the figure size

mean_estimations = np.mean(estimations, axis=1)
mean_errors = np.mean(errors, axis=1)

# Plotting the error bars
plt.errorbar(alphas, mean_estimations, mean_errors, fmt='o-', color='b', capsize=5, label='Estimations')
plt.xlabel('Alpha')
plt.ylabel('Mean Estimations')
plt.title('Mean Estimations vs. Alpha')
plt.xticks(alphas)  # Show all alphas on the x-axis

# Adding grid and legend
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()

# Plot with improved aesthetics
plt.figure(figsize=(8, 6))  # Adjust the figure size

plt.scatter(alphas, mean_errors, color='b', label = 'mean errors')
plt.xlabel('Alpha')
plt.ylabel('Mean Errors')
# Adding grid and legend
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()

a = 5
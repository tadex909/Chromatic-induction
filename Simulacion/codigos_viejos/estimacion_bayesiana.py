import numpy as np
import pymc as pm
import pytensor.tensor as pt
import arviz as az
# Define true values of h and e

if __name__ == '__main__':   
    h_true = 0.5
    e_true = np.random.choice([0.2, 0.4, 0.6, 0.8], size=100)

# Define function to generate data
    def generate_data(h, e):
        p_0 = 3/4 * np.exp(-e/h)
        p_1 = 1 - p_0
        data = np.random.binomial(n=1, p=p_1, size=len(e))
        return data

# Generate data
    data = generate_data(h_true, e_true)

# Define model
    with pm.Model() as model:
    # Priors
        h = pm.Uniform('h', lower=0.001, upper=0.2)
    
    # Likelihood
        p_0 = 3/4 * pt.exp(-e_true/h)
        p_1 = 1 - p_0
        y_obs = pm.Bernoulli('y_obs', p=p_1, observed=data)
    
    # Sample posterior
        trace = pm.sample(1000, chains=4, tune=1000)
    

# Print summary of results
        pm.summary(trace)
    # Access the posterior distribution of h
    print(az.summary(trace, kind="stats"))
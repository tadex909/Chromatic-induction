import numpy as np
import statsmodels.api as sm
from scipy.stats import bernoulli
from statsmodels.base.model import GenericLikelihoodModel
from matplotlib import pyplot as plt


def array_to_symmetric_matrix(arr):
    n = int(np.sqrt(2 * len(arr) + 0.25) - 0.5)
    if n * (n + 1) / 2 != len(arr):
        raise ValueError("Input array size does not match a symmetric matrix dimension")

    matrix = np.zeros((n, n))
    row, col = np.triu_indices(n)
    matrix[row, col] = matrix[col, row] = arr
    return matrix



# Define custom model
class CustomModel(GenericLikelihoodModel):
    
    def __init__(self, endog, exog, p0, **kwds):
        self.p0 = p0
        super().__init__(endog, exog, **kwds)
    
    def loglike(self, params):
        A = params
        print(A)
        e = self.exog
        p_0 = [self.p0(A, e_i) for e_i in e]
        p_1 = 1 - np.array(p_0)
        ll = self.endog * np.log(p_1) + (1 - self.endog) * np.log(p_0)
        ll = ll.sum()
        print(ll)
        return ll

# Define function to generate data
def generate_data(A, e, p0):
    
    
    p_0 = [p0(A, e_i) for e_i in e]
    p_1 = 1 - np.array(p_0)
    data = bernoulli.rvs(p = p_1)
    return data

# Set true values of h and e
A_true = [1, 2, 3, 1, 2, 3]
e_true = np.random.choice([0.05, 0.1, 0.15, 0.2], size = (10000,3))

# Define custom function for p_0
def p0_multi(A, e):
    A_matrix = np.reshape(array_to_symmetric_matrix(A),(3,3))
    exponente = -np.dot(e, np.dot(A_matrix, np.transpose(e)))
    prob = 3/4*np.exp(exponente)
    return prob

data = generate_data(A_true, e_true, p0_multi)

exog = e_true
endog = data
model = CustomModel(endog, exog, p0_multi)
result = model.fit(start_params=np.array([1, 2, 3, 1, 2, 3]))
print(result.params)


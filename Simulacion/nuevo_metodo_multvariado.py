import numpy as np
from scipy.optimize import minimize
from scipy.stats import bernoulli
from matplotlib import pyplot as plt
# Define the likelihood function


def p0_multi(A, e):
    exponente = -(A[0]*e[0]**2 + A[3]*e[1]**2 + A[5]*e[2]**2 + 2*A[1]*e[0]*e[1] + 2*A[2]*e[0]*e[2] + 2*A[4]*e[2]*e[1])
    prob = 3/4*np.exp(exponente)
    return prob


def log_likelihood(A, data):
    total_log_likelihood = 0
    for x, e in data:
        exponente = -(A[0]*(e[0])**2 + A[3]*(e[1])**2 + A[5]*(e[2])**2 + 2*A[1]*e[0]*e[1] + 2*A[2]*e[0]*e[2] + 2*A[4]*e[2]*e[1])
        p_0 = 3/4 * np.exp(exponente)
        p_1 = 1 - p_0
        total_log_likelihood += (1 - x) * np.log(p_0) + x * np.log(p_1)
    neg_log_likelihood = - total_log_likelihood
    
    return neg_log_likelihood



def graph_ll(z, data):
    total_log_likelihood = 0
    for x, e in data:
        exponente = -(z*(e[0])**2 + 1*(e[1])**2 + 1*(e[2])**2)
        p_0 = 3/4 * np.exp(exponente)
        p_1 = 1 - p_0
        total_log_likelihood += (1 - x) * np.log(p_0) + x * np.log(p_1)
    return total_log_likelihood




def generate_data(A, e, p0):
    
    
    p_0 = [p0(A, e_i) for e_i in e]
    p_1 = 1 - np.array(p_0)
    data = bernoulli.rvs(p = p_1)
    return data


def array_to_symmetric_matrix(arr):
    n = int(np.sqrt(2 * len(arr) + 0.25) - 0.5)
    if n * (n + 1) / 2 != len(arr):
        raise ValueError("Input array size does not match a symmetric matrix dimension")

    matrix = np.zeros((n, n))
    row, col = np.triu_indices(n)
    matrix[row, col] = matrix[col, row] = arr
    return matrix


A_true = [2, 1, 1, 2, -1, 3]

#e_true = np.random.choice([0.1, 0.3, 1.1, 1.4], size = (100,3))
e_true = np.random.normal(loc = 0, scale = 1, size = (100,3))
#import random

# Define the two possible options
#options = [[0.5, 0, 0], [0, 0.5, 0], [0, 0, 0.5], [1.5, 0, 0], [0, 1.5, 0], [0, 0, 1.5]]

# Number of samples to pick
#n = 1000  # Adjust as needed

# Generate "n" random samples
#e_true = [random.choice(options) for _ in range(n)]




data_0 = generate_data(A_true, e_true, p0_multi)


# Example data (replace with your actual data)
data = [(a, b) for a, b in zip(data_0, e_true)]


#x = np.linspace(0.1,4,1000)

#y = [graph_ll(z,data) for z in x]

#plt.plot(x,y)
#plt.show()
# Initial guess for A components (replace with your initial guess)
initial_A = [1.14, 0.74, 0.73, 1.99, -1.34, 3.17]
# Define bounds for A components (modify as needed)
#bounds = [(0, None), (0, None), (0, None), (0, None), (0, None), (0, None)]
# Find the MLE estimates for A using the data
result = minimize(log_likelihood, initial_A, args=(data,), method= "Nelder-Mead", options={'disp': True})
estimated_A = result.x



estimated_A = array_to_symmetric_matrix(estimated_A)

print("Estimated A:")
print(estimated_A.reshape((3, 3)))

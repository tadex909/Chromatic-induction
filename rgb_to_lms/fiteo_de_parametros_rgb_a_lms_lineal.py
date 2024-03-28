import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize


# Load the data from "integrals_output.txt"
data = np.loadtxt("rgb_to_lms/rgb_to_lms_R_G_B_L_M_S_data_final.txt", skiprows=1)  # Skip the header row
# Find the maximum value in the entire array
max_value = np.max(data)

# Divide the last three columns by the maximum value
data[:, 3:] /= max_value


# Split the data into independent variables (A, B, C) and dependent variables (X, Y, Z)
RGB = np.transpose(data[:, :3])  # First three columns as independent variables (A, B, C)
LMS = np.transpose(data[:, 3:])  # Last three columns as dependent variables (X, Y, Z)

#A_test = np.array([1,2,3,4,5,6,7,8,9]).reshape((3,3))
#gammas_test = np.array([1,2,3]).reshape((3,1))
#LMS = np.dot(A_test,RGB**gammas_test)



def model(params,x):
    A_flat, gammas, A0_flat  = params[:9], params[9:12], params[12:] 
    A = A_flat.reshape((3,3))
    gammas = gammas.reshape((3,1))
    A0 = A0_flat.reshape((3,1))
    new_x = (x ** gammas)
    y = np.dot(A,new_x) + A0
    return y

"""def model(params,x):
    A_flat, gammas  = params[:9], params[9:]
    A = A_flat.reshape((3,3))
    gammas = gammas.reshape((3,1))
    
    new_x = (x ** gammas)
    y = np.dot(A,new_x) 
    return y""" 

# Define the cost function to minimize
def cost_function(params):
    predicted = model(params,RGB)
    error = LMS - predicted
    return np.sum(error**2)



# Initial guess for parameters (A, gammas, A0)
initial_params = np.array([0.0058, 0.014, 0.0008, 0.0018, 0.0139, 0.001, 0.0005, 0.0002, 0.00376, 
                            2.23, 2.22, 2.37,
                            -5.4, -4.6, 4.3])


# Define bounds for exponents
#gammas_bound = [(2.5, 2.9), (2.6, 3), (0.2, 1)]  

# Define bounds for all parameters
#parameter_bounds = [(None,None)] * 9 + gammas_bound 


# Call minimize to find the best parameters
#result = minimize(cost_function, initial_params, bounds = parameter_bounds)
result = minimize(cost_function, initial_params)
# Extract the optimized parameters
optimized_params = result.x

# Extract the optimized values of a, C, b
A_optimized, gammas_optimized, A0_optimized = (
    optimized_params[:9], optimized_params[9:12], optimized_params[12:]
)

# Reshape the C matrix
A_optimized = A_optimized.reshape((3, 3))
A0_optimized = A0_optimized.reshape((3,1))

print("Optimized Parameters:")
print("A =", A_optimized)
print("gammas =", gammas_optimized)
print("A0 =", A0_optimized)

LMS_prediction = np.transpose(model(optimized_params,RGB))

# Add a fourth column to RGB_original containing S_error
RGB_LMS = np.hstack((data, LMS_prediction))

# Save the modified data to a text file
np.savetxt("rgb_to_lms/rgb_with_lms_and_prediction.txt", RGB_LMS, delimiter='\t', header="R\tG\tB\tL\tM\tS\tL_pred\tM_pred\tS_pred", comments='')

# Define the filename where you want to save the parameters
output_filename = "rgb_to_lms/optimized_parameters.txt"

# Create a header text to label the parameters
header_text = """Optimized Parameters:
A (Matrix):
"""

# Combine the parameters into a single array
all_optimized_params = np.concatenate((A_optimized.flatten(), gammas_optimized.flatten(), A0_optimized.flatten()))

# Save the header text and parameters to a text file
with open(output_filename, 'w') as file:
    file.write(header_text)
    # Save A as a formatted matrix
    file.write(np.array_str(A_optimized, precision=10, suppress_small=True))
    file.write("\n\n")
    # Label and save gammas and A0
    file.write("gammas = {}\n".format(gammas_optimized))
    file.write("A0 = {}\n".format(A0_optimized))

print("Optimized parameters saved to", output_filename)
import numpy as np 
from matplotlib import pyplot as plt
import os
from scipy.integrate import simps

#unidades en nm
lambda_L = 568.2 
lambda_M = 542.8
lambda_S = 442.1

sigma_L = 64.76
sigma_M = 52.8
sigma_S = 32.96

def L_curve(x):
    y = np.exp(-(x-lambda_L)**2/sigma_L**2)
    return y

def M_curve(x):
    y = np.exp(-(x-lambda_M)**2/sigma_M**2)
    return y

def S_curve(x):
    y = np.exp(-(x-lambda_S)**2/sigma_S**2)
    return y


directory = "Calibracion_pantalla/colores/segundo_intento/filtered_spectrums_1s/datos_utiles"

# Initialize arrays to store data
integrals_data = []

# Iterate through files in the directory
for filename in os.listdir(directory):
    if filename.startswith("spectrum") and filename.endswith("_s_filtered.txt"):
        # Extract the three numbers from the filename
        numbers = filename.split("_")[1:4]
        #code_arrays.append(numbers)
        
        # Read the content of the file
        filepath = os.path.join(directory, filename)
        data = np.loadtxt(filepath)
        wavelength = data[:,0]
        spectrum = data[:,1]

        l_integral = np.trapz(L_curve(wavelength)*spectrum, x=wavelength)/1000
        m_integral = np.trapz(M_curve(wavelength)*spectrum, x=wavelength)/1000
        s_integral = np.trapz(S_curve(wavelength)*spectrum, x=wavelength)/1000

        integrals_data.append(numbers + [l_integral, m_integral, s_integral])

# Convert integrals_data to a NumPy array
integrals_data = np.array(integrals_data)

# Save the data to a file
output_file = "rgb_to_lms/rgb_to_lms_R_G_B_L_M_S_data_final.txt"
header = "R G B L_integral M_integral S_integral"
np.savetxt(output_file, integrals_data, fmt="%s", header=header, comments="")

print("Data saved to", output_file)




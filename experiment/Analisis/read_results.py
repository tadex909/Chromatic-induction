import os
import numpy as np
import matplotlib.pyplot as plt

# Function to read data from a file
def read_results_file(file_path):
    data = np.loadtxt(file_path, skiprows=1)
    k_values_deg = data[:, 0]
    values = data[:, 1]
    k_errors = data[:, 2]
    errors = data[:,3]
    return k_values_deg, values, k_errors, errors

# Specify the directory where the results files are stored
results_dir = "Analisis/results"  # Change this to the directory where you saved the files

k_0_13 = []
k_error_0_13 = []
h_0_13 = []
h_error_0_13 = []

k_0_25 = []
k_error_0_25 = []
h_0_25 = []
h_error_0_25 = []

k_0_36 = []
k_error_0_36 = []
h_0_36 = []
h_error_0_36 = []

# Loop through files in the directory
for file_name in os.listdir(results_dir):
    if file_name.endswith(".txt"):
        file_path = os.path.join(results_dir, file_name)
        subject_name, sml_dir, _ = file_name.split("_")
        sml_dir = sml_dir[:-10]  # Remove "_results" from sml_dir

        # Read data from the file

        k_values_deg, values, k_errors, errors = read_results_file(file_path)

        if(file_name == "tade_[1, 0, 0]_results.txt"):
            k_0_13, h_0_13, k_error_0_13, h_error_0_13 = read_results_file(file_path)

        if(file_name == "tadebluer_[1, 0, 0]_results.txt"):
            k_0_25, h_0_25, k_error_0_25, h_error_0_25 = read_results_file(file_path)
        
        if(file_name == "tade3ers_[1, 0, 0]_results.txt"):
            k_0_36, h_0_36, k_error_0_36, h_error_0_36 = read_results_file(file_path)



        # Create the error plot
        #plt.figure(figsize=(9, 6.75))
        #plt.errorbar(k_values_deg, values, xerr= k_errors, yerr=errors, fmt='o', label=f'Valor del umbral, Dirección SML = {sml_dir}')

        # Set x and y labels with larger font size
        #plt.xlabel('Frecuencia espacial k (1/°)', fontsize=16)
        #plt.ylabel('Umbral de discriminación h', fontsize=16)
        #plt.xticks(fontsize=14)
        #plt.yticks(fontsize=14)
        #plt.legend(fontsize=16)
        #plt.grid(True)
        #plt.title(f'Results for {subject_name}, Direction {sml_dir}')
        #plt.show()


plt.figure(figsize=(9, 6.75))
plt.errorbar(k_0_13, h_0_13, yerr=h_error_0_13, xerr= k_error_0_13, fmt='o',label=f'S = 0.13')
plt.errorbar(k_0_25, h_0_25, yerr=h_error_0_25, xerr= k_error_0_25, fmt='o', label=f'S = 0.25')
plt.errorbar(k_0_36, h_0_36, yerr=h_error_0_36, xerr= k_error_0_36, fmt='o', label=f'S = 0.36')

# Set x and y labels with larger font size
plt.xlabel('Frecuencia espacial k (1/°)', fontsize=16)
plt.ylabel('Umbral de discriminación h', fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=14)
plt.grid(True)
plt.title(f'Modulación en la dirección S para diferentes fondos')
plt.show()

plt.figure(figsize=(9, 6.75))
plt.errorbar([0.13,0.25,0.36],[0.0031, 0.00556641, 0.00732422], yerr= [0.00036, 0.00035, 0.0005], fmt= 'o')
plt.xlabel('Coordenada S del fondo', fontsize=16)
plt.ylabel('Umbral de discriminación mínimo h', fontsize=16)
plt.plot(np.linspace(0,0.37,3),0.0215*np.linspace(0,0.37,3))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=14)
plt.grid(True)
plt.show()
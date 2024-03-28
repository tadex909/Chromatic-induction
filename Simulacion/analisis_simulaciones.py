import os
from collections import defaultdict
import numpy as np
from matplotlib import pyplot as plt
# Specify the directory containing your files
directory_path = "Simulacion/resultados_de_estimacion_cuadratica"

# Create a defaultdict to store data for each alpha
alpha_data = defaultdict(list)

# Loop through all files in the directory
for filename in os.listdir(directory_path):
    if filename.startswith("h_estimations_alpha_") and filename.endswith(".txt"):
        # Extract alpha from the filename
        alpha = float(filename.split("_")[3])
        
        # Read the file and extract the first column values
        file_path = os.path.join(directory_path, filename)
        data = np.loadtxt(file_path, usecols=0)
        
        # Add the data to the defaultdict for the corresponding alpha
        alpha_data[alpha].extend([data[-1]])

alphas = []
errors = []

# Calculate the mean for each alpha
for alpha, data in alpha_data.items():
    alphas = alphas + [alpha]
    error = np.abs(0.5-np.array(data))
    mean_error = np.mean(error)
    errors = errors + [mean_error]
    print(f"Alpha: {alpha}, Mean error: {mean_error}")

plt.figure(figsize=(8, 6))
plt.scatter(alphas, errors, marker='o', linestyle='-', color = '#48A9A6')
plt.xlabel(r'$\alpha$', fontsize=16)  # Adjust fontsize as needed
plt.ylabel('Error promedio', fontsize=16)  # Adjust fontsize as needed
#plt.title('Alphas vs Mean Errors', fontsize=16)  # Adjust fontsize as needed
plt.axvline(x = 1.3174, color = '#7189FF')
plt.grid(True, alpha=0.7)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.show()
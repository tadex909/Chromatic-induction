import os
import re
from ML_estimator import *
import matplotlib.pyplot as plt
from scipy.special import jv


# Function to read amplitudes and results from a file
def read_file(filename):
    amplitudes = []
    results = []

    with open(filename, 'r') as file:
        lines = file.readlines()
        found_adapted = False
        k_value = None

        for line in lines:
            if found_adapted:
                data = line.strip().split('\t')
                amplitudes.append(float(data[1]))
                results.append(float(data[2]))
            elif 'adapted' in line:
                found_adapted = True
            elif line.startswith('Spatial frequency k:'):
                k_value = float(line.split(':')[1].strip())

        return k_value, amplitudes, results

# Input subject name
subject_name = input("Enter the subject's name: ")

# Create a dictionary to store amplitudes and results for each value of k
data_dict = {}

# Navigate through folders and read files
folder_path = "Subjects/" + subject_name
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".dat"):
            file_path = os.path.join(root, file)
            k, amp, res = read_file(file_path)
            
            if k not in data_dict:
                data_dict[k] = {'amplitudes': [], 'results': []}
            
            data_dict[k]['amplitudes'].extend(amp)
            data_dict[k]['results'].extend(res)

# Print or use the data_dict as needed
for k, data in data_dict.items():
    print(f"Spatial frequency k = {k}:")
    print("Amplitudes:", data['amplitudes'])
    print("Results:", data['results'])


# Calculate values and errors for each k using the estimator function
k_values = []
values = []
errors = []

for k, data in data_dict.items():
    k_values.append(k)
    result = estimador(data['amplitudes'], data['results'])
    value = np.abs(result.params[0])
    error = result.bse[0]
    values.append(value)
    errors.append(error)

# Create the error plot
plt.errorbar(k_values, values, yerr=errors, fmt='o', label='Value with Error')
plt.xlabel('Spatial frequency k')
plt.ylabel('Value')
plt.title('Error Plot')
plt.legend()
plt.grid(True)
plt.show()

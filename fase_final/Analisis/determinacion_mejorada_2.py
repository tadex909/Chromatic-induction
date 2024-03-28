import os
import re
from ML_estimator import *
import matplotlib.pyplot as plt

dict_distances = {"toto" : 79, "gasti": 77, "martina" : 78, "martinal" : 78,
                    "tade" : 71, "tade_bluer": 71, "tade_3ers": 71, "tade_4tos" :71,
                    "herrmaestre" : 78, "bauti": 65, "ines": 46, "gaston_b" : 70}


save_dir = "Analisis/results"  # Change this to the desired directory
os.makedirs(save_dir, exist_ok=True)

# Function to read amplitudes and results from a file
def read_file(filename):
    amplitudes = []
    results = []
    k_value = None
    sml_direction = None

    with open(filename, 'r') as file:
        lines = file.readlines()
        found_adapted = False

        for line in lines:
            if found_adapted:
                data = line.strip().split('\t')
                amplitudes.append(float(data[1]))
                results.append(float(data[2]))
            elif 'adapted' in line:
                found_adapted = True
            elif line.startswith('Spatial frequency k:'):
                k_value = float(line.split(':')[1].strip())
            elif line.startswith('SML direction of change:'):
                sml_direction = line.split(':')[1].strip()

        return k_value, sml_direction, amplitudes, results


# Input subject name
subject_name = input("Enter the subject's name: ")

distance = dict_distances[subject_name]

# Create a nested dictionary to store amplitudes and results for each k and SML direction combination
data_dict = {}

# Create a set to store unique SML direction values
sml_directions = set()

# Navigate through folders and read files
folder_path = "Subjects/" + subject_name
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".dat"):
            file_path = os.path.join(root, file)
            k, sml_dir, amp, res = read_file(file_path)
            
            if k not in data_dict:
                data_dict[k] = {}
            if sml_dir not in data_dict[k]:
                data_dict[k][sml_dir] = {'amplitudes': [], 'results': []}
            
            data_dict[k][sml_dir]['amplitudes'].extend(amp)
            data_dict[k][sml_dir]['results'].extend(res)
            
            sml_directions.add(sml_dir)

# Create separate error plots for each k and SML direction combination
for sml_dir in sml_directions:
    k_values = []
    values = []
    errors = []
    
    for k, var_dict in data_dict.items():
        if sml_dir in var_dict:
            k_values.append(k)
            print("In the direction: ", sml_dir, " and for k = ", k, "we have ", len(var_dict[sml_dir]['results']), " data")
            result = estimador(var_dict[sml_dir]['amplitudes'], var_dict[sml_dir]['results'])
            value = np.abs(result.params[0])
            error = result.bse[0]
            values.append(value)
            errors.append(error)
    

    k_values_deg = np.pi/(180*np.arctan(1.4/distance))*np.array(k_values)
    #k_values_deg = k_values
    k_errors_deg = np.pi/180*1/np.arctan(1.4/distance)**2*(1/(1+(1.4/distance)**2))*1.4/distance**2*np.array(k_values)*2
    idx = np.argmin(values)
    h_min = values[idx]
    error_min = errors[idx]
    k_min = k_values_deg[idx]
    k_error_min = k_errors_deg[idx]
    print("El sujeto es: ", subject_name)
    print("Su dirección de varacion es: ", sml_dir)
    print("Su k óptimo es: ", k_min)
    print("error k: ", k_error_min) 
    print("Su h min es: ", h_min)
    print("Su h error es: ",error_min)

    # Create the error plot
    # Set the figure size
    plt.figure(figsize=(11, 8))
    
    #k_values = np.array(k_values)
    #values = np.array(values)
    #sorted_indices = np.argsort(k_values)
    #k_values = k_values[sorted_indices]
    #gavalues = values[sorted_indices]
    
    plt.errorbar(k_values_deg, values, yerr=errors, xerr= k_errors_deg, fmt='o', label=f'Valor del umbral, Dirección SML = {sml_dir}')
    # Set x and y labels with larger font size 
    plt.xlabel('Frecuencia espacial k (1/°)', fontsize=18)
    plt.ylabel('Umbral de discriminación h', fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    #plt.title(f'={sml_dir}')
    plt.legend(fontsize = 16)
    plt.grid(True)
    plt.show()

    file_name = f"{subject_name}_{sml_dir}_results.txt"
    file_path = os.path.join(save_dir, file_name)
    np.savetxt(file_path, np.column_stack((k_values_deg, values, k_errors_deg, errors)), header="k_values_deg values errors", comments="")

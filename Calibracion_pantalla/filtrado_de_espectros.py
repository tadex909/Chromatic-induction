import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
import scipy.signal as sg
import os
from pathlib import Path



def replace_large_values_with_average(arr, threshold_factor):
    modified_array = arr.copy()  # Create a copy to avoid modifying the original array
    
    for i in range(2, len(modified_array) - 2):
        if modified_array[i] > threshold_factor * modified_array[i - 1]:
            average = (modified_array[i - 2] + modified_array[i + 2]) / 2
            modified_array[i] = average
            
    return modified_array

def array_interpolado(*arrays):
    # Find the maximum value from the first element across all input arrays
    max_first = max(arr[0] for arr in arrays)
    
    # Find the minimum value from the last element across all input arrays
    min_last = min(arr[-1] for arr in arrays)

    # Create an empty list to store combined values
    combined_values = []
    
    # Iterate through each input array
    for arr in arrays:
        # Select values from the array that are within the range defined by max_first and min_last
        values = arr[(arr >= max_first) & (arr <= min_last)]
        # Extend the combined_values list with the selected values
        combined_values.extend(values)

    # Convert the combined_values list into a numpy array
    combined_array = np.array(combined_values)
    
    # Concatenate the maximum value, combined array, and minimum value
    unique_sorted_array = np.unique(np.concatenate(([max_first], combined_array, [min_last])))

    # Return the resulting array with unique and sorted values
    return unique_sorted_array


def bessel_filter(sig, cut_off, fs, tipo, orden=6):
    sos = sg.bessel(N=orden, Wn=cut_off, btype=tipo, fs=fs, output='sos')
    filtered = sg.sosfilt(sos, sig)
    return filtered


def filtrarBessel(x, f_samp, f_cut, orden):
	'''
    Definidas la frecuencia de muestreo, la frecuencia de corte y el orden del filtro, se filtra
    la señal x con un filtro butterworth/bessel pasabajos con las características indicadas
    '''
	nyq = 0.5 * f_samp
	cutoff = f_cut/nyq
	b, a = sg.bessel(orden, cutoff, btype='low', analog=False, output = 'ba')
	x_filt = sg.filtfilt(b, a, x)
	return x_filt


directory = "Calibracion_pantalla/Archivos_necesarios_para_la_calibracion/"

#transmitancia de la fibra
transmitancia_fibra = np.genfromtxt(directory + "optic_fiber_transmittance.csv", delimiter=',', skip_header=1)

#ganancia del espectrómetro
ganancia_espectrometro = np.genfromtxt(directory + "ganancia_relativa_espectrometro.txt", delimiter= '\t', skip_header = 1)


input_dir = "Calibracion_pantalla/colores/segundo_intento"


#espectro_negro_0_5s = np.genfromtxt(input_dir + "/spectrum_0_0_0_integration_0.5000_s.txt", delimiter= '\t', skip_header = 10)[:,1]
espectro_negro_1s = np.genfromtxt(input_dir + "/spectrum_0_0_0_integration_1.0000_s.txt", delimiter= '\t', skip_header = 10)[:,1]
#espectro_negro_2s = np.genfromtxt(input_dir + "/spectrum_0_0_0_integration_2.0000_s.txt", delimiter= '\t', skip_header = 10)[:,1]


# Path to the output directory
output_dir = "Calibracion_pantalla/colores/segundo_intento/filtered_spectrums_1s"

# Create the output directory if it doesn't exist
Path(output_dir).mkdir(exist_ok=True)


# Get a list of files in the input directory
file_list = [file for file in os.listdir(input_dir) if file.startswith("spectrum")]

file_list_0_5s = [file for file in file_list if '0.5000' in str(file)]
file_list_1s = [file for file in file_list if '1.0000' in str(file)]
file_list_2s = [file for file in file_list if '2.0000' in str(file)]

# Process each file
for file_name in file_list_1s:
    input_path = os.path.join(input_dir, file_name)
    output_path = os.path.join(output_dir, file_name.replace(".txt", "_filtered.txt"))

    rgb_code = file_name.split("_")[1:4]
    rgb_title = "RGB: ({}, {}, {})".format(*rgb_code)
    input_data = np.loadtxt(input_path, delimiter='\t', usecols=(0, 1))

    wavelength_espectro = input_data[10:,0]
    espectro_medido = input_data[10:,1]

    #a cada espectro le resto el fondo rgb = (0,0,0) y pongo en 0 los valores que puedan 
    #llegar a ser negativos

    y_sin_fondo = np.maximum(espectro_medido - espectro_negro_1s,0)
    y_sin_fondo[y_sin_fondo < 120] = 0
    y_sin_fondo = replace_large_values_with_average(y_sin_fondo,3)

    wavelength = array_interpolado(wavelength_espectro, transmitancia_fibra[:,0], ganancia_espectrometro[:,0])

    wavelength = wavelength[wavelength > 380]

    smallest_wavelength_diff = np.min(np.diff(wavelength))

    

    # Design a low-pass filter
    cutoff_frequency = 11000000  # Adjust this cutoff frequency as needed
    nyquist_frequency = 0.5 / smallest_wavelength_diff
    normal_cutoff = cutoff_frequency / nyquist_frequency
    b, a = sg.butter(4, normal_cutoff, btype='low', analog=False)

    

    f1 = interp1d(wavelength_espectro, y_sin_fondo, kind='linear')
    f2 = interp1d(transmitancia_fibra[:,0], transmitancia_fibra[:,1], kind='linear')
    f3 = interp1d(ganancia_espectrometro[:,0], ganancia_espectrometro[:,1], kind='linear')

    espectro_inter = f1(wavelength)
    fibra_inter = f2(wavelength)/100
    ganancia_inter = f3(wavelength)

    #plt.figure(figsize=(10, 6))
    #plt.plot(wavelength, fibra_inter, label='Transmitancia de Fibra Interpolada')
    #plt.plot(wavelength, ganancia_inter, label='Ganancia de Espectrómetro Interpolada')
    #plt.xlabel('Longitud de Onda')
    #plt.ylabel('Valor')
    #plt.title('Interpolación de Datos')
    #plt.legend()
    #plt.grid(True)
    #plt.show()

    espectro_real = (espectro_inter/fibra_inter)/ganancia_inter


    espectro_real = replace_large_values_with_average(espectro_real,5)
    # Apply the filter
    #espectro_filtrado_1 = sg.lfilter(b, a, espectro_real)
    espectro_filtrado_1 = sg.filtfilt(b, a, espectro_real)
    espectro_filtrado_1 = np.maximum(espectro_filtrado_1,0)



    plt.figure(figsize=(10, 6))
    plt.plot(wavelength, espectro_inter, label='Espectro medido a través de la fibra y espectrómetro')
    plt.plot(wavelength, espectro_real, label='Espectro real de la pantalla')
    plt.plot(wavelength, espectro_filtrado_1, label='Espectro filtrado con filtro pasabajos de la pantalla')
    plt.xlabel('Longitud de Onda')
    plt.ylabel('Valor')
    plt.title('Comparación de espectros '+ rgb_title)
    plt.legend()
    plt.grid(True)
  
    # Save the plot to the output directory with a unique name
    plot_filename = os.path.join(output_dir+"/images", f"spectrum_{rgb_code[0]}_{rgb_code[1]}_{rgb_code[2]}.png")
    plt.savefig(plot_filename)

    # Close the current plot to release resources and clear the figure
    plt.close()
    output_data = np.column_stack((wavelength, espectro_filtrado_1))
    np.savetxt(output_path, output_data, delimiter='\t', fmt='%.4f')


    
    
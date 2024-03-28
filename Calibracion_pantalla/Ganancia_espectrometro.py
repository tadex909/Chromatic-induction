import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
import scipy.signal as sg


def array_interpolado(*arrays):
    max_first = max(arr[0] for arr in arrays)
    min_last = min(arr[-1] for arr in arrays)

    combined_values = []
    for arr in arrays:
        values = arr[(arr >= max_first) & (arr <= min_last)]
        combined_values.extend(values)

    combined_array = np.array(combined_values)
    unique_sorted_array = np.unique(np.concatenate(([max_first], combined_array, [min_last])))

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



def rms_periodic(arr, period=5):
    """
    Calculates the RMS of each point of an array with a period of 'period' points.
    """
    half_period = period // 2
    
    # Pad the array to handle edge cases
    padded_arr = np.pad(arr, half_period, mode='edge')
    
    # Calculate the RMS for each point
    rms_arr = np.zeros_like(arr)
    for i in range(len(arr)):
        window = padded_arr[i:i+period]
        rms_arr[i] = np.sqrt(np.mean(np.square(window)))
    
    return rms_arr






directory = "Calibracion_pantalla/Archivos_necesarios_para_la_calibracion/"

#names: Wavelength	March Data	June Data
espectro_sol_ref = np.genfromtxt(directory + "espectro_solar_de_referencia.txt", delimiter='\t', skip_header=1)

#names: Wavelength	Real Intensity 
espectro_sol_medido_filtro = np.genfromtxt(directory + "Espectro_sol_con_filtro.txt", delimiter='\t', skip_header=1)

#names: Wavelength	Real Intensity
espectro_sol_medido_fibra = np.genfromtxt(directory + "Espectro_sol_con_fibra_y_filtro.txt", delimiter='\t', skip_header=1)

#names: wavelenght(nm)	transmitancia	error
transmitancia_filtro = np.genfromtxt(directory + "Transmitancia_filtro.txt", delimiter='\t', skip_header=1)

#names: wavelength(nm),Relative Transmission
transmitancia_fibra = np.genfromtxt(directory + "optic_fiber_transmittance.csv", delimiter=',', skip_header=1)


wavelength_1 = espectro_sol_ref[:,0]
wavelength_2 = espectro_sol_medido_filtro[:,0]
wavelength_3 =  transmitancia_filtro[:,0]
wavelength_4 = espectro_sol_medido_fibra[:,0]
wavelength_5 = transmitancia_fibra[:,0]


wavelength = array_interpolado(wavelength_1, wavelength_2, wavelength_3,wavelength_4,wavelength_5)

f1 = interp1d(wavelength_1, espectro_sol_ref[:,1], kind='linear')
f2 = interp1d(wavelength_2, espectro_sol_medido_filtro[:,1], kind='linear')
f3 = interp1d(wavelength_3, transmitancia_filtro[:,1], kind='linear')
f4 = interp1d(wavelength_4, espectro_sol_medido_fibra[:,1], kind='linear')
f5 = interp1d(wavelength_5, transmitancia_fibra[:,1], kind='linear')

espectro_sol_ref_interp = f1(wavelength)/np.amax(f1(wavelength))
espectro_sol_filtro_interp = f2(wavelength)
transmitancia_filtro_interp = f3(wavelength)
espectro_sol_fibra_interp = f4(wavelength)
transmitancia_fibra_interp = f5(wavelength)

espectro_sol_ocean = espectro_sol_filtro_interp/transmitancia_filtro_interp
espectro_sol_ocean = espectro_sol_ocean/np.amax(espectro_sol_ocean)

ganancia_espectrometro = espectro_sol_ocean/espectro_sol_ref_interp
espectro_sol_comparar = espectro_sol_fibra_interp/(transmitancia_fibra_interp/100)


plt.figure(figsize=(8, 6))
plt.plot(wavelength, espectro_sol_ref_interp, linewidth = 2, color = '#48A9A6')
#plt.title('Comparación de frecuencias espaciales \n óptimas en las direcciones S y L-M', fontsize = 14)
plt.xlabel('Longitud de onda (nm)', fontsize=16)
plt.ylabel('Espectro solar (cuentas normalizadas)', fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(wavelength, espectro_sol_ocean, linewidth = 2, color = '#7189FF')
#plt.title('Comparación de frecuencias espaciales \n óptimas en las direcciones S y L-M', fontsize = 14)
plt.xlabel('Longitud de onda (nm)', fontsize=16)
plt.ylabel('Espectro solar (cuentas normalizadas)', fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend()
plt.grid(True)
plt.show()




plt.plot(wavelength,espectro_sol_comparar/espectro_sol_filtro_interp)
#plt.plot(wavelength,espectro_sol_comparar, label = 'Espectro solar medido por el espectrómetro')
#plt.plot(wavelength,espectro_sol_filtro_interp)
plt.show()

#plt.plot(wavelength,espectro_sol_ocean, label = 'Espectro solar medido por el espectrómetro')
#plt.plot(wavelength,espectro_sol_ref_interp, label = 'Espectro solar de referencia')
#plt.xlabel("Wavelength [nm]")
#plt.ylabel("Intensity [ADC/μs]")
#plt.legend()
#plt.grid()
#plt.show()

ganancia_filtrada = rms_periodic(ganancia_espectrometro,80)/np.amax(rms_periodic(ganancia_espectrometro,80))

error = (np.abs(rms_periodic(ganancia_espectrometro,80)-ganancia_espectrometro))/np.amax(rms_periodic(ganancia_espectrometro,80))

output_data = np.column_stack((wavelength, ganancia_filtrada,error))

plt.errorbar(wavelength,ganancia_filtrada,error)
plt.show()

np.savetxt("Calibracion_pantalla/ganancia_relativa_espectrometro.txt", output_data, fmt='%.6f', delimiter='\t', header="Wavelength\tGanancia relativa\terror", comments='')

#ganancia_filtrada = filtrarBessel(ganancia_espectrometro, 1/10, 1.5,3)
plt.figure(figsize=(8, 6))
plt.plot(wavelength,ganancia_espectrometro, linewidth = 1, color = "#D81159", label = 'Ganancia antes de filtrar')
plt.plot(wavelength,ganancia_filtrada, linewidth = 2, color = '#7189FF', label = 'Ganancia filtrada')
#plt.title('Comparación de frecuencias espaciales \n óptimas en las direcciones S y L-M', fontsize = 14)
plt.xlabel('Longitud de onda (nm)', fontsize=16)
plt.ylabel('Ganancia', fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize = 14)
plt.grid(True)
plt.show()
#---------------------------------------------------------------------





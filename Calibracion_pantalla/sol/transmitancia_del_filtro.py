from matplotlib import pyplot as plt
import numpy as np
import scipy.signal as sg

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



datos_filtro = np.genfromtxt('sol/20230427/Thorlabs_NE20A_facil.dat', delimiter='\t', usecols=(1, 2, 3, 4))

nm_filtro = datos_filtro[:,0]

T = datos_filtro[:,2]

T_filtrado = filtrarBessel(T, 1/5, .03,7)

T_error_filtro = datos_filtro[:,3]

fig, ax = plt.subplots()

plt.plot(nm_filtro,T)
plt.plot(nm_filtro,(T_filtrado))
ax.set_xlabel('Longitud de onda (nm)')
ax.set_ylabel('Transmitancia')
plt.grid()
# Show the plot
plt.show()

residuo = np.abs(T_filtrado - T)

std_dev = rms_periodic(residuo,7)

plt.plot(nm_filtro,residuo, label = "residuo")

plt.plot(nm_filtro,std_dev, label = "desviación estándar")

plt.grid()

plt.show()

error_total = np.sqrt(std_dev**2+(0.01*T)**2)

#########################
fig, ax = plt.subplots()

# Plot the data with error bars
ax.errorbar(nm_filtro, T_filtrado, yerr=error_total, fmt='o', capsize=5)


# Set the x and y axis labels
ax.set_xlabel('Longitud de onda (nm)')
ax.set_ylabel('Transmitancia')
plt.grid()
# Show the plot
plt.show()

data_to_save = np.column_stack((nm_filtro, T_filtrado, error_total))
np.savetxt('sol/Transmitancia_filtro.txt', data_to_save, fmt='%.6f', delimiter='\t', header='wavelenght(nm)\ttransmitancia\terror', comments='')


########################



#datos_espectro_fibra = np.genfromtxt('sol/20230424/fibra_1_mejor.txt', delimiter='\t')


#nm = datos_espectro_fibra[:,0]

#cuentas = datos_espectro_fibra[:,1]

#plt.plot(nm,cuentas)

#plt.show()
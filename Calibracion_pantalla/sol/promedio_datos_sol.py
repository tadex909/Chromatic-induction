import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d


i_archivos = [str(i) for i in range(1,5)]
mean_intensity = 0
bg_intensity = 0
for i in i_archivos:
    with open("Calibracion_pantalla/sol/20230424/spectro_"+i+".txt", 'r') as file:
    # Skip over the header lines
        for line in file:
            if line.startswith('>>>>>Begin Processed Spectral Data<<<<<'):
                break

        wavelengths = []
        intensities = []
        for line in file:
        # Split the line into two columns and convert them to floats
            if line.startswith('>>>>>End Processed Spectral Data<<<<<'):
                break
            columns = line.split()
            wavelength = float(columns[0])
            intensity = float(columns[1])

        # Add the data to the list
            wavelengths.append(wavelength)
            intensities.append(intensity)
        mean_intensity += np.array(intensities)/4


with open("Calibracion_pantalla/sol/20230424/fondo_intermedio.txt", 'r') as file:
    # Skip over the header lines
        for line in file:
            if line.startswith('>>>>>Begin Processed Spectral Data<<<<<'):
                break

        wavelengths = []
        intensities = []
        for line in file:
        # Split the line into two columns and convert them to floats
            if line.startswith('>>>>>End Processed Spectral Data<<<<<'):
                break
            columns = line.split()
            wavelength = float(columns[0])
            intensity = float(columns[1])

        # Add the data to the list
            wavelengths.append(wavelength)
            intensities.append(intensity)
        bg_intensity += np.array(intensities)


real_intensity = np.maximum(mean_intensity - bg_intensity,0)

output_data = np.column_stack((wavelengths, real_intensity))
#np.savetxt("Calibracion_pantalla/Archivos_necesarios_para_la_calibracion/Espectro_sol_con_filtro.txt", output_data, fmt='%.6f', delimiter='\t', header="Wavelength\tReal Intensity", comments='Espectro del sol medido sin la fibra óptica y con filtro infrarrojo')

plt.plot(wavelengths,real_intensity)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensidad (ADC/s)')
plt.show()




datos_filtro = np.genfromtxt('Calibracion_pantalla/sol/20230427/Thorlabs_NE20A_facil.dat', delimiter='\t', usecols=(1, 2, 3, 4))

nm_filtro = datos_filtro[:,0]

T = datos_filtro[:,2]


f = interp1d(nm_filtro, T, kind='linear')
T_interp = f(wavelengths)

plt.plot(wavelengths,T_interp)
plt.show()
spm_intensity = real_intensity/T_interp

#plt.plot(nm_filtro,T)
#plt.plot(wavelengths,T_interp)
#plt.show()
#plt.plot(wavelengths,spm_intensity)

plt.plot(wavelengths,spm_intensity)
plt.xlabel("Longitud de onda", fontsize = 15)
plt.ylabel("Intensidad",size = 15)
plt.legend(prop={'size': 12})
plt.tick_params(labelsize=15)
plt.grid(which = 'major')
plt.show()
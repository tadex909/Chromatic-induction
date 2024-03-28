
import matplotlib.pyplot as plt
import numpy as np
# Read the file into a pandas DataFrame
file_path = 'Calibracion_pantalla/Espectro_referencia_sol.txt'

with open(file_path, 'r') as file:
    lines = file.readlines()

# Initialize lists to store data
wavelengths = []
march_data = []
june_data = []

# Parse the data
for line in lines[1:]:
    parts = line.strip().split('\t')
    wavelengths.append(int(parts[0]))
    march_data.append(float(parts[1].replace('E', 'e')))
    june_data.append(float(parts[2].replace('E', 'e')))

# Plotting
plt.figure(figsize=(10, 6))

# Plot the data
plt.plot(wavelengths, march_data, label='March 20th')
plt.plot(wavelengths, june_data, label='June 21st')

# Add labels and title
plt.xlabel('Wavelength (nm)')
plt.ylabel('Solar Noon Irradiance (mE cm^-2 d^-1 nm^-1)')
plt.title('Solar Noon Irradiance vs. Wavelength')

output_data = np.column_stack((wavelengths, march_data, june_data))
np.savetxt("Calibracion_pantalla/Archivos_necesarios_para_la_calibracion/espectro_solar_de_referencia.txt", output_data, fmt='%.6f', delimiter='\t', header="Wavelength\tMarch Data\tJune Data", comments='')

plt.legend()
plt.grid(True)
plt.show()
plt.plot(wavelengths,np.array(june_data)/np.array(march_data),label = 'Comparación')

# Show the plot
plt.grid(True)
plt.show()

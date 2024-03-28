import matplotlib.pyplot as plt
import numpy as np
import os

# RGB code and integration times to compare
red, green, blue = 0, 51, 51
integration_times_to_compare = [500000, 1000000, 2000000]

# Directory containing the saved spectrum files
spectrum_directory = "Calibracion_pantalla/colores"

# Read and filter the files
data_to_plot = []
for integration_time_micros in integration_times_to_compare:
    integration_time_seconds = integration_time_micros / 1e6
    #file_name = f"spectrum_{red}_{green}_{blue}_integration_{integration_time_seconds:.4f}_s.txt"
    file_name = f"spectrum_fondo_integration_{integration_time_seconds:.4f}_s.txt"
    file_path = os.path.join(spectrum_directory, file_name)
    
    if os.path.exists(file_path):
        data = np.genfromtxt(file_path, delimiter='\t')
        data_to_plot.append((integration_time_micros, data))

# Plot the data
for integration_time_micros, data in data_to_plot:
    wavelengths = data[:, 0]
    intensities = data[:, 1]
    
    # Ignore the first 2 points
    wavelengths = wavelengths[2:]
    intensities = intensities[2:]
    
    plt.plot(wavelengths, intensities, label=f"Integration Time: {integration_time_micros} μs")

plt.xlabel("Wavelength [nm]")
plt.ylabel("Intensity [ADC/μs]")
plt.title(f"Spectrum Comparison for RGB: {red}, {green}, {blue}")
plt.legend()
plt.grid()
plt.show()
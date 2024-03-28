import numpy as np
from seabreeze.spectrometers import Spectrometer


# Initialize seabreeze spectrometer
spec = Spectrometer.from_first_available()
integration_time_micros = 500000  # Set your desired integration time
spec.integration_time_micros(integration_time_micros)


# Function to read spectrum and return intensity data
def read_spectrum():
    spec.integration_time_micros(integration_time_micros)
    wavelengths = spec.wavelengths()
    intensities = np.zeros(wavelengths.size)
    number_of_samples = 3    
    for i in range(number_of_samples):
        intensities_i = spec.intensities()
        intensities = intensities + intensities_i 

    return wavelengths, intensities / number_of_samples

running = True




wavelengths, intensities = read_spectrum()


# Save spectrum to a separate text file named based on RGB and integration time
integration_time_seconds = integration_time_micros / 1e6
file_name = f"Calibracion_pantalla/colores/spectrum_fondo_integration_{integration_time_seconds:.4f}_s.txt"
with open(file_name, "w") as file:
    for wavelength, intensity in zip(wavelengths, intensities):
        file.write(f"{wavelength}\t{intensity}\n")


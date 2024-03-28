import pygame
import time
import numpy as np
from itertools import product
from seabreeze.spectrometers import Spectrometer

# Initialize Pygame
pygame.init()

# Initialize seabreeze spectrometer
spec = Spectrometer.from_first_available()
integration_time_micros = 1000000  # Set your desired integration time
spec.integration_time_micros(integration_time_micros)

# Screen dimensions
width = 800
height = 600

# Initialize screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Changing Colors")

# List of possible RGB values
#rgb_values = [0, 51, 102, 151, 204]

b_values = [0, 25, 60, 76, 125, 140, 176, 220, 254, 255]
r_values = [0]
g_values = [0]
# Generate all combinations of RGB values
#color_combinations = list(product(rgb_values, repeat=3))
color_combinations = list(product(r_values,g_values,b_values))
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
color_log = []


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for i in range(1,len(color_combinations)):
            
            r, g, b = color_combinations[i]
            # Clear the screen
o            screen.fill((0, 0, 0))

            # Set the background color
            screen.fill((r, g, b))
            
            # Read spectrum and log color and spectrum data
            wavelengths, intensities = read_spectrum()
            r, g, b = color_combinations[i-1]
            color_log.append((r, g, b, wavelengths, intensities))

            # Save spectrum to a separate text file named based on RGB and integration time
            integration_time_seconds = integration_time_micros / 1e6
            file_name = f"Calibracion_pantalla/colores/segundo_intento/spectrum_{r}_{g}_{b}_integration_{integration_time_seconds:.4f}_s.txt"
            with open(file_name, "w") as file:
                for wavelength, intensity in zip(wavelengths, intensities):
                    file.write(f"{wavelength}\t{intensity}\n")

            # Update the display
            pygame.display.flip()

            # Wait for a short interval
            time.sleep(1)

        # Quit Pygame
        pygame.quit()

import time
import numpy as np
from itertools import product
from seabreeze.spectrometers import Spectrometer
import matplotlib.pyplot as plt

# Initialize seabreeze spectrometer
spec = Spectrometer.from_first_available()
integration_time_micros = 1000000  # Set your desired integration time
spec.integration_time_micros(integration_time_micros)

# List of possible RGB values
rgb_values = [0, 51, 102, 153, 204]
r_values = [0, 25, 37, 51, 102, 153, 204, 254]
g_values = [0]
b_values = [0]

# Generate all combinations of RGB values
color_combinations = list(product(rgb_values, repeat=3))

color_log = []

for r, g, b in color_combinations:
    spec.integration_time_micros(integration_time_micros)
    wavelengths = spec.wavelengths()
    intensities = np.zeros(wavelengths.size)
    number_of_samples = 3    
    for i in range(number_of_samples):
        intensities_i = spec.intensities()
        intensities = intensities + intensities_i

    # Log color and spectrum data
    color_log.append((r, g, b, wavelengths, intensities))

    # Create a plot to visualize the color
    plt.figure()
    plt.title(f"Color: R={r}, G={g}, B={b}")
    plt.plot(wavelengths, intensities)
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Intensity")
    plt.savefig(f"spectrum_{r}_{g}_{b}.png")

    # Close the plot
    plt.close()

    # Wait for a short interval
    time.sleep(1)

# Quit Pygame
pygame.quit()

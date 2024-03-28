import pygame
import time
import math
import numpy as np
from seabreeze.spectrometers import Spectrometer

# Initialize Pygame
pygame.init()

# Initialize seabreeze spectrometer
spec = Spectrometer.from_first_available()
integration_time_micros = 40000  # Set your desired integration time
spec.integration_time_micros(integration_time_micros)

# Screen dimensions
width = 800
height = 600

# Number of colors to show
num_colors = 3

# Initialize screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Changing Colors")

# Function to calculate RGB values for equally distributed colors
def get_color(angle):
    red = math.sin(angle) * 127 + 128
    green = math.sin(angle + 2 * math.pi / 3) * 127 + 128
    blue = math.sin(angle + 4 * math.pi / 3) * 127 + 128
    return int(red), int(green), int(blue)

# Function to read spectrum and return intensity data
def read_spectrum():
    spec.integration_time_micros(integration_time_micros)
    wavelengths = spec.wavelengths()
    intensities = np.zeros(wavelengths.size)
    number_of_samples = 3    
    for i in range(number_of_samples):
    #print (i)
        intensities_i = spec.intensities()
    # plot(x,y)
        intensities = intensities + intensities_i 


    return wavelengths, intensities/number_of_samples

running = True
angle = 0
color_log = []

while running and len(color_log) < num_colors:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Get the RGB color values
    red, green, blue = get_color(angle)

    # Set the background color
    screen.fill((red, green, blue))

    # Read spectrum and log color and spectrum data
    wavelengths, intensities = read_spectrum()
    color_log.append((red, green, blue, wavelengths, intensities))

    # Save spectrum to a separate text file named based on RGB and integration time
    integration_time_seconds = integration_time_micros / 1e6
    file_name = f"Calibracion_pantalla/colores/spectrum_{red}_{green}_{blue}_integration_{integration_time_seconds:.4f}_s.txt"
    with open(file_name, "w") as file:
        for wavelength, intensity in zip(wavelengths, intensities):
            file.write(f"{wavelength}\t{intensity}\n")

    # Update the display
    pygame.display.flip()

    # Increment the angle for the next color
    angle += (2 * math.pi) / num_colors

    # Wait for 5 seconds
    time.sleep(1)

# Quit Pygame
pygame.quit()
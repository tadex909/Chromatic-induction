import matplotlib.pyplot as plt
import os
import re
import numpy as np

# Directory containing the saved spectrum files
spectrum_directory = "Calibracion_pantalla/colores"

# Get a list of all spectrum files in the directory
spectrum_files = [file for file in os.listdir(spectrum_directory) if file.startswith("spectrum")]

# Choose two spectrum files (you can adjust the indices as needed)
chosen_spectrum_files = spectrum_files

# Lists to store the data
wavelengths_list = []
intensities_list = []

# Read the intensity data from the chosen spectrum files
for chosen_spectrum_file in chosen_spectrum_files:
    wavelengths = []
    intensities = []
    with open(os.path.join(spectrum_directory, chosen_spectrum_file), "r") as file:
        for i, line in enumerate(file):
            if i >= 2:  # Skip the first two points
                wavelength, intensity = map(float, line.strip().split("\t"))
                wavelengths.append(wavelength)
                intensities.append(intensity)
    wavelengths_list.append(wavelengths)
    intensities_list.append(intensities)


plt.plot(wavelengths_list[3],intensities_list[3])
plt.show()

# Calculate the quotient of intensities
quotient_intensities = np.divide(intensities_list[0], intensities_list[8])

# Plot the quotient of intensities
plt.plot(wavelengths_list[0], quotient_intensities)
plt.xlabel("Wavelength [nm]")
plt.ylabel("Intensity Quotient")
plt.title("Spectrum Intensity Quotient")
plt.show()

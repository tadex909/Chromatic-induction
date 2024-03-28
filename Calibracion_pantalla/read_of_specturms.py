import matplotlib.pyplot as plt
import os
import re
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







# Directory containing the saved spectrum files
spectrum_directory = "Calibracion_pantalla/colores"

# Get a list of all spectrum files in the directory
spectrum_files = [file for file in os.listdir(spectrum_directory) if file.startswith("spectrum")]

# Choose two spectrum files (you can adjust the indices as needed)
chosen_spectrum_file1 = spectrum_files[3]
chosen_spectrum_file2 = spectrum_files[2]

# Extract RGB values from the file names using regular expressions
match1 = re.match(r"spectrum_(\d+)_(\d+)_(\d+).txt", chosen_spectrum_file1)
match2 = re.match(r"spectrum_(\d+)_(\d+)_(\d+).txt", chosen_spectrum_file2)
if match1 and match2:
    red1, green1, blue1 = map(int, match1.groups())
    red2, green2, blue2 = map(int, match2.groups())
else:
    print("File name format doesn't match expected pattern.")
    exit(1)

# Read the intensity data from the chosen spectrum files
wavelengths1 = []
intensities1 = []
with open(os.path.join(spectrum_directory, chosen_spectrum_file1), "r") as file:
    for i, line in enumerate(file):
        if i >= 2:  # Skip the first two points
            wavelength, intensity = map(float, line.strip().split("\t"))
            wavelengths1.append(wavelength)
            intensities1.append(intensity)

wavelengths2 = []
intensities2 = []
with open(os.path.join(spectrum_directory, chosen_spectrum_file2), "r") as file:
    for i, line in enumerate(file):
        if i >= 2:  # Skip the first two points
            wavelength, intensity = map(float, line.strip().split("\t"))
            wavelengths2.append(wavelength)
            intensities2.append(intensity)

# Apply the Bessel filter to the intensities
filter_intensity1 = filtrarBessel(intensities1, 1/5, .03, 7)
filter_intensity2 = filtrarBessel(intensities2, 1/5, .03, 7)

# Plot the data
#plt.plot(wavelengths1, intensities1, label=f"RGB: {red1}, {green1}, {blue1}")
plt.plot(wavelengths1, filter_intensity1, label=f"Filtered: RGB: {red1}, {green1}, {blue1}")
#plt.plot(wavelengths2, intensities2, label=f"RGB: {red2}, {green2}, {blue2}")
plt.plot(wavelengths2, filter_intensity2, label=f"Filtered: RGB: {red2}, {green2}, {blue2}")
plt.xlabel("Wavelength [nm]")
plt.ylabel("Intensity [ADC/μs]")
plt.title("Spectrum")
plt.legend()
plt.show()

# Plot the intensity data with RGB color name as label
#plt.plot(wavelengths, intensities)
#plt.xlabel("Wavelength [nm]")
#plt.ylabel("Intensity [ADC/μs]")
#plt.title("Spectrum")
#plt.text(0.5, 0.9, f"Color: ({red}, {green}, {blue})", horizontalalignment='center', verticalalignment='bottom', transform=plt.gca().transAxes)

#plt.show()
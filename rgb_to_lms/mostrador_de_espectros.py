import glob
import matplotlib.pyplot as plt
import numpy as np

# Directory containing the files
directory = "Calibracion_pantalla/colores/filtered_spectrums_1s/"

# Get a list of files matching the pattern
file_pattern = "spectrum_*_s_filtered.txt"
files = glob.glob(directory + file_pattern)

# Iterate through the files
for file in files:
    # Extract the numbers from the file name
    file_name = file.split("/")[-1]  # Extract the file name without path
    parts = file_name.split("_")
    numbers = [int(part) for part in parts if part.isdigit()]

    if len(numbers) != 3:
        continue  # Skip files that don't have exactly 3 numbers in the name

    # Load data from the file
    data = np.loadtxt(file)
    x = data[:, 0]
    y = data[:, 1]

    # Create a plot
    plt.figure()
    plt.plot(x, y)
    
    # Set the title based on the extracted numbers
    title = f"Spectrum: {numbers[0]}, {numbers[1]}, {numbers[2]}"
    plt.title(title)

    # Add x and y labels
    plt.xlabel("Wavelength")
    plt.ylabel("Intensity")

    # Add a grid
    plt.grid(True)

    # Customize plot settings as needed

    # Show or save the plot
    plt.show()  # Use plt.savefig("filename.png") to save the plot to a file if needed

import csv
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread('transmitancia_fibra/solo_grafico.png', cv2.IMREAD_GRAYSCALE)

# Apply thresholding to isolate data points
_, thresholded = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

# Find contours representing data points

point_index = np.where(np.array(thresholded) == 0)

x = point_index[1]/947*(1048-200) + 200

y = -point_index[0]/498*(109.5) + 109.5

# Find unique values of x and their indices
unique_x, unique_indices = np.unique(x, return_index=True)

# Calculate the mean y values corresponding to unique x values
mean_y_values = [np.mean(y[x == value]) for value in unique_x]

# Create a list of tuples combining unique_x and mean_y_values
data = list(zip(unique_x, mean_y_values))

# Specify the CSV file name
filename = "transmitancia_fibra/optic_fiber_transmittance.csv"

# Write data to the CSV file
with open(filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["x", "mean_y"])  # Write header
    csvwriter.writerows(data)  # Write data rows

print(f"Data saved to {filename}")





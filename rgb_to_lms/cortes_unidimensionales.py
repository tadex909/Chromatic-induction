import numpy as np
import matplotlib.pyplot as plt

# Load the data from "integrals_output.txt"
data = np.loadtxt("rgb_to_lms/rgb_to_lms_R_G_B_L_M_S_data.txt", skiprows=1)  # Skip the header row

filtered_data = data[(data[:, :3] != 0).sum(axis=1) <= 1]


non_zero_R = filtered_data[(filtered_data[:, 0] != 0) | ((filtered_data[:, 0] == 0) & (filtered_data[:, 1] == 0) & (filtered_data[:, 2] == 0))][:,[0,3,4,5]]
non_zero_G = filtered_data[(filtered_data[:, 1] != 0) | ((filtered_data[:, 0] == 0) & (filtered_data[:, 1] == 0) & (filtered_data[:, 2] == 0))][:,[1,3,4,5]]
non_zero_B = filtered_data[(filtered_data[:, 2] != 0) | ((filtered_data[:, 0] == 0) & (filtered_data[:, 1] == 0) & (filtered_data[:, 2] == 0))][:,[2,3,4,5]]

sorted_indices = np.argsort(non_zero_R[:, 0])
non_zero_R = np.log(non_zero_R[sorted_indices])

sorted_indices = np.argsort(non_zero_G[:, 0])
non_zero_G = np.log(non_zero_G[sorted_indices])

sorted_indices = np.argsort(non_zero_B[:, 0])
non_zero_B = np.log(non_zero_B[sorted_indices])

#--------------------------------------------------------------------

plt.plot(non_zero_R[:,0], non_zero_R[:,1],label = 'L en función de R')
plt.plot(non_zero_R[:,0], non_zero_R[:,2],label = 'M en función de R')
plt.plot(non_zero_R[:,0], non_zero_R[:,3],label = 'S en función de R')
plt.grid(which = 'Major')
plt.legend()
plt.show()

plt.plot(non_zero_G[:,0], non_zero_G[:,1],label = 'L en función de G')
plt.plot(non_zero_G[:,0], non_zero_G[:,2],label = 'M en función de G')
plt.plot(non_zero_G[:,0], non_zero_G[:,3],label = 'S en función de G')
plt.grid(which = 'Major')
plt.legend()
plt.show()

plt.plot(non_zero_B[:,0], non_zero_B[:,1],label = 'L en función de B')
plt.plot(non_zero_B[:,0], non_zero_B[:,2],label = 'M en función de B')
plt.plot(non_zero_B[:,0], non_zero_B[:,3],label = 'S en función de B')
plt.grid(which = 'Major')
plt.legend()
plt.show()
"""
#---------------------------------------------------------------------
# Create a figure with subplots arranged in a 3x3 grid
fig, axs = plt.subplots(3, 3, figsize=(15, 12))

# Define the data and labels for each group of plots
data_sets = [non_zero_R, non_zero_G, non_zero_B]
color_labels = ['R', 'G', 'B']

# Loop through each group and plot the data in each subplot
for i, (data, color_label) in enumerate(zip(data_sets, color_labels)):
    for j in range(3):
        axs[i, j].plot(data[:, 0], data[:, j + 1], label=f'{["L", "M", "S"][j]} en función de {color_label}')
        axs[i, j].grid(which='major')
        axs[i, j].legend()

# Adjust spacing between subplots
plt.tight_layout()

# Display the combined figure
plt.show()


# Create a figure with subplots arranged in a 3x3 grid
fig, axs = plt.subplots(3, 3, figsize=(15, 12))
data_sets = [np.log(non_zero_R), np.log(non_zero_G), np.log(non_zero_B)]
color_labels = ['R', 'G', 'B']

# Loop through each group and plot the data in each subplot
for i, (data, color_label) in enumerate(zip(data_sets, color_labels)):
    for j in range(3):
        axs[i, j].plot(data[:, 0], data[:, j + 1], label=f'{["L", "M", "S"][j]} en función de {color_label}')
        axs[i, j].grid(which='major')
        axs[i, j].legend()

# Adjust spacing between subplots
plt.tight_layout()

# Display the combined figure
plt.show()

"""
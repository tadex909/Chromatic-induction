import numpy as np
import matplotlib.pyplot as plt

# Define the range of x values
x = np.linspace(0, 3, 100)  # Adjust the range as needed

# Define the functions
y1 = (3/4) * np.exp(-x**2)
y2 = 1 - (3/4) * np.exp(-x**2)

# Create the plot
plt.figure(figsize=(8, 6))
plt.plot(x, y1, color='#2081C3', linewidth=3)
plt.plot(x, y2, color='#60435F', linewidth=3)

plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()

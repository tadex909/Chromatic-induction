import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf

# Define the error function (cumulative distribution function of the normal distribution)
def psychometric_curve(x, slope, midpoint):
    return 0.5 * (1 + erf(slope * (x - midpoint)))

# Generate x values
x_values = np.linspace(0, 10, 100)

# Define parameters for the psychometric curves
slope_vowel = 1.7  # Bigger slope
midpoint_vowel = 5
slope_animal = 0.5  # Smaller slope
midpoint_animal = 5

# Compute y values for each curve
y_values_vowel = psychometric_curve(x_values, slope_vowel, midpoint_vowel)
y_values_animal = psychometric_curve(x_values, slope_animal, midpoint_animal)

# Plot the curves with thicker lines
plt.plot(x_values, y_values_vowel, label='Vowel perception', linewidth=2)
plt.plot(x_values, y_values_animal, label='Animal vocalization', linewidth=2)

# Add labels and legend with bigger font
plt.xlabel('F1 or F2', fontsize=14)
plt.ylabel('Probability of answering /u/', fontsize=14)
plt.title('Psychometric Curves', fontsize=16)
plt.legend(fontsize=12)

# Hide x ticks
plt.xticks([])

# Show the plot
plt.grid(True)
plt.show()

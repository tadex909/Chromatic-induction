import numpy as np
import matplotlib.pyplot as plt

def calculate_max_frequency(mu, sigma_values):
    max_frequencies = []

    for sigma in sigma_values:
        x = np.linspace(mu - 10000 * sigma, mu + 10000 * sigma, 1000000)
        y = np.exp(-(x - mu)**2 / sigma**2)
        f = y - 4 * np.gradient(np.gradient(y, x), x)

        # Subtract the mean value
        f -= np.mean(f)

        # Compute the Fourier transform
        fourier_transform = np.fft.fft(f)
        frequencies = 2 * np.pi * np.fft.fftfreq(len(f), d=(x[1] - x[0]))
        amplitude_spectrum = np.abs(fourier_transform)

        # Find the frequency corresponding to the maximum amplitude
        max_frequency = frequencies[np.argmax(amplitude_spectrum)]
        max_frequencies.append(max_frequency)

    return max_frequencies

def plot_max_frequency(sigma_values, max_frequencies):
    plt.plot(sigma_values, max_frequencies, marker='o')
    plt.xlabel('Sigma', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Frequency Corresponding to Maximum Amplitude in Fourier Transform', fontsize=14)
    plt.grid(True)
    plt.show()

# Define the range of sigma values
sigma_values = np.linspace(0.1, 5, 100)

# Calculate the frequency corresponding to the maximum amplitude for each sigma
max_frequencies = np.abs(calculate_max_frequency(0, sigma_values))

# Plot the results
plot_max_frequency(sigma_values, max_frequencies)
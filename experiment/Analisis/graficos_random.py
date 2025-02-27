import numpy as np
import matplotlib.pyplot as plt

def plot_gaussian(sigma):
    mu = 0
    x = np.linspace(mu - 10000 * sigma, mu + 10000 * sigma, 10000000)
    y = np.exp(-(x - mu)**2 / sigma**2)
    f = y - 4 * np.gradient(np.gradient(y, x), x)
    
    # Subtract the mean value
    f -= np.mean(f)
    f_cos = np.cos(0.88 * x)
    
    # Plot the original function
    plt.figure(figsize=(14, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(x[np.where(np.abs(x) < 20)], f[np.where(np.abs(x) < 20)], linewidth=5)
    plt.plot(x[np.where(np.abs(x) < 20)], f_cos[np.where(np.abs(x) < 20)], linestyle='--')
    plt.xlabel('x', fontsize=12)
    plt.ylabel('f(x)', fontsize=12)
    plt.title('Original Function (Mean Subtracted)', fontsize=14)
    plt.legend()
    
    # Set the limits for the x and y axes
    plt.xlim([-7, 7])  # Adjust the values as needed
    plt.ylim([-1.5, 3.5])    # Adjust the values as needed

    # Compute and plot the Fourier transform
    fourier_transform = np.fft.fft(f)
    frequencies = 2 * np.pi * np.fft.fftfreq(len(f), d=(x[1] - x[0]))
    amplitude_spectrum = np.abs(fourier_transform)
    
    plt.subplot(1, 2, 2)
    plt.plot(frequencies[np.where(np.abs(frequencies) < 10)], amplitude_spectrum[np.where(np.abs(frequencies) < 10)])
    plt.xlabel('Frequency', fontsize=12)
    plt.ylabel('Amplitude', fontsize=12)
    plt.title('Fourier Transform', fontsize=14)
    
    # Add a vertical line at the frequency with maximum amplitude
    max_frequency_index = np.argmax(amplitude_spectrum)
    max_frequency = np.abs(frequencies[max_frequency_index])
    plt.axvline(x=max_frequency, color='r', linestyle='--')
    
    # Set the limits for the x and y axes
    plt.xlim([0, 5])  # Adjust the values as needed
    plt.ylim([0, 2000]) 

    plt.legend()
    plt.tight_layout()
    plt.show()

# Plot the Gaussian with mean subtracted and its Fourier transform
plot_gaussian(2)

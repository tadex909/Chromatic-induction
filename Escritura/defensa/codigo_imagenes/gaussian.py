import numpy as np
import matplotlib.pyplot as plt

def plot_gaussian(mu, sigma):
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    y = np.exp(-(x - mu)**2 / (2 * sigma**2)) / (sigma * np.sqrt(2 * np.pi))
    f = y + np.gradient(np.gradient(y, x), x)
    plt.plot(x, f)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Función f(x)')
    plt.grid(True)
    plt.show()

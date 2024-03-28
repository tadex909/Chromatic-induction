import numpy as np
from scipy.special import jv
from matplotlib import pyplot as plt

x = np.linspace(0,2.5,2000)

#f = jv(0,x)
p_0 = 3/4*np.exp(-x**2)
p_1 = 1- p_0

plt.figure(figsize = (8,6))
plt.plot(x,p_0, linewidth = 3)
plt.plot(x,p_1, linewidth = 3)
plt.grid(visible=True)
plt.show()
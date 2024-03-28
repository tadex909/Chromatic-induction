import numpy as np
from scipy.special import jv
from matplotlib import pyplot as plt

x = np.linspace(0,22,2000)

f = jv(0,x)

plt.plot(x,f)
plt.grid(visible=True)
plt.show()
#import numpy as np
#from numpy import abs, cos, sin, sqrt, arcsin
#import matplotlib.pyplot as plt


#x = np.linspace(-8.5,8.5,12000)

#y = np.exp(-(x/3)**2) - 1/2*np.exp(-(x/4)**2)

#plt.figure(figsize=(8, 6), dpi=80)
#plt.plot(x,y, linewidth = '4', color = '#60435F')
#plt.ylabel("p(x = 0| $h = 1$, $\epsilon$)", fontsize = 15)
#plt.xlabel("$\epsilon$",size = 15)
#plt.legend(prop={'size': 12})
#plt.tick_params(labelsize=15)
#plt.grid(which = 'major')
#plt.show()
import matplotlib.pyplot as plt

# Your data
data = [2.05, 4.12, 1.88, 4.6, 5.44, 9.29, 3.38, 7.38, 3.38, 4.58, 9.99, 2.61, 4.75, 3.25, 7.4, 6.95, 7.51, 5.85, 3.56, 4.26, 8.13, 6.33, 9.07, 6.44, 1.13, 2, 7.08, 4.86, 3.19, 2.52, 3.89, 5.75, 6.88, 7.18, 5.95, 5.07, 3.21, 7.57, 6.81, 3.95, 2.73, 3.01, 6.76, 5.22, 3.9, 4.27, 5.4, 7.05, 1.69, 5.26, 8.3, 6.2, 2.68, 3.21, 6.01, 8.1]

# Define custom bin edges
bin_edges = [0, 0.5 ,1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5 ,5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]

# Create a histogram with custom bin edges
plt.hist(data, bins=bin_edges, edgecolor='black')
plt.title('Histogram')
plt.xlabel('Value')
plt.ylabel('Frequency')

# Show the histogram
plt.show()


#!/usr/bin/env python
# coding: utf-8

# In[ ]:
from IPython import get_ipython

get_ipython().run_line_magic('pylab', 'inline')
from numpy import *
from matplotlib import pyplot as plt
from seabreeze.spectrometers import Spectrometer

#
# conda install -c conda-forge seabreeze
#
spec = Spectrometer.from_first_available()


# In[ ]:


integration_time_micros = 10e3

spec.integration_time_micros(integration_time_micros)

n = 40

x  = spec.wavelengths()
ys = zeros(x.size)

for i in range(n):
    #print (i)
    y = spec.intensities()
    # plot(x,y)
    ys = ys + y 
    
ys = ys/(n*integration_time_micros) 

plt.plot(x[30:],ys[30:]/n)
plt.xlabel("Wavelength [nm]")
plt.ylabel("Intensity [ADC/\mu s]")

#xlim(340,350)


# In[ ]:


plt.semilogy(x[30:],ys[30:]/n)

plt.xlabel("Wavelength [nm]")
plt.ylabel("Intensity [ADC/\mu s]")


# In[ ]:


savetxt('rojo_con_nombre.out.out', 
        array([x,ys]).T, 
        header="spectrum \n 1: wavelengh [nm] \n 2: intensity [ADC /micro_seg] \n", 
        footer="end")


# %%

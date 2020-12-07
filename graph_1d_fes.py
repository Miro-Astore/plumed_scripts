import numpy as np 
import matplotlib.pyplot as plt 

data = np.loadtxt('fes.dat')
plt.plot(data[:,0],data[:,1])
plt.show()

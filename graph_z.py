import numpy as np 
import matplotlib.pyplot as plt 

COLVAR_FILES=['repl00/COLVAR.0','repl01/COLVAR.1','repl02/COLVAR.2','repl03/COLVAR.3']

for i in range(len(COLVAR_FILES)):
    data = np.loadtxt(COLVAR_FILES[i])
    plt.semilogy(data[:,0],data[:,-2])
#plt.ylim([-20, 0])
plt.ylim([0, 1])
plt.show()

import numpy as np
import matplotlib.pyplot as plt
import re

#need the number of bins in each axis of the grid.
data=np.loadtxt('GRIDS')
pattern=re.compile('nbins')
grid_dims=[0,0]
ind=0
for i, line in enumerate(open('GRIDS')):
    for match in re.finditer(pattern, line):
            #print ('Found on line %s: %s' % (i+1, match.group()))
            #print(line)
            if re.search('nbins',str(line)):
                nbin_line=line
                nbin_line=nbin_line.split(' ') 
                nbins=np.int(nbin_line[-1])
                grid_dims[ind]=nbins
                ind=ind+1
print(grid_dims)


x,y,z=(data[:,0],data[:,1],data[:,2])
x=np.reshape(x,grid_dims)
y=np.reshape(y,grid_dims)
z=np.reshape(z,grid_dims)
print(z)
#print (type(x))
#print ((x))

type(x)
# x and y are bounds, so z should be the value *inside* those bounds.
# Therefore, remove the last value from the z array.
#z = z[:-1, :-1]
z_min, z_max = -np.abs(z).max(), np.abs(z).max()
#
fig, ax = plt.subplots()
#
c = ax.pcolormesh(x, y, z, cmap='RdBu', vmin=z_min, vmax=z_max)
ax.set_title('pcolormesh')
# set the limits of the plot to the limits of the data
ax.axis([x.min(), x.max(), y.min(), y.max()])
fig.colorbar(c, ax=ax)
#
plt.show()

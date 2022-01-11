import numpy as np
import matplotlib as mpl
#mpl.use('svg')
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import re

#need the number of bins in each axis of the grid.
data=np.loadtxt('fes.dat')
pattern=re.compile('nbins')
grid_dims=[0,0]
ind=0
x_label_text=''
y_label_text=''

for i, line in enumerate(open('fes.dat')):

    if i==0:
        temp_line=line
        temp_line=line.split(' ')
        x_label_text=temp_line[2]
        y_label_text=temp_line[3]
        x_label_text=x_label_text.split('.')[0]
        y_label_text=y_label_text.split('.')[0]

for i, line in enumerate(open('fes.dat')):
    for match in re.finditer(pattern, line):
            #print ('Found on line %s: %s' % (i+1, match.group()))
            #print(line)
            if re.search('nbins',str(line)):
                nbin_line=line
                nbin_line=nbin_line.split(' ') 
                nbins=np.int(nbin_line[-1])
                grid_dims[ind]=nbins
                ind=ind+1
#print(grid_dims)


x,y,z=(data[:,0],data[:,1],data[:,2])
x=np.reshape(x,grid_dims)
y=np.reshape(y,grid_dims)
z=np.reshape(z,grid_dims)

print(np.shape(z))

#print (type(x))
#print ((x))

type(x)

# x and y are bounds, so z should be the value *inside* those bounds.
# Therefore, remove the last value from the z array.
#z = z[:-1, :-1]

#z_min, z_max =  np.abs(z).max(), -np.abs(z).min()


#
fig, ax = plt.subplots()

#c = ax.contourf(x, y, z, cmap='RdBu', vmin=z_min, vmax=z_max,rasterized=True)
#levels = MaxNLocator(nbins=15).tick_values(z_min, z_max)
c = ax.pcolormesh(x, y, z)
ax.set_title('Free Energy Surface of Opening Coordinates.')
# set the limits of the plot to the limits of the data
ax.axis([x.min(), x.max(), y.min(), y.max()])
ax.set_xlabel(x_label_text)
ax.set_ylabel(y_label_text)
fig.colorbar(c, ax=ax)

def format_coord(xt, yt):
    xarr = x[0,:]
    yarr = y[:,0]
    if ((xt > xarr.min()) & (xt <= xarr.max()) & 
        (yt > yarr.min()) & (yt <= yarr.max())):
        col = np.searchsorted(xarr, xt)-1
        row = np.searchsorted(yarr, yt)-1
        zt = z[row, col]
        return f'xt={xt:1.4f}, yt={yt:1.4f}, zt={zt:1.4f}'
        #return f'zt={zt:1.4f}'
    else:
        return f''

ax.format_coord = format_coord

#now we will plot the trace of a simulation over the course of the simulation. Must specify the COLVARS FILE.

with open('COLVAR', 'r') as fhand:
    file_lines = [line[:-1] for line in fhand if ((line.strip() != '') and (('#' in line) == False))] # remove the last character '\n'. **Remove empty lines**.
line_length=len(file_lines[0].split(' '))

mat_raw = [[(float(term)) for term in (line.split())] for line in file_lines if len(line.split(' '))==line_length ]
mat = np.array(mat_raw)
#mat=np.array(mat[:-2])
num_cols=np.shape(mat)[1]
# then you can do whatever you like. eg: first column
x=mat[-100000:-1:20,1]
y=mat[-100000:-1:20,2]
plt.plot(x,y)
plt.show()

#plt.savefig('fes.png',dpi=2000)

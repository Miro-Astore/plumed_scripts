import numpy as np
import matplotlib as mpl
#mpl.use('Agg')
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import re

fes_file='out.FES'
#need the number of bins in each axis of the grid.
data=np.loadtxt(fes_file)
pattern=re.compile('nbins')
grid_dims=[0,0]
ind=0
num_walkers=8
x_label_text=''
y_label_text=''
plot_levels=range(0,160,2)

for i, line in enumerate(open(fes_file)):

    if i==0:
        temp_line=line
        temp_line=line.split(' ')
        x_label_text=temp_line[2]
        y_label_text=temp_line[3]
        x_label_text=x_label_text.split('.')[0]
        y_label_text=y_label_text.split('.')[0]

for i, line in enumerate(open(fes_file)):
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
#c = ax.pcolormesh(x, y, z)
c = ax.contour(x, y, z,levels=plot_levels,colors='k',linewidths=0.6)
c = ax.contourf(x, y, z,levels=plot_levels)
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
labels=np.array(range(num_walkers))+1

    #now we will plot the trace of a simulation over the course of the simulation. Must specify the COLVARS FILE.
for i in range(num_walkers):

    with open('repl0' + str(i) + '/COLVAR.' + str(i), 'r') as fhand:
        file_lines = [line[:-1] for line in fhand if ((line.strip() != '') and (('#' in line) == False))] # remove the last character '\n'. **Remove empty lines**.
    line_length=len(file_lines[0].split(' '))

    mat_raw = [[(float(term)) for term in (line.split())] for line in file_lines if len(line.split(' '))==line_length ]
    mat = np.array(mat_raw)
    print(mat)
    #mat=np.array(mat[:-2])
    num_cols=np.shape(mat)[1]
    print(np.shape(mat))
    # then you can do whatever you like. eg: first column
    #x=mat[-10000:-1:20,1]
    #y=mat[-10000:-1:20,2]
    #12461
    #last 200 ns  of walker 
    #x=mat[:-1:10,1]
    #y=mat[:-1:10,2]

    x=mat[-20000:-1:1000,1]
    y=mat[-20000:-1:1000,2]
    #if (i == 1):
    #    plt.plot(x,y, label=labels[i])
    plt.plot(x,y,label=labels[i])

plt.legend()
plt.tight_layout()
plt.show()

#########plt.savefig('fes.png',dpi=2000)

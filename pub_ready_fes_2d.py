import numpy as np
import pickle
import matplotlib as mpl
#mpl.use('Agg')
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import re


fes_file = "out.FES"

mpl.rc('image',cmap='magma')
#need the number of bins in each axis of the grid.
cutoffs = [-0.014, 0.024, -0.014, 0.024]
data=np.loadtxt(fes_file)
pattern=re.compile('nbins')
grid_dims=[0,0]
ind=0
x_label_text=''
y_label_text=''

plot_levels=range(0,120,10)

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

#z = z[x<-0.015]
#z = z[x>0.025]
#
#y = y[x<-0.015]
#y = y[x>0.025]
#
#z = z[y<-0.015]
#z = z[y>0.025]
#
#x = x[y<-0.015]
#x = x[y>0.025]

x=np.reshape(x,grid_dims)
y=np.reshape(y,grid_dims)
z=np.reshape(z,grid_dims)

print(np.shape(z))

#z = z[x<-0.015]
#z = z[x>0.025]
#
#y = y[x<-0.015]
#y = y[x>0.025]
#
#z = z[y<-0.015]
#z = z[y>0.025]
#
#x = x[y<-0.015]
#x = x[y>0.025]

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
print(np.min(z))
z=z-np.min(z)
#c = ax.contour(x, y, z,levels=plot_levels,cornor_mask=True)
c = ax.contour(x, y, z,levels=plot_levels,colors='k',linewidths=0.6)
c = ax.contourf(x, y, z,levels=plot_levels)
ax.set_title('Free Energy Surface of Opening Coordinates.')
# set the limits of the plot to the limits of the data
#ax.axis([x.min(), x.max(), y.min(), y.max()])
ax.axis(cutoffs)
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
#plt.savefig('fes.pdf',dpi=2000)
plt.tight_layout()
pickle.dump(fig, open('FigureObject.fig.pickle', 'wb')) # This is for Python 3 - py2 may need `file` instead of `open`
plt.savefig('FES_temp.pdf')
plt.show()

import numpy as np
import os 
from functools import reduce
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import re
import glob
import itertools
import matplotlib.gridspec as gridspec

cutoffs = [-0.005, 0.024, -0.005, 0.024]
files=list([])
files = ['out_900.FES', 'out_925.FES', 'out_950.FES','out.FES']
#files = ['out_50.FES','out_400.FES','out_500.FES','out_600.FES', 'out_700.FES','out_800.FES']
#for i in range(200,900,50):
#    files.append('out_' + str(i) + '.FES')
print(files)

plot_levels=range(0,90,2)

#handy function for determining factors don't lose
def factors(n):    
    return list(set(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0))))

def format_coord(xt, yt, zt):
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

#detect files and sort them nicely
#files.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])

facts = np.sort(np.array((factors(len(files)))))

print (facts)
print ((len(facts)-1)/2)

#determining rows and cols arrangement, more annoying than you'd think
num_plots_rows=0
num_plots_cols=0

#if a square number we'll have an odd number of factors so set number of rows and cols to the same thing 
if (len(facts) % 2) == 0:
    num_plots_rows=facts[int(len(facts)/2-1)]
    num_plots_cols=facts[int(len(facts)/2)]
else:
    num_plots_rows=facts[int((len(facts)-1)/2)]
    num_plots_cols=facts[int((len(facts)-1)/2)]

print(num_plots_rows)
print(num_plots_cols)

#make grid for viewing convergence
#plt.figure(figsize=(10,4))
AX=gridspec.GridSpec(num_plots_rows,num_plots_cols)
#AX.update (wspace=0.4,hspace=0.8)

row_arr=range(num_plots_rows)
col_arr=range(num_plots_cols)

row_arr_t=list(itertools.chain.from_iterable(itertools.repeat(x, num_plots_cols) for x in row_arr))
row_arr=row_arr_t

col_arr=list(col_arr)*num_plots_rows

print(row_arr)
print(col_arr)

for i in range(len(files)):

    row_place=row_arr[i] 
    col_place=col_arr[i] 
    plt.subplot2grid((num_plots_rows,num_plots_cols),(row_place,col_place),colspan=1,rowspan=1)

    #need the number of bins in each axis of the grid.
    data=np.loadtxt(files[i])
    pattern=re.compile('nbins')
    grid_dims=[0,0]
    ind=0
    x_label_text=''
    y_label_text=''

    for j, line in enumerate(open(files[i])):

        if j==0:
            temp_line=line
            temp_line=line.split(' ')
            x_label_text=temp_line[2]
            y_label_text=temp_line[3]
            x_label_text=x_label_text.split('.')[0]
            y_label_text=y_label_text.split('.')[0]

    for j, line in enumerate(open(files[i])):
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
    #fig, ax = plt.subplots()

    #c = ax.contourf(x, y, z, cmap='RdBu', vmin=z_min, vmax=z_max,rasterized=True)
    #levels = MaxNLocator(nbins=15).tick_values(z_min, z_max)
    #c = plt.contour(x, y, z)
#levels = MaxNLocator(nbins=15).tick_values(z_min, z_max)
    temp_min = 0
    for k in range(np.shape(z)[0]): 
        for l in range(np.shape(z)[1]): 
            if z[k][l] < temp_min and x[k][l] > cutoffs[0] and  x[k][l] < cutoffs[1] and  y[k][l] > cutoffs[2] and  y[k][l] < cutoffs[3] : 
            #if z[i][j] < temp_min: 
                temp_min = z[k][l]
            

    print(temp_min)
    z=z-temp_min
    #c = ax.contour(x, y, z,levels=plot_levels,cornor_mask=True)
    c = plt.contour(x, y, z,levels=plot_levels,colors='k',linewidths=0.6)
    c = plt.contourf(x, y, z,levels=plot_levels)
    #c = plt.pcolormesh(x, y, z)
    plt.title(str(files[i]))
    # set the limits of the plot to the limits of the data
    plt.xlim([cutoffs[0], cutoffs[1]])
    plt.ylim([cutoffs[2], cutoffs[3]])
    plt.format_coord = format_coord
    #plt.ylabel(y_label_text)
    plt.colorbar(c)


#plt.savefig('fig.pdf')
plt.tight_layout()
plt.show()

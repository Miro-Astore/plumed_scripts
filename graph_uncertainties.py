import fnmatch
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from natsort import natsorted, ns, natsort_keygen

file_list=list('')
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, 'fes.*.dat'):
            file_list.append(file)

natsort_key1 = natsort_keygen(key=lambda y: y.lower()) 
file_list.sort(key=natsort_key1)
names=list('')
for i in file_list:
    names.append(i.split('.')[1])

names=set(names)
names=list(names)

segregated_list=[list('')]*len(names)

for i in range(len(names)):
    temp_arr=['']
    for j in file_list:
        if names[i]==j.split('.')[1]:
            temp_arr.append(j)

    temp_arr.pop(0)
    segregated_list[i]=temp_arr


plt.figure(figsize=(10,5))
gridspec.GridSpec(len(names),1)
plt.subplot2grid((len(names),1),(0,0),colspan=1,rowspan=1)

for i in range(len(names)):
    x=np.zeros(len(segregated_list[i]))
    y=np.zeros(len(segregated_list[i]))

    for j in range(len(segregated_list[i])):
        print(segregated_list[i][j])
        data=np.loadtxt(segregated_list[i][j])
        

import numpy as np

count=0
with open('COLVAR', 'r') as fhand:
    file_lines = [line[:-1] for line in fhand if ((line.strip() != '') and (('#' in line) == False)) ] # remove the last character '\n'. **Remove empty lines**.
mat_raw = [[float(term) for term in line.split()] for line in file_lines]
mat = np.array(mat_raw)
# then you can do whatever you like. eg: first column
num_cols=np.shape(mat)[1]
for i in range(num_cols-1):
    print(np.std(mat[:,i+1]))

    print (' col ' + str (i+1) +  ' max ' + str(np.max(mat[:,i+1])) +  ' min , ' + str(np.min(mat[:,i+1])) +  ' std ' + str(np.std(mat[:,i+1])) )
# reshape it to n by n matrix:
#res = first_col.reshape((n, n))

#!/bin/bash
#PBS -P CFTR
#PBS -l ncpus=12
#PBS -l ngpus=1
#PBS -m abe
#PBS -l walltime=6:00:00
#PBS -l mem=8GB
#PBS -M yearlyboozefest@gmail.com

module load intel-mkl/2020.2.254
module load openmpi/4.0.3
module load cuda/11.0.3
module load python3-as-python


cd $PBS_O_WORKDIR
cwd=/home/mast0277/plumed
./configure --prefix=$cwd --enable-modules=opes
make -j 4 
make doc
make install


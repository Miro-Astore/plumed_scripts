module load intel-mkl/2020.2.254
module load gcc/11.1.0
module load openmpi/4.0.3
module load cuda/11.0.3
cwd=$(pwd)
./configure --prefix=$cwd --enable-modules=opes
make -j 4 
make doc
make install


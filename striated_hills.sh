equil_time=0
stride=50000

export PATH=$PATH:/scratch/f91/ma2374/a100_install/plumed-2.8.0/bin
export PATH=$PATH:/scratch/f91/ma2374/programs/gromacs_a100_mpicc/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/scratch/f91/ma2374/a100_install/plumed-2.8.0/lib
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/scratch/f91/ma2374/a100_install/plumed-2.8.0/lib/pkgconfig
export PLUMED_KERNEL=/scratch/f91/ma2374/a100_install/plumed-2.8.0/lib/libplumedKernel.so

total_time=$(cat repl00/out.KERNELS  | tail -n 5 | head -n 1  | awk '{print $1}') 
blocks=$( echo "($total_time - $equil_time) / $stride " | bc -l )
blocks=$(printf "%.0f\n" $blocks)
echo $blocks

#for i in $(seq 1 $blocks); 
for i in $(seq 1 1); 
do
	max_time=$( echo "$total_time - $equil_time - ($stride * $(($i - 1)))"  | bc -l)
        echo $max_time
	#cat repl00/out.KERNELS | awk -v  max_time=$max_time  '$0  && $1 < max_time ' > KERNELS_$i
	cat repl00/out.KERNELS > KERNELS_$i
        #grab header
        cat KERNELS_$i  | head -n 10 | grep \# | sed "s^\.^^g" > copy.KERNELS
        #append the rest of the file
        cat KERNELS_$i | grep -v \# >> copy.KERNELS
        cat copy.KERNELS | head -n-1 > temp.KERNELS
        mv temp.KERNELS copy.KERNELS
        python plumed_scripts/State_from_Kernels.py  -f copy.KERNELS -o out_$i.STATE
        python plumed_scripts/FES_from_State.py --temp 310 -f out_$i.STATE -o out_$i.FES
done 

#python plumed_scripts/view_fes_convergence_2d.py

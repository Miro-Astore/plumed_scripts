module load plumed/2.6.0
equil_time=500000
stride=100000
total_time=$(cat HILLS  | tail -n 5 | head -n 1  | awk '{print $1}') 
blocks=$( echo "($total_time - $equil_time) / $stride " | bc -l )
blocks=$(printf "%.0f\n" $blocks)
echo $blocks

for i in $(seq 0 $blocks); 
do
	max_time=$( echo "$total_time - $equil_time + ($stride * $i)"  | bc -l)
	cat HILLS | awk -v  max_time=$max_time  '$0  && $1 < max_time ' > HILLS_$i
	plumed sum_hills --hills HILLS_$i --bin 400,400 --outfile fes$i.dat 

done 

#python plumed_scripts/view_fes_convergence_2d.py

module load plumed/2.6.0
whole_hills_file="HILLS"
equil_time=100000
stride=100000
total_time=$(cat $whole_hills_file  | tail -n 5 | head -n 1  | awk '{print $1}') 
blocks=$( echo "($total_time - $equil_time) / $stride " | bc -l )
blocks=$(printf "%.0f\n" $blocks)
echo $blocks

for i in $(seq 1 $blocks); 
#for i in $(seq 0 $blocks); 
do
	max_time=$( echo "$equil_time + ($stride * $(($i - 1)))"  | bc -l)

        echo $max_time
	cat $whole_hills_file | awk -v  max_time=$max_time  '$0  && $1 < max_time ' > HILLS_$i
        max_time_ns=$(($max_time / 1000))
        #grab header
        cat HILLS_$i  | head -n 10 | grep \# > copy.HILLS
        #append the rest of the file
        cat HILLS_$i | grep -v \# >> copy.HILLS
        cat copy.HILLS | head -n-1 > temp.HILLS
        mv temp.HILLS copy.HILLS
        plumed sum_hills --hills copy.HILLS --bin 200,200 --outfile out_$max_time_ns.FES

done 

#python plumed_scripts/view_fes_convergence_2d.py

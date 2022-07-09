equil_time=0
stride=50000
whole_state_file="out.STATE"

total_time=$(cat out.STATE  | tail -n 5 | head -n 1  | awk '{print $1}') 
blocks=$( echo "($total_time - $equil_time) / $stride " | bc -l )
blocks=$(printf "%.0f\n" $blocks)
echo $blocks

#last_FIELDS_line=$(cat $whole_state_file | grep -n FIELDS |  cut -f1 -d: | tail -n 1)
#total_length=$(cat $whole_state_file | wc -l )
#tail -n $(echo $(($last_FIELDS_line - $total_length-1))) $whole_state_file > snap.STATE

cat $whole_state_file | grep -v \# | awk '{print $1}' | uniq > /dev/shm/time_stamps.txt

#for i in $(seq 1 $blocks); 
for i in $(seq 1 $blocks); 
do
	target_time=$( echo "$total_time - $equil_time - ($stride * $(($i - 1)))"  | bc -l)
        
        target_time_ns=$(($target_time / 1000))
        echo $target_time_ns
        
        min=$(awk -v target_time=$target_time '{printf ("%.0f\n",($0-target_time))}' /dev/shm/time_stamps.txt | tee /dev/shm/subtracted_list.txt |  sort | head -n 1 )
        min_line=$(cat /dev/shm/subtracted_list.txt | grep -n "^$min\$" |  cut -f1 -d: | tail -n 1)
        new_target_time=$(cat /dev/shm/time_stamps.txt | sed "$min_line q;d" )
        echo $new_target_time

	cat $whole_state_file | awk -v  new_target_time=$new_target_time  '$0  && ($1 == new_target_time  || match($0, /\#/) )  ' > temp_STATE 
        last_not_comment_line=$(cat temp_STATE | grep -n -v \# |  cut -f1 -d: | tail -n 1 )
        head -n $last_not_comment_line temp_STATE > STATE_$target_time_ns

        last_FIELDS_line=$(cat STATE_$target_time_ns | grep -n FIELDS |  cut -f1 -d: | tail -n 1)
        total_length=$(cat STATE_$target_time_ns | wc -l )
        tail -n $(echo $(($last_FIELDS_line - $total_length-1))) STATE_$target_time_ns > temp.STATE
        mv temp.STATE STATE_$target_time_ns

        ##grab header
        #cat KERNELS_$i  | head -n 10 | grep \# | sed "s^\.^^g" > copy.KERNELS
        ##append the rest of the file
        #cat KERNELS_$i | grep -v \# >> copy.KERNELS
        #cat copy.KERNELS | head -n-1 > temp.KERNELS
        #mv temp.KERNELS copy.KERNELS
        python plumed_scripts/FES_from_State.py --temp 310 -f STATE_$target_time_ns -o out_$STATE_$target_time_ns.FES
done 

#python plumed_scripts/view_fes_convergence_2d.py

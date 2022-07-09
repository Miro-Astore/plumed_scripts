last_FIELDS_line=$(cat out.STATE | grep -n FIELDS |  cut -f1 -d: | tail -n 1)
total_length=$(cat out.STATE | wc -l )
tail -n $(echo $(($last_FIELDS_line - $total_length-1))) out.STATE > snap.STATE


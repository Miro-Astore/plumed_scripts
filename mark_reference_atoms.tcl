set ref_mark_sel [atomselect 0 "name CA and resid 99 to 108 334 to 342 914 to 922 1128 to 1138 1114 to 1121 318 to 326 1003 to 1010 122 to 129"]
set  md_mark_sel [atomselect 1 "name CA and resid 99 to 108 334 to 342 914 to 922 1128 to 1138 1114 to 1121 318 to 326 1003 to 1010 122 to 129"]

set x [$ref_mark_sel get x]
set y [$ref_mark_sel get y]
set z [$ref_mark_sel get z]

$md_mark_sel set x $x
$md_mark_sel set y $y
$md_mark_sel set z $z

set sel [atomselect 1 "all"]
$sel set beta 0.0
$sel set occupancy 1.0
$md_mark_sel set beta 1.0

$sel writepdb marked.pdb

exit

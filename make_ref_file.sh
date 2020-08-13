#usage bash plumed_scripts/make_ref_file.sh ref_struct md_start_struct
vmd -dispdev text $1 -f  $2 -e  ./plumed_scripts/mark_reference_atoms.tcl 
cat marked.pdb | grep ^ATOM > file.pdb
awk '{
if (NF == 11) {
	if ($11==1.00) 
		 print $0 
}

if ( NF == 10) {
	if ($10==1.00) 
		 print $0 
}
}
' file.pdb > reference_struct.pdb

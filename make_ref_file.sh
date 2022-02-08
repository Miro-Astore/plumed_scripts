#usage bash plumed_scripts/make_ref_file.sh ref_struct md_start_struct
vmd -dispdev text $1 -f  $2 -e  ./plumed_scripts/mark_reference_atoms.tcl 
cat marked.pdb | grep -E "^.{62}1\.00\s" > reference_struct.pdb

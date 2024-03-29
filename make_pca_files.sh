#this will take a list of pca files with their last frame corresponding to the most extreme of the desired pca vector. it will then cat them together and make them readable to plumed. the occ and beta stuff is to fix plumed's hacky indexing rules. 
#second argument $2 is the reference system 

#usage 
# bash plumed_scripts/make_pca_files.sh list_pcas.txt ref_average_struct.pdb md_start_struct.pdb 

count=1
for i in $(cat $1); 
do 

	echo "making vec files"
	vmd -dispdev text $i -f $3 -e  ./plumed_scripts/mark_reference_atoms.tcl 
echo "REMARK TYPE=OPTIMAL" > vec_struct.pdb
cat marked.pdb | grep -E "^.{62}1\.00\s" > file.pdb

cat  file.pdb >> vec_struct.pdb
echo "END" >> vec_struct.pdb

echo "making ref files"
vmd -dispdev text $2 -f $3 -e  ./plumed_scripts/mark_reference_atoms.tcl 

echo "REMARK TYPE=OPTIMAL" > reference_struct.pdb
cat marked.pdb | grep -E "^.{62}1\.00\s" > file.pdb
cat file.pdb >> reference_struct.pdb
echo "END" >> reference_struct.pdb
cat reference_struct.pdb vec_struct.pdb  > plumed_pca_$count.pdb

count=$(($count + 1 ))
done

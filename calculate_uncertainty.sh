#plumed driver --mf_xtc memb_prod1.xtc --plumed plumed_scripts/reweight.dat --kt 2.57748353

bmax=`awk 'BEGIN{max=0.}{if($1!="#!" && $4>max)max=$4}END{print max}' COLVAR_reweighted`

pca1_max=`awk 'BEGIN{max=0.}{if($1!="#!" && $2>max)max=$2}END{print max}' COLVAR_reweighted`

pca2_max=`awk 'BEGIN{max=0.}{if($1!="#!" && $3>max)max=$3}END{print max}' COLVAR_reweighted`

pca1_min=`awk 'BEGIN{min=0.}{if($1!="#!" && $2<min)min=$2}END{print min}' COLVAR_reweighted`

pca2_min=`awk 'BEGIN{min=0.}{if($1!="#!" && $3<min)min=$3}END{print min}' COLVAR_reweighted`

echo $pca1_min
echo $pca1_max
echo $pca2_min
echo $pca2_max


awk '{if($1!="#!") print $2,exp(($4-bmax)/kbt)}' kbt=2.57748353 bmax=$bmax COLVAR_reweighted > pca1.weight

awk '{if($1!="#!") print $3,exp(($4-bmax)/kbt)}' kbt=2.57748353 bmax=$bmax COLVAR_reweighted > pca2.weight


#for i in `seq 1 10 1000`; do python3 plumed_scripts/do_block_fes.py pca1.weight 1  -0.001 0.001 500 2.57748353 $i pca1 ; done 
#
#for i in `seq 1 10 1000`; do python3 plumed_scripts/do_block_fes.py pca2.weight 1  -0.001 0.001 500 2.57748353 $i pca2 ; done 
for i in `seq 1 10 1000`; do python3 plumed_scripts/do_block_fes.py pca1.weight 1  $pca1_min $pca1_max 500 2.57748353 $i pca1 ; done 

for i in `seq 1 10 1000`; do python3 plumed_scripts/do_block_fes.py pca2.weight 1  $pca2_min $pca2_max 500 2.57748353 $i pca2 ; done 

for i in $(ls fes.pca*); 
do 
	cat $i | grep -v Inifinity > temp.fes
	mv temp.fes $i
done

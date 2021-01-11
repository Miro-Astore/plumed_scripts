#plumed driver --mf_xtc memb_prod1.xtc --plumed plumed_scripts/reweight.dat --kt 2.494339

bmax=`awk 'BEGIN{max=0.}{if($1!="#!" && $4>max)max=$4}END{print max}' COLVAR_reweighted`

awk '{if($1!="#!") print $2,$3,exp(($4-bmax)/kbt)}' kbt=2.494339 bmax=$bmax COLVAR_reweighted > pca1_pca2.weight

for i in `seq 1 10 1000`; do python3 plumed_scripts/do_block_fes.py pca1_pca2.weight 2 -0.1 0.1 220 -0.1 0.1 220 2.494339 $i ; done 


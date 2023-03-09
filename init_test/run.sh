#!/bin/bash

set -e

# Run reconstructions

[ ! -d results/LL_1_1 ] && ./run_reco.sh LL 1 1 # ones are dummies here

[ ! -d results/Bloch_flash_1_1 ] && ./run_reco.sh Bloch_flash 1 1 # ones are dummies here

R1_scaling=(10 5 3 2 1 0.5)
R2_scaling=(01 05 10 20)

for (( i=0; i<${#R1_scaling[@]}; i++ ));
do
	for (( j=0; j<${#R2_scaling[@]}; j++ ));
	do
		echo "${R1_scaling[$i]}" "${R2_scaling[$j]}"

		[ ! -d results/Bloch_short_${R1_scaling[$i]}_${R2_scaling[$j]} ] && ./run_reco.sh Bloch_short "${R1_scaling[$i]}" "${R2_scaling[$j]}"
	done
done


# Sort datasets

for (( i=0; i<${#R2_scaling[@]}; i++ ));
do
	bart join 7 $(find results/Bloch_short_*_"${R2_scaling[$i]}"/t1map.cfl | sed -e 's/\.cfl//') tmp_t1_"${R2_scaling[$i]}"
	bart join 7 $(find results/Bloch_short_*_"${R2_scaling[$i]}"/t2map.cfl | sed -e 's/\.cfl//') tmp_t2_"${R2_scaling[$i]}"
done

# Order
echo "Ordering of files!"

FILE=results/order.txt
[ -f ${FILE} ] && rm ${FILE}
touch ${FILE}

# SR1
echo $(find results/Bloch_short_*_"${R2_scaling[0]}"/t1map.cfl | sed -e 's/results\/Bloch_short//' | sed -e 's/t1map.cfl//' | sed -e 's/_01\///' | sed -e 's/_//') >> ${FILE} # ${R2_scaling[0]} == 01
# SR2
echo $(find tmp_t1_*.cfl | sed -e 's/\.cfl//' | sed -e 's/tmp_t1//' | sed -e 's/_//') >> ${FILE}

bart join 8 $(find tmp_t1_*.cfl | sed -e 's/\.cfl//') results/joined_Bloch_t1_maps
bart join 8 $(find tmp_t2_*.cfl | sed -e 's/\.cfl//') results/joined_Bloch_t2_maps

# Clean up
rm tmp_*.{cfl,hdr}



# Improve testing

# Join ROIs
bart join 6 $(ls vertices/*.cfl | sed -e 's/\.cfl//') results/rois

# Extract ROIs

bart fmac results/{LL_1_1/t1map,rois,LL_1_1/t1_test}

bart fmac results/{Bloch_flash_1_1/t1map,rois,Bloch_flash_1_1/t1_test}

for (( i=0; i<${#R1_scaling[@]}; i++ ));
do
	for (( j=0; j<${#R2_scaling[@]}; j++ ));
	do

		bart fmac results/Bloch_short_${R1_scaling[$i]}_${R2_scaling[$j]}/t1map results/rois results/Bloch_short_${R1_scaling[$i]}_${R2_scaling[$j]}/t1_test

		bart fmac results/Bloch_short_${R1_scaling[$i]}_${R2_scaling[$j]}/t2map results/rois results/Bloch_short_${R1_scaling[$i]}_${R2_scaling[$j]}/t2_test
	done
done

rm results/rois.{cfl,hdr}
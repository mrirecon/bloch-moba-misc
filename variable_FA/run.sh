#!/bin/bash

set -eux

export BART_COMPAT_VERSION=v0.9.00

# Load data
./data/load_data.sh


# Run reconstructions
[ ! -d results/LL_8 ] && ./run_reco.sh LL 8


FAs=(20 40 45 50 60 70 77)

for (( i=0; i<${#FAs[@]}; i++ ));
do
	echo "${FAs[$i]}"

	[ ! -d results/Bloch_${FAs[$i]} ] && ./run_reco.sh Bloch "${FAs[$i]}"
done

# Sort datasets

bart join 7 $(find results/Bloch_*/t1map.cfl | sed -e 's/\.cfl//') results/joined_t1

bart join 7 $(find results/Bloch_*/t2map.cfl | sed -e 's/\.cfl//') results/joined_t2


# Order
echo "Ordering of files!"

FILE=results/order.txt
[ -f ${FILE} ] && rm ${FILE}
touch ${FILE}

echo $(find results/Bloch_*/t1map.cfl | sed -e 's/results\/Bloch_//' | sed -e 's/\/t1map.cfl//' ) >> ${FILE}



# Improve testing

# Join ROIs
bart join 6 $(ls vertices/*.cfl | sed -e 's/\.cfl//') results/rois

bart fmac results/LL_8/t1map results/rois results/LL_8/t1_test

for (( i=0; i<${#FAs[@]}; i++ ));
do
	# Extract ROIs
	bart fmac results/Bloch_${FAs[$i]}/t1map results/rois results/Bloch_${FAs[$i]}/t1_test
	bart fmac results/Bloch_${FAs[$i]}/t2map results/rois results/Bloch_${FAs[$i]}/t2_test

done

rm results/rois.{cfl,hdr}
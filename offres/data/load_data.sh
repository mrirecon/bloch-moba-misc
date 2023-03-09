#!/bin/bash

# Estimate absolute paths

FULL_PATH=$(realpath ${0})
ABS_PATH=$(dirname ${FULL_PATH})


# Get and rename data for this analysis
## FIXME: remove rename and load data directly

FILES=(
	data_invivo_b0map
	)

OUT=(
	ksp_b0map
	)

for (( i=0; i<${#FILES[@]}; i++ ));
do
	if [[ ! -f "${ABS_PATH}/${OUT[$i]}.cfl" ]];
	then

		bart copy ${ABS_PATH}/../../data/${FILES[$i]} ${ABS_PATH}/${OUT[$i]}

		echo "Generated output file: ${ABS_PATH}/${OUT[$i]}.{cfl,hdr}" >&2
	fi
done
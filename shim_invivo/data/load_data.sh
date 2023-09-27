#!/bin/bash

# Estimate absolute paths

FULL_PATH=$(realpath ${0})
ABS_PATH=$(dirname ${FULL_PATH})


# Get and rename data for this analysis
## FIXME: remove rename and load data directly

FILES=(
	data_invivo_b0map
	data_invivo_b1map
	data_invivo_irflash
	data_invivo_irbssfp
	data_invivo_irbssfp_shim
	)

OUT=(
	ksp_b0map
	ksp_b1map
	ksp_flash
	ksp_bssfp
	ksp_bssfp_shim
	)

source ${ABS_PATH}/../../utils/data_loc.sh

for (( i=0; i<${#FILES[@]}; i++ ));
do
	if [[ ! -f "${ABS_PATH}/${OUT[$i]}.cfl" ]];
	then
		if [[ -f $DATA_LOC/${FILES[$i]}".cfl" ]];
		then
			bart copy $DATA_LOC/${FILES[$i]} ${ABS_PATH}/${OUT[$i]}
		else
			bart copy ${ABS_PATH}/../../data/${FILES[$i]} ${ABS_PATH}/${OUT[$i]}
		fi

		echo "Generated output file: ${ABS_PATH}/${OUT[$i]}.{cfl,hdr}" >&2
	fi
done
#!/bin/bash

# Estimate absolute paths

FULL_PATH=$(realpath ${0})
ABS_PATH=$(dirname ${FULL_PATH})


# Get and rename data for this analysis
## FIXME: remove rename and load data directly

FILES=(
	data_vfa_irflash
	data_vfa_irbssfp_20
	data_vfa_irbssfp_40
	data_vfa_irbssfp_45
	data_vfa_irbssfp_50
	data_vfa_irbssfp_60
	data_vfa_irbssfp_70
	data_vfa_irbssfp_77
	data_vfa_b0map
	data_vfa_b1map
)

OUT=(
	ksp_flash
	ksp_20
	ksp_40
	ksp_45
	ksp_50
	ksp_60
	ksp_70
	ksp_77
	ksp_b0map
	ksp_b1map
)

for (( i=0; i<${#FILES[@]}; i++ ));
do
	if [[ ! -f "${ABS_PATH}/${OUT[$i]}.cfl" ]];
	then
		bart copy ${ABS_PATH}/../../data/${FILES[$i]} ${ABS_PATH}/${OUT[$i]}

		echo "Generated output file: ${ABS_PATH}/${OUT[$i]}.{cfl,hdr}" >&2
	fi
done
#!/bin/bash

# Estimate absolute paths

FULL_PATH=$(realpath ${0})
ABS_PATH=$(dirname ${FULL_PATH})


# Get and rename data for this analysis
## FIXME: remove rename and load data directly

FILES=(data_06_irflash data_06_irbssfp_short)
OUT=(ksp_flash ksp_short)

for (( i=0; i<${#FILES[@]}; i++ ));
do
	if [[ ! -f "${OUT[$i]}.cfl" ]];
	then
		bart copy ${ABS_PATH}/../../data/${FILES[$i]} ${ABS_PATH}/${OUT[$i]}

		echo "Generated output file: ${OUT[$i]}.{cfl,hdr}" >&2
	fi
done

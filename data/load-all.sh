#!/bin/bash

set -B

ZENODO_RECORD=7837312

for i in  data_invivo_b0map data_invivo_b1map data_invivo_irflash data_invivo_irbssfp \
	data_invivo_irbssfp_shim data_vfa_b0map data_vfa_b1map data_vfa_irflash \
	data_vfa_irbssfp_20 data_vfa_irbssfp_40 data_vfa_irbssfp_45 data_vfa_irbssfp_50 \
	data_vfa_irbssfp_60 data_vfa_irbssfp_70 data_vfa_irbssfp_77
do

	./load-cfl.sh ${ZENODO_RECORD} ${i} .
done


ZENODO_RECORD_2=6992763

for i in  data_06_irflash data_06_irbssfp_short
do

	./load-cfl.sh ${ZENODO_RECORD_2} ${i} .
done
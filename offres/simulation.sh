#!/bin/bash

set -euo pipefail
set -b
set -x

FULL_PATH=$(realpath ${0})
REL_PATH=$(dirname ${FULL_PATH})

[ -d tmp ] && rm -r tmp
mkdir tmp

# Simulation
DIM=1
SPOKES=1
REP=1

SEQ=IR-BSSFP
FA=45
BWTP=4
REP=1000
INV_LEN=0
INV_SPOILER=0
SLICE_THICKNESS=0.001
SLICE_PROFILE_SPINS=1


# Short RF
RF_DUR=0.00001
TR=0.0045
TE=0.00225
PREP_LEN=${TE}
SS_GRAD_STRENGTH=0



T1=0.834
T2=0.08
M0=1

OFF=(270 7 87)	# [rad/s]

[ -f off.txt ] && rm off.txt
touch off.txt

NAME=()

for (( i=0; i<${#OFF[@]}; i++ ));
do
	echo "${OFF[$i]}"

	printf "%04.0f\n" "${OFF[$i]}" >> off.txt

	nice -n 5 bart sim --STM \
	--seq IR-BSSFP,TR=${TR},TE=${TE},FA=${FA},Nrep=${REP},Trf=${RF_DUR},BWTP=${BWTP},off=${OFF[$i]},pinv,ipl=${INV_LEN},ppl=${PREP_LEN},sl-grad=${SS_GRAD_STRENGTH},isp=${INV_SPOILER},slice-thickness=${SLICE_THICKNESS},Nspins=${SLICE_PROFILE_SPINS} \
	--split-dim \
	-1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/sig_$(printf "%04.0f\n" "${OFF[$i]}")

	# Use to avoid sorting it
	NAME+="tmp/sig_$(printf "%04.0f\n" "${OFF[$i]}") "

done


# Stack signals
bart join 6 $(echo "${NAME[@]}") joined_sig

[ -d tmp ] && rm -r tmp
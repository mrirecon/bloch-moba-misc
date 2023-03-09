#!/bin/bash

set -euo pipefail
set -b
set -x


FULL_PATH=$(realpath ${0})
REL_PATH=$(dirname ${FULL_PATH})


# Load and Extract Reconstruction information

if [ ! -f ${REL_PATH}/opts.sh ];
then
	echo "${REL_PATH}/opts.sh does not exist." >&2
	exit 1
fi

source ${REL_PATH}/opts.sh



[ -d tmp ] && rm -r tmp
mkdir tmp

# Adjust Simulation

REP=1000
SEQ=IR-BSSFP
SLICE_THICKNESS=0.02
B1=0.857830

# Long RF

#WM, reference
T1=1.470930
T2=0.0196
M0=1

nice -n 5 bart sim --STM \
--seq IR-BSSFP,TR=${TR},TE=${TE},FA=$(echo $FA $B1 | awk '{printf "%f\n",$1*$2}'),Nrep=${REP},Trf=${RF_DUR},BWTP=${BWTP},ipl=${INV_LEN},ppl=${PREP_LEN},sl-grad=${SS_GRAD_STRENGTH},isp=${INV_SPOILER},slice-thickness=${SLICE_THICKNESS},Nspins=${SLICE_PROFILE_SPINS} \
--split-dim \
-1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 sig



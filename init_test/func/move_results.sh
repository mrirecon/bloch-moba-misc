#!/bin/bash

set -euo pipefail
set -x

# Estimate relative paths

FULL_PATH=$(realpath ${0})
REL_PATH=$(dirname ${FULL_PATH})


# Load and Extract Reconstruction information

if [ ! -f ${REL_PATH}/opts.sh ];
then
	echo "${REL_PATH}/opts.sh does not exist." >&2
	exit 1
fi

source ${REL_PATH}/opts.sh

SR1=$1
SR2=$2

# Save results

RESULTS=results/${MODEL}_${SR1}_${SR2}

[ ! -d $RESULTS ] && mkdir -p $RESULTS

cp t1map.{cfl,hdr} $RESULTS || true
cp t2map.{cfl,hdr} $RESULTS || true

# Save additional information

OUTDIR=out/out_${MODEL}_${SR1}_${SR2}

[ ! -d $OUTDIR ] && mkdir -p $OUTDIR

# Save additional files (not reqired for paper)
if true;
then
        ALL_FILES=${OUTDIR}/all
        
        [ ! -d $ALL_FILES ] && mkdir $ALL_FILES

        mv *.{cfl,hdr,png,log} $ALL_FILES || true
fi


rm current_*.{cfl,hdr} || true
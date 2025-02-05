#!/bin/bash

set -e

export BART_COMPAT_VERSION=v0.9.00

# Load data
./data/load_data.sh


# Run reconstructions

[ ! -d results/LL ] && ./run_reco.sh LL
[ ! -d results/Bloch_flash ] && ./run_reco.sh Bloch_flash
[ ! -d results/Bloch_short ] && ./run_reco.sh Bloch_short
[ ! -d results/Bloch_short_b0 ] && ./run_reco.sh Bloch_short_b0


# Improve testing

# Join ROIs
bart join 6 $(ls vertices/*.cfl | sed -e 's/\.cfl//') results/rois

# Extract ROIs

bart fmac results/{LL/t1map,rois,LL/t1_test}

bart fmac results/{Bloch_flash/t1map,rois,Bloch_flash/t1_test}

bart fmac results/{Bloch_short/t1map,rois,Bloch_short/t1_test}
bart fmac results/{Bloch_short/t2map,rois,Bloch_short/t2_test}

bart fmac results/{Bloch_short_b0/t1map,rois,Bloch_short_b0/t1_test}
bart fmac results/{Bloch_short_b0/t2map,rois,Bloch_short_b0/t2_test}

rm results/rois.{cfl,hdr}
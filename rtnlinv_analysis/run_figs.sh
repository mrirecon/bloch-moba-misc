#!/bin/bash

./run.sh

# -------------------------------------
#       Visualization
# -------------------------------------

python3 func/plot_simulation.py results/Bloch_short{,_hp}/t1map ref_roi roi sim results/figure  $(ls vertices/*.cfl | sed -e 's/\.cfl//')

./func/move_results.sh


# Improve Testing

# Join ROIs
bart join 6 $(ls vertices/*.cfl | sed -e 's/\.cfl//') results/rois

# Extract ROIs

bart fmac results/{LL/t1map,rois,LL/t1_test}

bart fmac results/{Bloch_flash/t1map,rois,Bloch_flash/t1_test}

bart fmac results/{Bloch_short/t1map,rois,Bloch_short/t1_test}
bart fmac results/{Bloch_short/t2map,rois,Bloch_short/t2_test}

bart fmac results/{Bloch_short_hp/t1map,rois,Bloch_short_hp/t1_test}
bart fmac results/{Bloch_short_hp/t2map,rois,Bloch_short_hp/t2_test}

rm results/rois.{cfl,hdr}



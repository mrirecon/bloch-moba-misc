#!/bin/bash

./run.sh

# -------------------------------------
#       Visualization
# -------------------------------------

python3 func/plot_simulation.py results/Bloch_short{,_hp}/t1map results/ref_roi results/roi results/sim results/figure  $(ls vertices/*.cfl | sed -e 's/\.cfl//')


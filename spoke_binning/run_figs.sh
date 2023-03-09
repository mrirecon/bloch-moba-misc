#!/bin/bash

set -eux

# Run reconstructions
./run.sh

# Create figure
./func/create_figure.py results/Bloch_flash/t1map results/Bloch_short/t{1,2}map results/Bloch_short_nobin/t{1,2}map results/figure  $(ls vertices/*.cfl | sed -e 's/\.cfl//')

./clean_up.sh

#!/bin/bash

./run.sh

# Visualize slice-profile simulation

python3 plot_simulation.py figure off.txt joined_sig b0map3 $(ls vertices/*.cfl | sed -e 's/\.cfl//')

# rm *.{cfl,hdr}
#!/bin/bash

export BART_COMPAT_VERSION=v0.9.00

# Load data
./data/load_data.sh

# Load B0 Map
./b0map/load_b0map.sh

# Rotate B0 map for visualization
SAMPLES=$(bart show -d 0 b0map)
bart resize -c 0 $((SAMPLES/2)) 1 $((SAMPLES/2)) b0map b0map2
bart flip $(bart bitmask 0) b0map2 b0map3

rm b0map{,2}.{cfl,hdr}


## Run slice-profile simulation
./simulation.sh

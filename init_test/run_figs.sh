#!/bin/bash

set -eux


# Run reconstructions
./run.sh

# Create figure
./func/create_figure.py results/joined_Bloch_t1_maps results/joined_Bloch_t2_maps results/figure results/order.txt

# ./clean_up.sh

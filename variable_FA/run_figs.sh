#!/bin/bash

set -eux

# Run reconstructions
./run.sh

# Create figure
./func/create_figure.py results/LL_8/t1map results/joined_t1 results/joined_t2 results/figure results/order.txt vertices/v000 vertices/v001

./clean_up.sh

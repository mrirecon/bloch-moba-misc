#!/bin/bash

set -eux

# Check if BART is set up correctly

if [ ! -e $TOOLBOX_PATH/bart ] ;
then
	echo "\$TOOLBOX_PATH is not set correctly!" >&2
	exit 1
fi

export PATH=$TOOLBOX_PATH:$PATH


export MODEL=$1

# Load Model dependencies

case ${MODEL} in

LL | Bloch_flash)
	RAW=data/ksp_flash
	;;

Bloch_short1)

	RAW=data/ksp_bssfp_shim

	# Load B1 map
	./b1map/load_b1map.sh mask/mask
	./b0map/load_b0map.sh
	;;

Bloch_short2)

	RAW=data/ksp_bssfp

	# Load B1 map
	./b1map/load_b1map.sh mask/mask
	./b0map/load_b0map.sh
	;;
esac


# Load required parameters
source func/opts.sh

# Prepare kspace data for reconstruction
./func/prepare_data.sh ${RAW}

# Run reconstrution
./func/reco.sh ${RAW} traj data

# Postprocess data
./func/post_process.sh mask/mask

# Move data to model folder
./func/move_results.sh
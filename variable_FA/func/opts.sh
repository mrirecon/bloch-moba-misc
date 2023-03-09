#!/bin/bash

AV_COILS=3
AV=10

# Sequence Parameter
BWTP=4

# Optimization Parameter
OS=1
REDU_FAC=3
INNER_ITER=250
STEP_SIZE=0.95
MIN_R1=0.001

RF_DUR=0.001
INV_LEN=0.01
INV_SPOILER=0.005
SLICE_PROFILE_SPINS=21
SS_GRAD_STRENGTH=0.01879

SLICE_THICKNESS=0.02
NOM_SLICE_THICKNESS=0.005

GA=13

# Model specifics
case ${MODEL} in

LL)
	ITER=12

        TR=0.0038
        TE=0.00226
        FA=8
        INV_LEN=0
        PREP_LEN=0
        INV_SPOILER=0
        DELAY=0.0153

	LAMBDA=0.001
        ;;

Bloch_flash)

	ITER=12

        TR=0.0038
        TE=0.00226
        FA=8
        PREP_LEN=0

	LAMBDA=0.0002
        ;;

Bloch)

	ITER=12

        TR=0.0045
        TE=0.00225
        PREP_LEN=${TE}

	LAMBDA=0.0002
        ;;

esac

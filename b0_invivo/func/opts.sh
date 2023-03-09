#!/bin/bash

GA=7
AV_COILS=5
AV=15

# Sequence Parameter
BWTP=4

# Optimization Parameter
OS=1
REDU_FAC=3
INNER_ITER=250
STEP_SIZE=0.95
MIN_R1=0.001


# Model specifics
case ${MODEL} in

LL)

        TR=0.0038
        TE=0.00226
        FA=8
        RF_DUR=0.001
        INV_LEN=0
        PREP_LEN=0
        INV_SPOILER=0
        DELAY=0.0153
        ;;

Bloch_flash)

        TR=0.0038
        TE=0.00226
        FA=8
        RF_DUR=0.001
        INV_LEN=0.01
        PREP_LEN=0
        INV_SPOILER=0.005
        SLICE_PROFILE_SPINS=21
        SS_GRAD_STRENGTH=0.01879
        ;;

Bloch_short | Bloch_short_b0)

        TR=0.0045
        TE=0.00225
        FA=45
        PREP_LEN=${TE}
        RF_DUR=0.001
        INV_LEN=0.01
        INV_SPOILER=0.005
        SLICE_PROFILE_SPINS=21
        SS_GRAD_STRENGTH=0.01879
        ;;

esac

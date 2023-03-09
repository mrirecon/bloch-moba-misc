#!/bin/bash

set -eux

# Find correct B1 and B0 map orientation
# Stack all radial spokes of inversion curve into single slice and reconstruct them

# Estimate relative paths
FULL_PATH=$(realpath ${0})
REL_PATH=$(dirname ${FULL_PATH})

# Load data
# bart twixread -A /home/ague/archive/vol/2023-03-14_MRTG-BLMB-0008/raw/meas_MID00049_FID06090_IR_bSSFP_BR256_1ms_IMT_Radial_513d35c9_develop__AdvShim01.dat _raw
bart copy ${REL_PATH}/../data/ksp_bssfp _raw

SAMPLES=$(bart show -d 0 _raw)
SPOKES=$(bart show -d 1 _raw)
COILS=$(bart show -d 3 _raw)
FRAMES=$(bart show -d 10 _raw)

bart transpose 1 3 _raw{,1}
bart reshape $(bart bitmask 3 10) $((FRAMES*SPOKES)) 1 _raw{1,2}
bart transpose 1 3 _raw2 raw
rm _raw{,1,2}.{cfl,hdr}

bart transpose 1 2 raw tmp
bart transpose 0 1 tmp raw2
rm {raw,tmp}.{cfl,hdr}

# Estimate Coil sensitivities
bart traj -x $SAMPLES -y $((FRAMES*SPOKES)) -s7 -G -D -r _traj
bart scale -- 0.5 _traj traj
rm _traj.{cfl,hdr}

# Phase preserving PI reconstruction
bart nufft -g -i traj raw2 _pro

# Grid non-Cartesian data to Cartesian grid
bart fft $(bart bitmask 0 1 2) _pro ksp
rm _pro.{cfl,hdr}

# Estimate Coil sensitivities
bart ecalib -c 0 -m 1 ksp sens
rm ksp.{cfl,hdr}

# Phase preserving PI reconstruction
bart pics -g -e -S -d 5 -l1 -r0.001 -t traj raw2 sens ref

rm {traj,raw2,sens}.{cfl,hdr}

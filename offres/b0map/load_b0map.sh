#!/bin/bash

# B0 Mapping with Siemens Sequence "gre_field_mapping" based on
# Nayak, K.S. and Nishimura, D.G. (2000),
# Automatic field map generation and off-resonance correction for projection reconstruction imaging.
# Magn. Reson. Med., 43: 151-154.
# https://doi.org/10.1002/(SICI)1522-2594(200001)43:1<151::AID-MRM19>3.0.CO;2-K

# Estimate relative paths
FULL_PATH=$(realpath ${0})
REL_PATH=$(dirname ${FULL_PATH})

TE1=0.00492	# Early TE
TE2=0.00738	# Late TE

# Load data
# bart twixread -A /home/ague/archive/vol/2023-03-14_MRTG-BLMB-0008/raw/meas_MID00043_FID06084_gre_field_mapping_BR256_S01.dat raw
bart copy ${REL_PATH}/../data/ksp_b0map raw

# Estimate Coil sensitivities
bart ecalib -c 0 -m 1 raw sens

# Phase preserving PI reconstruction
bart pics -g -e -S -d 5 raw sens _reco
rm {sens,raw}.{cfl,hdr}

SAMPLES=$(bart show -d 0 _reco)
bart resize -c 0 $((SAMPLES/2)) _reco reco

bart slice 5 0 reco te1
bart slice 5 1 reco te2
rm {,_}reco.{cfl,hdr}

# Estimate B0 = phase(reco(TE2) * conj(reco(TE2))) / (TE2 - TE1)
# Nayak & Nishimura, MRM, 2000.

bart conj te1 te1c
bart fmac te2 te1c prod
bart carg prod ph
bart scale -- $(echo $TE1 $TE2 | awk '{printf "%f\n", -1/($2-$1)}') ph _b0map # [rad/s] 
rm {ph,te1,te1c,te2,prod}.{cfl,hdr}

# Resize for input in moba
bart resize -c 0 $SAMPLES 1 $SAMPLES _b0map __b0map
bart transpose 0 1 __b0map b0map
rm {_,}_b0map.{cfl,hdr}

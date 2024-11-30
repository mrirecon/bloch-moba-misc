#!/bin/bash

set -e

export BART_COMPAT_VERSION=v0.9.00

# File to store off-resonance
[ -f off.txt ] && rm off.txt
touch off.txt

T1=0.834
T2=0.08
REP=500
TR=0.0045
TE=0.00225
FA=45
TRF=0.001
BWTP=4

Nspins=100

for i in `seq 0 $Nspins`;
do
	OFF=$(echo $i $Nspins $TE | awk '{printf "%f\n", -3.1415 + 2*3.1415*1/$3*$1/$2}') # [rad/s]

	# Relative off-resonance
	OFF2=$(echo $i $Nspins $TE | awk '{printf "%f\n", -3.1415 + 2*3.1415*$1/$2}') # rad/s/TE
	echo $OFF2 >> off.txt

	# Simulation
        bart sim --ODE \
	--seq BSSFP,TR=$TR,TE=$TE,Nrep=$REP,ppl=$TE,Trf=$TRF,FA=$FA,BWTP=$BWTP,off=$OFF \
	-1 $T1:$T1:1 -2 $T2:$T2:1 \
	sig_$(printf "%03.0f" $i)
	
	# Extract steady-state data
	bart slice 5 $((REP-1)) sig_$(printf "%03.0f" $i) sig2_$(printf "%03.0f" $i)
done

bart join 6 $(ls sig2_*.cfl | sed -e 's/\.cfl//') data

# Clean up
rm sig{,2}_*.{cfl,hdr}

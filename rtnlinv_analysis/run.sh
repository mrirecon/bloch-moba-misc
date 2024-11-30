#!/bin/bash


set -euxB

export BART_COMPAT_VERSION=v0.9.00

# ---------------------------
#         moba recons
# ---------------------------

# Load data
./data/load_data.sh

[ ! -d results/LL ] && ./run_reco.sh LL
[ ! -d results/Bloch_flash ] && ./run_reco.sh Bloch_flash
[ ! -d results/Bloch_short ] && ./run_reco.sh Bloch_short
[ ! -d results/Bloch_short_hp ] && ./run_reco.sh Bloch_short_hp

# ---------------------------
#      RT-NLINV recon
# ---------------------------

export MODEL=RTNLINV

# Load required parameters
source ./func/opts.sh

# Load b1map
./b1map/load_b1map.sh

# Prepare kspace data for reconstruction
KSP=data/ksp_bssfp
./func/prepare_data.sh ${KSP}

# ! Flipped 10th dim for nlinv !
# -> better inital guess for inversion time in the end
bart transpose 5 10 data{,1}
bart transpose 5 10 traj{,1}
bart flip $(bart bitmask 10) data{1,2}
bart flip $(bart bitmask 10) traj{1,2}

# -------------------------------------
#    RT-NLINV Reconstruction
# -------------------------------------
BR=$(bart show -d 0 ${KSP})

bart rtnlinv -g -x ${BR}:${BR}:1 -S -i 10 -t traj2 data2 _reco _sens

# Reverse flipping of time
bart flip $(bart bitmask 10) {_,}reco

# -------------------------------------
#    Extract ROI from nlinv reco
# -------------------------------------
bart fmac reco vertices/v000 roi0
bart avg -w 3 roi0 roi_avg0

bart fmac reco vertices/v001 roi1
bart avg -w 3 roi1 roi_avg1

bart join 12 roi{0,1,}
# -------------------------------------
#    Extract Physical Para from Ref 1
# -------------------------------------
# T1 parameter
bart fmac results/Bloch_short/t1map vertices/v000 t1roi
bart avg -w 3 t1roi t1avg

bart fmac results/Bloch_short/t1map vertices/v001 t1roi1
bart avg -w 3 t1roi1 t1avg1

# T2 parameter
bart fmac results/Bloch_short/t2map vertices/v000 t2roi
bart avg -w 3 t2roi t2avg

bart fmac results/Bloch_short/t2map vertices/v001 t2roi1
bart avg -w 3 t2roi1 t2avg1

# bart show t1avg
# bart show t2avg



# -------------------------------------
#    Extract Physical Para from Ref HP
# -------------------------------------
# T1 parameter
bart fmac results/Bloch_short_hp/t1map vertices/v000 t1roi_hp
bart avg -w 3 t1roi_hp t1avg_hp

bart fmac results/Bloch_short_hp/t1map vertices/v001 t1roi_hp1
bart avg -w 3 t1roi_hp1 t1avg_hp1

# T2 parameter
bart fmac results/Bloch_short_hp/t2map vertices/v000 t2roi_hp
bart avg -w 3 t2roi_hp t2avg_hp

bart fmac results/Bloch_short_hp/t2map vertices/v001 t2roi_hp1
bart avg -w 3 t2roi_hp1 t2avg_hp1

# bart show t1avg_hp
# bart show t2avg_hp


# B1 parameter

BR=$(($(bart show -d 0 b1map)/2))

bart resize -c 0 ${BR} 1 ${BR} b1map _b1map

bart fmac _b1map vertices/v000 b1roi
bart avg -w 3 b1roi b1avg

bart fmac _b1map vertices/v001 b1roi1
bart avg -w 3 b1roi1 b1avg1

# bart show b1avg

bart join 11 t1roi t2roi b1roi t1roi_hp t2roi_hp ref_roi0 # To keep std information
bart join 11 t1roi1 t2roi1 b1roi1 t1roi_hp1 t2roi_hp1 ref_roi1

bart join 12 ref_roi{0,1,}




# -------------------------------------
#    	Run Simulation
# -------------------------------------

REP=$(($(bart show -d 10 ${KSP})/AV))

# For ROI 0

SEQ=IR-BSSFP
SLICE_THICKNESS=0.02
T1=$(bart show -f "%+.6e%+.6ei" t1avg | sed -r "s/([+-]+[0-9]\.[0-9]{6}e[+-]?[0-9]{2}).*/\1/g")
T2=$(bart show -f "%+.6e%+.6ei" t2avg | sed -r "s/([+-]+[0-9]\.[0-9]{6}e[+-]?[0-9]{2}).*/\1/g")
B1=$(bart show -f "%+.6e%+.6ei" b1avg | sed -r "s/([+-]+[0-9]\.[0-9]{6}e[+-]?[0-9]{2}).*/\1/g")
M0=1

nice -n 5 bart sim --STM \
--seq IR-BSSFP,TR=${TR},TE=${TE},FA=$(echo $FA $B1 | awk '{printf "%f\n",$1*$2}'),Nrep=${REP},Trf=${RF_DUR},BWTP=${BWTP},ipl=${INV_LEN},ppl=${PREP_LEN},sl-grad=${SS_GRAD_STRENGTH},isp=${INV_SPOILER},slice-thickness=${SLICE_THICKNESS},Nspins=${SLICE_PROFILE_SPINS},av-spokes=${AV} \
--split-dim \
-1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 sim0


# For ROI 1

SEQ=IR-BSSFP
SLICE_THICKNESS=0.02
T1=$(bart show -f "%+.6e%+.6ei" t1avg1 | sed -r "s/([+-]+[0-9]\.[0-9]{6}e[+-]?[0-9]{2}).*/\1/g")
T2=$(bart show -f "%+.6e%+.6ei" t2avg1 | sed -r "s/([+-]+[0-9]\.[0-9]{6}e[+-]?[0-9]{2}).*/\1/g")
B1=$(bart show -f "%+.6e%+.6ei" b1avg1 | sed -r "s/([+-]+[0-9]\.[0-9]{6}e[+-]?[0-9]{2}).*/\1/g")
M0=1

nice -n 5 bart sim --STM \
--seq IR-BSSFP,TR=${TR},TE=${TE},FA=$(echo $FA $B1 | awk '{printf "%f\n",$1*$2}'),Nrep=${REP},Trf=${RF_DUR},BWTP=${BWTP},ipl=${INV_LEN},ppl=${PREP_LEN},sl-grad=${SS_GRAD_STRENGTH},isp=${INV_SPOILER},slice-thickness=${SLICE_THICKNESS},Nspins=${SLICE_PROFILE_SPINS},av-spokes=${AV} \
--split-dim \
-1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 sim1

bart join 12 sim{0,1,}

# -------------------------------------
#    	Visualization
# -------------------------------------

python3 func/plot_simulation.py results/Bloch_short{,_hp}/t1map ref_roi roi sim results/figure  $(ls vertices/*.cfl | sed -e 's/\.cfl//')

./func/move_results.sh


# Improve Testing

# Join ROIs
bart join 6 $(ls vertices/*.cfl | sed -e 's/\.cfl//') results/rois

# Extract ROIs

bart fmac results/{LL/t1map,rois,LL/t1_test}

bart fmac results/{Bloch_flash/t1map,rois,Bloch_flash/t1_test}

bart fmac results/{Bloch_short/t1map,rois,Bloch_short/t1_test}
bart fmac results/{Bloch_short/t2map,rois,Bloch_short/t2_test}

bart fmac results/{Bloch_short_hp/t1map,rois,Bloch_short_hp/t1_test}
bart fmac results/{Bloch_short_hp/t2map,rois,Bloch_short_hp/t2_test}

rm results/rois.{cfl,hdr}
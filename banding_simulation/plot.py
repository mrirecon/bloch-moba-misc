#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.join(os.environ['TOOLBOX_PATH'], 'python'))
import cfl

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from copy import copy

FS = 20
MS = 8

DARK = 0

BCOLOR = 'white'  # Background color
TCOLOR = 'black'  # Text color

COLORS = ['#a6611a', '#018571', '#dfc27d', '#80cdc1']

if __name__ == "__main__":

	#Error if wrong number of parameters
	if( len(sys.argv) != 4):
		print( "Plotting" )
		print( "#-----------------------------------------------" )
		print( "Usage: plot_map.py <data> <savename>" )
		exit()

	off = np.loadtxt(sys.argv[1], unpack=True) # Off-resonance values rad/s/TE

	data = np.abs(cfl.readcfl(sys.argv[2]).squeeze())

	savename = sys.argv[3]


	# Detect banding regions

	max_data = np.max(data)
	min_data = np.min(data)

	# Location of bandings
	loc = off[data < min_data*1.1]

	# Width of bandings ~25 % of max signal
	ind = off[data < max_data*0.25]
	# only positve ones
	ind = ind[ind > 0]
	width = np.max(ind) - np.min(ind)


	# Visualization

	if "DARK_LAYOUT" in os.environ:
		DARK = int(os.environ["DARK_LAYOUT"])

	if(DARK):
		plt.style.use(['dark_background'])
	else:
		plt.style.use(['default'])
	
	fig = plt.figure(figsize=(12, 9), dpi=80)

	ax1 = fig.add_subplot(111)

	im = ax1.plot(off, np.abs(data), '.', color=COLORS[0], markersize=MS, label="signal")

	# Add rectangles for marking banding artifact regions
	rect = patches.Rectangle((loc[0]-width/2, 0), width,  max_data*1.1, edgecolor='none', facecolor=COLORS[3], label="banding\n regions")
	ax1.add_patch(rect)

	rect = patches.Rectangle((loc[1]-width/2, 0), width,  max_data*1.1, edgecolor='none', facecolor=COLORS[3])
	ax1.add_patch(rect)

	
	# Label stuff
	ax1.set_xlabel("Off-Resonance $\omega$ / (rad/s/TE)", fontsize=FS)
	ax1.set_ylabel("Signal |M$_{xy}$|", fontsize=FS)

	ax1.set_ylim([0, max_data*1.1])

	ax1.tick_params(axis='both', which='major', labelsize=FS-5)
	ax1.grid("on", color=TCOLOR, alpha=.1, linewidth=.5)
	asp = np.diff(ax1.get_xlim())[0] / np.diff(ax1.get_ylim())[0]
	ax1.set_aspect(asp)
	ax1.legend(fontsize=FS-3)
	
	fig.savefig(savename + ".svg", bbox_inches='tight', transparent=False)
	fig.savefig(savename + ".png", bbox_inches='tight', transparent=False)


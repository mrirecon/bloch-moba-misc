#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
from matplotlib import colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.optimize import curve_fit

from math import ceil


import sys
import os
sys.path.insert(0, os.path.join(os.environ['TOOLBOX_PATH'], 'python'))
import cfl

def func(x, m, b):
	return m * x + b


# Global variables

FS=28

COLORS = ['darkorange', 'r', 'g', 'b', 'm', 'y', 'c', 'k', 'w']

DARK = 0 #dark layout?

VMAX = 2.9
VMAX2 = 0.15
VMIN = 0

DIFF_SCALING = 1


BCOLOR='white'  # Background color
TCOLOR='black'  # Text color



def perform_roi_analysis(paramap, roi):

	segment = paramap * roi

	# Set zeros to be invalid for mean calculation
	segment_m = np.ma.masked_equal(segment, 0)

	return segment_m.mean(), segment_m.std()



if __name__ == "__main__":

	#Error if wrong number of parameters
	if( len(sys.argv) == 6):
		print( "Plotting" )
		print( "#-----------------------------------------------" )
		print( "Usage: create_figure.py <T1 maps> <T2 maps> <outfile> <ordering [txt]>" )
		exit()

	sysargs = sys.argv

	# Load maps
	t1 = np.abs(cfl.readcfl(sysargs[1]).squeeze())
	t1[t1 == np.inf] = 0

	t2 = np.abs(cfl.readcfl(sysargs[2]).squeeze())
	t2[t2 == np.inf] = 0

	# Define output filename
	outfile = sysargs[3]

	ordering = []

	with open(sysargs[4]) as f:

		lines=f.readlines()

		for line in lines:
			
			myarray = np.fromstring(line, dtype=float, sep=' ')
			
			ordering.append(myarray)

	print(ordering)	# sR1, sR2

	# DIMS
	dims = np.shape(t1)	# Samples, Samples, sR1, sR2
	print(dims)

	# --------------------------------------
	#         Create visualization
	# --------------------------------------

	if "DARK_LAYOUT" in os.environ:
		DARK = int(os.environ["DARK_LAYOUT"])

	if(DARK):
		plt.style.use(['dark_background'])
		BCOLOR='black'
		TCOLOR='white'
	else:
		plt.style.use(['default'])

	my_cmap = copy.copy(cm.get_cmap('viridis'))
	my_cmap.set_bad(BCOLOR)

	my_cmap2 = copy.copy(cm.get_cmap('turbo'))
	my_cmap2.set_bad(BCOLOR)
	


	fig = plt.figure(num = 1, figsize=(22, 40), dpi=120, edgecolor='w')

	grid = gridspec.GridSpec(dims[2], dims[3], wspace=0, hspace=-0.5, figure=fig)

	for i in range(1, dims[2]+1):	#sR1
		for j in range(1, dims[3]+1):	#sR2

			ax1 = fig.add_subplot(grid[((i-1)*dims[3])+(j-1)])

			t1m = np.ma.masked_equal(t1[:,:,i-1,j-1], 0)

			im = ax1.imshow(t1m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

			divider = make_axes_locatable(ax1)
			cax = divider.append_axes("right", size="5%", pad=0.05)
			cax.set_visible(False)

			ax1.set_yticklabels([])
			ax1.set_xticklabels([])
			ax1.xaxis.set_ticks_position('none')
			ax1.yaxis.set_ticks_position('none')
			# ax1.set_axis_off()

			if (1 == i):
				ax1.set_title("Init R2: "+str(ordering[1][j-1]), fontsize=FS+5)

			if (1 == j):
				ax1.set_ylabel("Init R1: "+str(ordering[0][i-1]), fontsize=FS+5)

			fig.add_subplot(ax1)

		# Ensure same scaling as map with colorbar has
		divider = make_axes_locatable(ax1)
		cax = divider.append_axes("right", size="5%", pad=0.05)
		cbar = plt.colorbar(im, cax=cax)
		cbar.set_label("T$_1$ / s", fontsize=FS)
		cbar.ax.tick_params(labelsize=FS-5)

	fig.savefig(outfile + '_T1.png', bbox_inches='tight', transparent=False)






	fig = plt.figure(num = 2, figsize=(22, 40), dpi=120, edgecolor='w')

	grid = gridspec.GridSpec(dims[2], dims[3], wspace=0, hspace=-0.5, figure=fig)

	for i in range(1, dims[2]+1):	# Init R1
		for j in range(1, dims[3]+1):	# Init R2

			ax1 = fig.add_subplot(grid[((i-1)*dims[3])+(j-1)])

			t1m = np.ma.masked_equal(t2[:,:,i-1,j-1], 0)

			im = ax1.imshow(t1m, origin='lower', cmap=my_cmap2, vmax=VMAX2, vmin=VMIN)

			divider = make_axes_locatable(ax1)
			cax = divider.append_axes("right", size="5%", pad=0.05)
			cax.set_visible(False)

			ax1.set_yticklabels([])
			ax1.set_xticklabels([])
			ax1.xaxis.set_ticks_position('none')
			ax1.yaxis.set_ticks_position('none')
			# ax1.set_axis_off()

			if (1 == i):
				ax1.set_title("Init R2: "+str(ordering[1][j-1]), fontsize=FS+5)

			if (1 == j):
				ax1.set_ylabel("Init R1: "+str(ordering[0][i-1]), fontsize=FS+5)

			fig.add_subplot(ax1)

		# Ensure same scaling as map with colorbar has
		divider = make_axes_locatable(ax1)
		cax = divider.append_axes("right", size="5%", pad=0.05)
		cbar = plt.colorbar(im, cax=cax)
		cbar.set_label("T$_2$ / s", fontsize=FS)
		cbar.ax.tick_params(labelsize=FS-5)

	fig.savefig(outfile + '_T2.png', bbox_inches='tight', transparent=False)


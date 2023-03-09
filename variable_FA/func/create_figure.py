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
LW=2
MS=8

COLORS = ['darkorange', 'r', 'g', 'b', 'm', 'y', 'c', 'peru', 'palegreen', 'slategray', 'gold', 'springgreen', 'slateblue', 'maroon']
# COLORS=['#a6611a', '#018571']

DARK = 0 #dark layout?

VMAX = 2.9
VMAX2 = 0.08
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
	if( len(sys.argv) == 9):
		print( "Plotting" )
		print( "#-----------------------------------------------" )
		print( "Usage: create_figure.py <LL ref T1> <T1 maps> <T2 maps> <outfile> <fa [txt]> <ROI 1[cfl]> <ROI 2[cfl]>" )
		exit()

	sysargs = sys.argv

	# Load maps
	reft1 = np.abs(cfl.readcfl(sysargs[1]).squeeze())
	reft1[reft1 == np.inf] = 0

	t1 = np.abs(cfl.readcfl(sysargs[2]).squeeze())
	t1[t1 == np.inf] = 0

	t2 = np.abs(cfl.readcfl(sysargs[3]).squeeze())
	t2[t2 == np.inf] = 0

	# Define output filename
	outfile = sysargs[4]

	fa = np.loadtxt(sysargs[5], unpack=True)

	# Load and stack all passed ROIs
	roi = np.abs(cfl.readcfl(sysargs[6]).squeeze())
	roi[roi == np.inf] = 0

	roi2 = np.abs(cfl.readcfl(sysargs[7]).squeeze())
	roi2[roi2 == np.inf] = 0

	rois = [roi, roi2]


	# DIMS
	dims = np.shape(t1)	# Samples, Samples, sR1, sR2
	print(dims)

	# Prepare output txt files

	texts = []

	text=r'''{\renewcommand{\arraystretch}{1.2}\begin{tabular}{c|c|c|c} & \#ROI & $m$ [s/deg] & $b$ [s] \\\hline'''
	texts.append(text)

	# --------------------------------------
	#         Extract T1
	# --------------------------------------

	t1_values = []
	t1_std = []

	t2_values = []
	t2_std = []

	t1_roi2_values = []
	t1_roi2_std = []

	t2_roi2_values = []
	t2_roi2_std = []

	ref1, refstd1 = perform_roi_analysis(reft1, roi)
	ref2, refstd2 = perform_roi_analysis(reft1, roi2)

	for i in range(0,np.shape(t1)[2]):

		val, std = perform_roi_analysis(t1[:,:,i], roi)
		t1_values.append(val)
		t1_std.append(std)

		val2, std2 = perform_roi_analysis(t2[:,:,i], roi)
		t2_values.append(val2)
		t2_std.append(std2)

		print("ROI 1")
		print("T1 = "+ str(val) + " +- "+ str(std) +" s")
		print("T2 = "+ str(val2) + " +- "+ str(std2) +" s")

		val, std = perform_roi_analysis(t1[:,:,i], roi2)
		t1_roi2_values.append(val)
		t1_roi2_std.append(std)

		val2, std2 = perform_roi_analysis(t2[:,:,i], roi2)
		t2_roi2_values.append(val2)
		t2_roi2_std.append(std2)

		print("ROI 2")
		print("T1 = "+ str(val) + " +- "+ str(std) +" s")
		print("T2 = "+ str(val2) + " +- "+ str(std2) +" s")



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


	fig = plt.figure(num = 1, figsize=(20, 20), dpi=120, edgecolor='w')

	outer = gridspec.GridSpec(2, 1, wspace=0, hspace=-0.1, figure=fig,
				height_ratios=(0.5, 0.5))

	top = gridspec.GridSpecFromSubplotSpec(1, 3,
			subplot_spec=outer[0], wspace=0.4, hspace=0,
			width_ratios=(0.26,0.37,0.37))



	# LL reference T1 map

	ax1 = fig.add_subplot(top[0])

	reft1_m = np.ma.masked_equal(reft1, 0)

	im = ax1.imshow(reft1_m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

	# Add Layer with ROIs
	for i in range(len(rois)):

		# Single color for ROI
		cmap_roi = colors.ListedColormap(COLORS[i])
		roi_tmp = np.ma.masked_equal(rois[i], 0)
		
		# Plot ROI as overlay
		im = ax1.imshow(roi_tmp, origin='lower', cmap=cmap_roi, alpha=0.6)

		# Add arrow pointing to ROI
		ybase = np.min(np.where(1 == roi_tmp)[0])
		xbase = np.max(np.where(1 == roi_tmp)[1])
		# ax1.arrow(xbase+20, ybase+20, -12, -12, head_width=5, color=COLORS[i])
		ax1.text(xbase+10, ybase, 'ROI '+str(i+1), fontsize=FS-5, fontweight='bold', color=COLORS[i])

	# Recreate Colorbar from image
	im = ax1.imshow(reft1_m, origin='lower', visible=False, cmap=my_cmap, vmax=VMAX, vmin=VMIN)

	divider2 = make_axes_locatable(ax1)
	cax2 = divider2.append_axes("bottom", size="5%", pad=0.05)
	cbar = plt.colorbar(im, cax=cax2, orientation="horizontal")
	cbar.set_label("T$_1$ / s", fontsize=FS)
	cbar.ax.tick_params(labelsize=FS)

	ax1.set_yticklabels([])
	ax1.set_xticklabels([])
	ax1.xaxis.set_ticks_position('none')
	ax1.yaxis.set_ticks_position('none')
	# ax1.set_axis_off()

	ax1.set_ylabel("Look-Locker", fontsize=FS)
	ax1.set_title("Reference T$_1$", fontsize=FS)

	ax1.text(0.03*np.shape(reft1_m)[0], 0.03*np.shape(reft1_m)[0], '$\\bf{T}_{1,LL}$', fontsize=FS-5, color=TCOLOR)
	
	fig.add_subplot(ax1)


	# T1 vs FA plot

	ax1 = fig.add_subplot(top[1])

	# ROI 1 values

	ax1.errorbar(fa, t1_values, yerr=t1_std, color=COLORS[0], ls='none', marker='o', markersize=MS, label="ROI 1")

	# Fit data linearly
	popt, pcov = curve_fit(func, fa, t1_values, p0=(1, 1))
	perr = np.sqrt(np.diag(pcov))
	# Add fit line to plot
	fa2 = np.linspace(0.9*np.min(fa), 1.05*np.max(fa), 100)
	fit1 = func(fa2, popt[0], popt[1])
	ax1.plot(fa2, fit1, ':', color=COLORS[0], linewidth=LW, label="fit 1")
	# Save fitting results
	text = "\multirow{2}{*}{$T_1$}" \
	        + '''&''' \
		+ "1" \
	        + '''&''' \
	        + str( np.round(popt[0], 3) ) +'$\pm$'+str( ceil(perr[0]*1000)/1000 ) \
	        + '''&''' \
	        + str( np.round(popt[1], 3) ) +'$\pm$'+str( ceil(perr[1]*1000)/1000 ) \
		+ r'''\\'''
	texts.append(text)

	# ROI 2 values

	ax1.errorbar(fa, t1_roi2_values, yerr=t1_roi2_std, color=COLORS[1], ls='none', marker='o', markersize=MS, label="ROI 2")
	
	# Fit data linearly
	popt, pcov = curve_fit(func, fa, t1_roi2_values, p0=(1, 1))
	perr = np.sqrt(np.diag(pcov))
	# Add fit line to plot
	fit1 = func(fa2, popt[0], popt[1])
	ax1.plot(fa2, fit1, ':', color=COLORS[1], linewidth=LW, label="fit 2")
	# Save fitting results
	text =  '''&''' \
		+ "2" \
	        + '''&''' \
	        + str( np.round(popt[0], 3) ) +'$\pm$'+str( ceil(perr[0]*1000)/1000 ) \
	        + '''&''' \
	        + str( np.round(popt[1], 3) ) +'$\pm$'+str( ceil(perr[1]*1000)/1000 ) \
		+ r'''\\\hline'''
	texts.append(text)
	


	ax1.set_xlabel('flip angle / $^\circ$', fontsize=FS-5)
	ax1.set_ylabel('T$_1$ / s', fontsize=FS-5)
	# ax1.set_ylabel('T$_1$ - Ref T$_1$', fontsize=FS-5)
	# ax1.legend(shadow=True, fancybox=True, loc='best', fontsize=FS-15)
	ax1.grid("on", color=TCOLOR, alpha=.1, linewidth=.5)

	ax1.xaxis.set_tick_params(labelsize=FS-10)
	ax1.yaxis.set_tick_params(labelsize=FS-10)

	asp = np.diff(ax1.get_xlim())[0] / np.diff(ax1.get_ylim())[0] * 0.92
	ax1.set_aspect(asp)

	fig.add_subplot(ax1)



	# T2 vs FA plot

	ax1 = fig.add_subplot(top[2])

	# ROI 1 values

	ax1.errorbar(fa, t2_values, yerr=t2_std, color=COLORS[0], ls='none', marker='o', markersize=MS, label="ROI 1")

	# Fit data linearly
	popt, pcov = curve_fit(func, fa, t2_values, p0=(1, 1))
	perr = np.sqrt(np.diag(pcov))
	# Add fit line to plot
	fit1 = func(fa2, popt[0], popt[1])
	ax1.plot(fa2, fit1, ':', color=COLORS[0], linewidth=LW, label="fit 1")
	# Save fitting results
	text = "\multirow{2}{*}{$T_2$}" \
	        + '''&''' \
		+ "1" \
	        + '''&''' \
	        + str( np.round(popt[0], 5) ) +'$\pm$'+str( ceil(perr[0]*100000)/100000 ) \
	        + '''&''' \
	        + str( np.round(popt[1], 3) ) +'$\pm$'+str( ceil(perr[1]*1000)/1000 ) \
		+ r'''\\'''
	texts.append(text)


	# ROI 1 values

	ax1.errorbar(fa, t2_roi2_values, yerr=t2_roi2_std, color=COLORS[1], ls='none', marker='o', markersize=MS, label="ROI 2")

	# Fit data linearly
	popt, pcov = curve_fit(func, fa, t2_roi2_values, p0=(1, 1))
	perr = np.sqrt(np.diag(pcov))
	# Add fit line to plot
	fit1 = func(fa2, popt[0], popt[1])
	ax1.plot(fa2, fit1, ':', color=COLORS[1], linewidth=LW, label="fit 2")
	# Save fitting results
	text =  '''&''' \
		+ "2" \
	        + '''&''' \
	        + str( np.round(popt[0], 5) ) +'$\pm$'+str( ceil(perr[0]*100000)/100000 ) \
	        + '''&''' \
	        + str( np.round(popt[1], 3) ) +'$\pm$'+str( ceil(perr[1]*1000)/1000 ) \
		+ r'''\\'''
	texts.append(text)
	

	ax1.set_xlabel('flip angle / $^\circ$', fontsize=FS-5)
	ax1.set_ylabel('T$_2$ / s', fontsize=FS-5)
	ax1.legend(fancybox=True, loc='best', fontsize=FS-13, framealpha=0.8)
	ax1.grid("on", color=TCOLOR, alpha=.1, linewidth=.5)

	ax1.xaxis.set_tick_params(labelsize=FS-10)
	ax1.yaxis.set_tick_params(labelsize=FS-10)

	asp = np.diff(ax1.get_xlim())[0] / np.diff(ax1.get_ylim())[0] * 0.92
	ax1.set_aspect(asp)

	ax1.text(-1.1*ax1.get_xlim()[0], 1.03*ax1.get_ylim()[1], 'IR-bSSFP ROI Values', fontsize=FS, color=TCOLOR)

	fig.add_subplot(ax1)



	bottom = gridspec.GridSpecFromSubplotSpec(3, dims[2],
			subplot_spec=outer[1], wspace=0, hspace=-0.2)

	# Bloch T1 map


	for i in range(0, dims[2]):

		ax1 = fig.add_subplot(bottom[i])

		t1m = np.ma.masked_equal(t1[:,:,i], 0)

		im = ax1.imshow(t1m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

		divider = make_axes_locatable(ax1)
		cax = divider.append_axes("right", size="5%", pad=0.05)
		cax.set_visible(False)

		ax1.set_yticklabels([])
		ax1.set_xticklabels([])
		ax1.xaxis.set_ticks_position('none')
		ax1.yaxis.set_ticks_position('none')
		# ax1.set_axis_off()

		if (0 == i):
			ax1.set_title("FA: "+str(int(fa[i]))+"$^\circ$", fontsize=FS-5)
		else:
			ax1.set_title(str(int(fa[i]))+"$^\circ$", fontsize=FS-5)

		fig.add_subplot(ax1)

	# Ensure same scaling as map with colorbar has
	divider = make_axes_locatable(ax1)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	cbar = plt.colorbar(im, cax=cax)
	cbar.set_label("T$_{1,FA}$ / s", fontsize=FS-5)
	cbar.ax.tick_params(labelsize=FS-10)


	# Diff T1 map

	for i in range(0, dims[2]):

		ax1 = fig.add_subplot(bottom[dims[2]+i])

		diff = np.abs(reft1-t1[:,:,i]) * DIFF_SCALING

		diffm = np.ma.masked_equal(diff, 0)

		im = ax1.imshow(diffm, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

		divider = make_axes_locatable(ax1)
		cax = divider.append_axes("right", size="5%", pad=0.05)
		cax.set_visible(False)

		ax1.set_yticklabels([])
		ax1.set_xticklabels([])
		ax1.xaxis.set_ticks_position('none')
		ax1.yaxis.set_ticks_position('none')
		# ax1.set_axis_off()

		if (0 == i):
			ax1.text(-0.3*np.shape(t1m)[0], -0.6*np.shape(t1m)[0], 'IR-bSSFP Reconstructions', fontsize=FS, color=TCOLOR, rotation=90)

		fig.add_subplot(ax1)

	# Ensure same scaling as map with colorbar has
	divider = make_axes_locatable(ax1)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	cbar = plt.colorbar(im, cax=cax)
	cbar.set_label("$|T_{1,LL}-T_{1,FA}|$ / s", fontsize=FS-10)
	cbar.ax.tick_params(labelsize=FS-10)

	# Bloch T2 map

	for i in range(0, dims[2]):

		ax1 = fig.add_subplot(bottom[2*dims[2]+i])

		t2m = np.ma.masked_equal(t2[:,:,i], 0)

		im = ax1.imshow(t2m, origin='lower', cmap=my_cmap2, vmax=VMAX2, vmin=VMIN)

		divider = make_axes_locatable(ax1)
		cax = divider.append_axes("right", size="5%", pad=0.05)
		cax.set_visible(False)

		ax1.set_yticklabels([])
		ax1.set_xticklabels([])
		ax1.xaxis.set_ticks_position('none')
		ax1.yaxis.set_ticks_position('none')
		# ax1.set_axis_off()

		fig.add_subplot(ax1)

	# Ensure same scaling as map with colorbar has
	divider = make_axes_locatable(ax1)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	cbar = plt.colorbar(im, cax=cax)
	cbar.set_label("T$_2$ / s", fontsize=FS-5)
	cbar.ax.tick_params(labelsize=FS-10)


	fig.savefig(outfile + '.png', bbox_inches='tight', transparent=False)


	# --------------------------------------
	#    Save fitting results to txt
	# --------------------------------------

	text=r'''\end{tabular}}'''
	texts.append(text)

	if (os.path.isfile("tables.txt")):
		os.remove("tables.txt")
	
	f = open("tables.txt", "a")
	for t in texts:
		f.write(t+"\n")
	f.close()


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
VMAX2 = 0.08
VMIN = 0

DIFF_MIN_T1 = 0.2
DIFF_MAX_T1 = -0.1

DIFF_MIN_T2 = -0.02
DIFF_MAX_T2 = 0.03


BCOLOR='white'  # Background color
TCOLOR='black'  # Text color



def perform_roi_analysis(paramap, roi):

	segment = paramap * roi

	# Set zeros to be invalid for mean calculation
	segment_m = np.ma.masked_equal(segment, 0)

	return segment_m.mean(), segment_m.std()



if __name__ == "__main__":

	#Error if wrong number of parameters
	if( len(sys.argv) < 7):
		print( "Plotting" )
		print( "#-----------------------------------------------" )
		print( "Usage: create_figure.py <LL T1 map> <Bloch T1 map> <outfile> <ROI 1> ... <ROI N>" )
		exit()

	sysargs = sys.argv

	# Load maps
	ll_map = np.abs(cfl.readcfl(sysargs[1]).squeeze())
	ll_map[ll_map == np.inf] = 0
	
	bloch_short_t1_noShim = np.abs(cfl.readcfl(sysargs[2]).squeeze())
	bloch_short_t1_noShim[bloch_short_t1_noShim == np.inf] = 0

	bloch_short_t2_noShim = np.abs(cfl.readcfl(sysargs[3]).squeeze())
	bloch_short_t2_noShim[bloch_short_t2_noShim == np.inf] = 0

	bloch_short_t1_Shim = np.abs(cfl.readcfl(sysargs[4]).squeeze())
	bloch_short_t1_Shim[bloch_short_t1_Shim == np.inf] = 0

	bloch_short_t2_Shim = np.abs(cfl.readcfl(sysargs[5]).squeeze())
	bloch_short_t2_Shim[bloch_short_t2_Shim == np.inf] = 0


	# Define output filename
	outfile = sysargs[6]

	# Load and stack all passed ROIs
	print("Passed ROIs are:")

	rois = []

	for i in sysargs[7:]:
	
		print("\t", i)

		current_roi = np.abs(cfl.readcfl(i).squeeze())

		rois.append(current_roi)

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
	


	fig = plt.figure(num = 1, figsize=(36, 15), dpi=120, edgecolor='w')

	outer = gridspec.GridSpec(1, 3, wspace=-0.55, hspace=0, figure=fig,
					width_ratios=(0.3,0.4,0.4))

	# left = gridspec.GridSpecFromSubplotSpec(3, 3,
	# 		subplot_spec=outer[0], wspace=0.1, hspace=0,
	# 		width_ratios=(0.2,0.6,0.2), height_ratios=(0.25,0.5,0.25))
	# # --------------------------------------
	# #          Look-Locker T1 map
	# # --------------------------------------

	# ax1 = plt.Subplot(fig, left[4])
	# # Layer with image

	# ll_map_m = np.ma.masked_equal(ll_map, 0)

	# im = ax1.imshow(ll_map_m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

	# # Add Layer with ROIs
	# for i in range(len(rois)):

	# 	# Single color for ROI
	# 	cmap_roi = colors.ListedColormap(COLORS[i])
	# 	roi_tmp = np.ma.masked_equal(rois[i], 0)
		
	# 	# Plot ROI as overlay
	# 	im = ax1.imshow(roi_tmp, origin='lower', cmap=cmap_roi, alpha=0.6)

	# 	# Add arrow pointing to ROI
	# 	ybase = np.min(np.where(1 == roi_tmp)[0])
	# 	xbase = np.max(np.where(1 == roi_tmp)[1])
	# 	# ax1.arrow(xbase+20, ybase+20, -12, -12, head_width=5, color=COLORS[i])
	# 	ax1.text(xbase+10, ybase, 'ROI '+str(i+1), fontsize=FS+5, fontweight='bold', color=COLORS[i])

	# # Recreate Colorbar from image
	# im = ax1.imshow(ll_map_m, origin='lower', visible=False, cmap=my_cmap, vmax=VMAX, vmin=VMIN)

	# divider2 = make_axes_locatable(ax1)
	# cax2 = divider2.append_axes("bottom", size="5%", pad=0.05)
	# cbar = plt.colorbar(im, cax=cax2, orientation="horizontal")
	# cbar.set_label("T$_1$ / s", fontsize=FS)
	# cbar.ax.tick_params(labelsize=FS)

	# ax1.set_yticklabels([])
	# ax1.set_xticklabels([])
	# ax1.xaxis.set_ticks_position('none')
	# ax1.yaxis.set_ticks_position('none')
	# # ax1.set_axis_off()

	# ax1.set_title("T$_1$ from IR FLASH", fontsize=FS+5)

	# ax1.text(0.03*np.shape(ll_map_m)[0], 0.03*np.shape(ll_map_m)[0], '$\\bf{T}_{1,F}$', fontsize=FS+5, color=TCOLOR)

	# fig.add_subplot(ax1)

	# --------------------------------------
	#           Bloch T1 map No Shim
	# --------------------------------------

	cleft = gridspec.GridSpecFromSubplotSpec(2, 1,
			subplot_spec=outer[0], wspace=0, hspace=0.1)

	ax2 = plt.Subplot(fig, cleft[0])

	bloch_short_t1_noShimm = np.ma.masked_equal(bloch_short_t1_noShim, 0)

	im2 = ax2.imshow(bloch_short_t1_noShimm, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

	# Ensure same scaling as map with colorbar has
	# divider = make_axes_locatable(ax2)
	# cax = divider.append_axes("bottom", size="5%", pad=0.05)
	# cax.set_visible(False)

	ax2.set_yticklabels([])
	ax2.set_xticklabels([])
	ax2.xaxis.set_ticks_position('none')
	ax2.yaxis.set_ticks_position('none')
	# ax2.set_axis_off()

	ax2.set_title("RING", fontsize=FS+5)
	ax2.set_ylabel("T$_1$ / s", fontsize=FS+5)
	# ax2.set_ylabel("short RF", fontsize=FS)

	ax2.text(0.03*np.shape(bloch_short_t1_noShimm)[0], 0.03*np.shape(bloch_short_t1_noShimm)[0], '$\\bf{T}_{1,B}$', fontsize=FS+5, color=TCOLOR)

	fig.add_subplot(ax2)

	# --------------------------------------
	#           Bloch T2 map No Shim
	# --------------------------------------

	ax2 = plt.Subplot(fig, cleft[1])

	bloch_short_t2_noShimm = np.ma.masked_equal(bloch_short_t2_noShim, 0)

	im2 = ax2.imshow(bloch_short_t2_noShimm, origin='lower', cmap=my_cmap2, vmax=VMAX2, vmin=VMIN)

	# Ensure same scaling as map with colorbar has
	# divider = make_axes_locatable(ax2)
	# cax = divider.append_axes("bottom", size="5%", pad=0.05)
	# cax.set_visible(False)

	ax2.set_yticklabels([])
	ax2.set_xticklabels([])
	ax2.xaxis.set_ticks_position('none')
	ax2.yaxis.set_ticks_position('none')
	# ax2.set_axis_off()

	ax2.set_ylabel("T$_2$ / s", fontsize=FS+5)

	ax2.text(0.03*np.shape(bloch_short_t2_noShimm)[0], 0.03*np.shape(bloch_short_t2_noShimm)[0], '$\\bf{T}_{2,B}$', fontsize=FS+5, color=TCOLOR)

	fig.add_subplot(ax2)

	# --------------------------------------
	#           Bloch T1 map Prior Shim
	# --------------------------------------

	rleft = gridspec.GridSpecFromSubplotSpec(2, 1,
			subplot_spec=outer[1], wspace=0, hspace=0.1)

	ax2 = plt.Subplot(fig, rleft[0])

	bloch_short_t1_Shimm = np.ma.masked_equal(bloch_short_t1_Shim, 0)

	im2 = ax2.imshow(bloch_short_t1_Shimm, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

	divider = make_axes_locatable(ax2)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	cbar = plt.colorbar(im2, cax=cax, orientation="vertical")
	# cbar.set_label("$|T_{1,F}-T_{1,B}|$ / s", fontsize=FS)
	cbar.ax.tick_params(labelsize=FS)

	ax2.set_title("Gradient Delays", fontsize=FS+5)

	ax2.set_yticklabels([])
	ax2.set_xticklabels([])
	ax2.xaxis.set_ticks_position('none')
	ax2.yaxis.set_ticks_position('none')
	# ax2.set_axis_off()

	ax2.text(0.03*np.shape(bloch_short_t1_Shimm)[0], 0.03*np.shape(bloch_short_t1_Shimm)[0], '$\\bf{T}_{1,B,GD}$', fontsize=FS+5, color=TCOLOR)

	fig.add_subplot(ax2)

	
	# --------------------------------------
	#           Bloch T2 map Prior Shim
	# --------------------------------------

	ax3 = plt.Subplot(fig, rleft[1])

	bloch_short_t2_Shimm = np.ma.masked_equal(bloch_short_t2_Shim, 0)

	im2 = ax3.imshow(bloch_short_t2_Shimm, origin='lower', cmap=my_cmap2, vmax=VMAX2, vmin=VMIN)

	divider = make_axes_locatable(ax3)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	cbar = plt.colorbar(im2, cax=cax, orientation="vertical")
	# cbar.set_label("$|T_{2,F}-T_{2,B}|$ / s", fontsize=FS)
	cbar.ax.tick_params(labelsize=FS)

	ax3.set_yticklabels([])
	ax3.set_xticklabels([])
	ax3.xaxis.set_ticks_position('none')
	ax3.yaxis.set_ticks_position('none')
	# ax3.set_axis_off()

	ax3.text(0.03*np.shape(bloch_short_t2_Shimm)[0], 0.03*np.shape(bloch_short_t2_Shimm)[0], '$\\bf{T}_{2,B,GD}$', fontsize=FS+5, color=TCOLOR)


	fig.add_subplot(ax3)

	


	# --------------------------------------
	#           Bloch T1 map Difference
	# --------------------------------------

	right = gridspec.GridSpecFromSubplotSpec(2, 1,
			subplot_spec=outer[2], wspace=0, hspace=0.1)

	ax2 = plt.Subplot(fig, right[0])

	diff_map = bloch_short_t1_noShim - bloch_short_t1_Shim

	diff_map_m = np.ma.masked_equal(diff_map, 0)

	im3 = ax2.imshow(diff_map_m, origin='lower', cmap=my_cmap, vmax=DIFF_MAX_T1, vmin=DIFF_MIN_T1)

	# Create colorbar and remove it to keep same scaling as other figures
	divider = make_axes_locatable(ax2)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	cbar = plt.colorbar(im3, cax=cax, orientation="vertical")
	# cbar.set_label("$|T_{1,F}-T_{1,B}|$ / s", fontsize=FS)
	cbar.ax.tick_params(labelsize=FS)


	ax2.set_yticklabels([])
	ax2.set_xticklabels([])
	ax2.xaxis.set_ticks_position('none')
	ax2.yaxis.set_ticks_position('none')
	# ax2.set_axis_off()

	ax2.set_title("Differences", fontsize=FS+5)

	ax2.text(0.03*np.shape(diff_map_m)[0], 0.03*np.shape(diff_map_m)[0], '$\\bf{T}_{1,B}-\\bf{T}_{1,B,GD}$', fontsize=FS, color=TCOLOR)

	fig.add_subplot(ax2)

	# --------------------------------------
	#           Bloch T2 map Difference
	# --------------------------------------

	ax3 = plt.Subplot(fig, right[1])

	diff_map = bloch_short_t2_noShim - bloch_short_t2_Shim

	diff_map_m = np.ma.masked_equal(diff_map, 0)

	im3 = ax3.imshow(diff_map_m, origin='lower', cmap=my_cmap2, vmax=DIFF_MAX_T2, vmin=DIFF_MIN_T2)

	divider = make_axes_locatable(ax3)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	cbar = plt.colorbar(im3, cax=cax, orientation="vertical")
	# cbar.set_label("$|T_{2,F}-T_{2,B}|$ / s", fontsize=FS)
	cbar.ax.tick_params(labelsize=FS)

	ax3.set_yticklabels([])
	ax3.set_xticklabels([])
	ax3.xaxis.set_ticks_position('none')
	ax3.yaxis.set_ticks_position('none')

	# Add Difference label
	ax3.text(0.03*np.shape(diff_map_m)[0], 0.03*np.shape(diff_map_m)[0], '$\\bf{T}_{2,B}-\\bf{T}_{2,B,GD}$', fontsize=FS, color=TCOLOR)
	
	fig.add_subplot(ax3)

	# --------------------------------------
	#           ROI Analysis
	# --------------------------------------

	ll_values = []
	ll_std = []
	bloch_s_values_t1 = []
	bloch_s_std_t1 = []
	bloch_s_values_t2 = []
	bloch_s_std_t2 = []
	bloch_l_values_t1 = []
	bloch_l_std_t1 = []
	bloch_l_values_t2 = []
	bloch_l_std_t2 = []

	for i in rois:

		lval, lstd = perform_roi_analysis(ll_map, i)
		ll_values.append(lval)
		ll_std.append(lstd)

		bval, bstd = perform_roi_analysis(bloch_short_t1_noShim, i)
		bloch_s_values_t1.append(bval)
		bloch_s_std_t1.append(bstd)

		bval2, bstd2 = perform_roi_analysis(bloch_short_t1_Shim, i)
		bloch_l_values_t1.append(bval2)
		bloch_l_std_t1.append(bstd2)

		bval, bstd = perform_roi_analysis(bloch_short_t2_noShim, i)
		bloch_s_values_t2.append(bval)
		bloch_s_std_t2.append(bstd)

		bval2, bstd2 = perform_roi_analysis(bloch_short_t2_Shim, i)
		bloch_l_values_t2.append(bval2)
		bloch_l_std_t2.append(bstd2)

	# --------------------------------------
	#        Table with ROI Analysis for T1
	# --------------------------------------
	# from matplotlib import rc
	# ax1 = fig.add_subplot(left[3])

	# plt.rc('text', usetex=True)
	# plt.rcParams['font.size'] = '26'

	text=r'''{\renewcommand{\arraystretch}{1.2}\begin{tabular}{c|c|c} $T_1$ [s] & \textbf{ROI 1} & \textbf{ROI 2} \\\hline''' \
	        + ''' IR FLASH & ''' \
	        + str(np.round(ll_values[0],3)) +'$\pm$'+str(ceil(ll_std[0]*1000)/1000 ) \
	        + '''&''' \
	        + str(np.round(ll_values[1],3)) +'$\pm$'+str(ceil(ll_std[1]*1000)/1000 ) \
	        + r'''\\''' \
	        + ''' Short RF & ''' \
	        + str(np.round(bloch_s_values_t1[0],3)) +'$\pm$'+str(ceil(bloch_s_std_t1[0]*1000)/1000 ) \
	        + '''&''' \
	        + str(np.round(bloch_s_values_t1[1],3)) +'$\pm$'+str(ceil(bloch_s_std_t1[1]*1000)/1000 ) \
	        + r'''\\''' \
	        + ''' Long RF & ''' \
	        + str(np.round(bloch_l_values_t1[0],3)) +'$\pm$'+str(ceil(bloch_l_std_t1[0]*1000)/1000 ) \
	        + '''&''' \
	        + str(np.round(bloch_l_values_t1[1],3)) +'$\pm$'+str(ceil(bloch_l_std_t1[1]*1000)/1000 ) \
	        + '''\end{tabular}}'''

	# ax1.text(0.48,0.5, text, ha="center", va="center", transform=ax1.transAxes)

	# ax1.set_yticklabels([])
	# ax1.set_xticklabels([])
	# ax1.xaxis.set_ticks_position('none')
	# ax1.yaxis.set_ticks_position('none')
	# ax1.set_axis_off()


	# --------------------------------------
	#        Table with ROI Analysis for T2
	# --------------------------------------
	# from matplotlib import rc
	# ax1 = fig.add_subplot(left[6])

	# plt.rc('text', usetex=True)
	# plt.rcParams['font.size'] = '28'

	text2=r'''{\renewcommand{\arraystretch}{1.2}\begin{tabular}{c|c|c} $T_2$ [s] & \textbf{ROI 1} & \textbf{ROI 2} \\\hline''' \
	        + ''' Short RF & ''' \
	        + str(np.round(bloch_s_values_t2[0],3)) +'$\pm$'+str(ceil(bloch_s_std_t2[0]*1000)/1000 ) \
	        + '''&''' \
	        + str(np.round(bloch_s_values_t2[1],3)) +'$\pm$'+str(ceil(bloch_s_std_t2[1]*1000)/1000 ) \
	        + r'''\\''' \
	        + ''' Long RF & ''' \
	        + str(np.round(bloch_l_values_t2[0],3)) +'$\pm$'+str(ceil(bloch_l_std_t2[0]*1000)/1000 ) \
	        + '''&''' \
	        + str(np.round(bloch_l_values_t2[1],3)) +'$\pm$'+str(ceil(bloch_l_std_t2[1]*1000)/1000 ) \
	        + '''\end{tabular}}'''

	if (os.path.isfile("tables.txt")):
		os.remove("tables.txt")
	
	f = open("tables.txt", "a")
	f.write(text+"\n")
	f.write(text2)
	f.close()

	# ax1.text(0.48,0.5, text, ha="center", va="center", transform=ax1.transAxes)

	# ax1.set_yticklabels([])
	# ax1.set_xticklabels([])
	# ax1.xaxis.set_ticks_position('none')
	# ax1.yaxis.set_ticks_position('none')
	# ax1.set_axis_off()

	fig.savefig(outfile + '.png', bbox_inches='tight', transparent=False)



	# fig2 = plt.figure(num = 2, dpi=120, edgecolor='w')

	# left = gridspec.GridSpec(1, 1, wspace=0, hspace=0, figure=fig2)

	# ax1 = fig2.add_subplot(left[0])


	# ind = 0

	# ll_all = []
	# bloch_all = []

	# for i in rois:

	# 	tmp = ll_map * i
	# 	tmp2 = bloch_short_t1_Shim * i
	# 	tmp3 = bloch_short_t2_Shim * i

	# 	print(np.shape(tmp))
	# 	print(np.shape(tmp2))

	# 	for x in range(0, np.shape(tmp)[0]):
	# 		for y in range(0, np.shape(tmp)[1]):

	# 			if (0 == i[x,y]):
	# 				continue

	# 			# print(tmp[x,y], tmp2[x,y])
	# 			ll_all.append(tmp[x,y])
	# 			bloch_all.append(tmp3[x,y]/tmp2[x,y])

	# 			ax1.scatter(tmp[x,y], tmp3[x,y]/tmp2[x,y], color=COLORS[ind])
	# 	ind += 1

	# # Fit data linearly

	# ll_all = np.array(ll_all)
	# bloch_all = np.array(bloch_all)

	# xdata = np.linspace(np.min(ll_all), np.max(ll_all), 100)

	# popt, pcov = curve_fit(func, ll_all, bloch_all) #, bounds=(0, [3., 1., 0.5]))

	# print(popt)

	# ax1.plot(xdata, func(xdata, *popt), '-', color='k', label='fit: m=%5.3f, b=%5.3f' % tuple(popt))

	# ax1.set_xlabel("T1 Look-Locker", fontsize=FS)
	# ax1.set_ylabel("T2/T1 Bloch", fontsize=FS)

	# ax1.tick_params(axis='both', which='major', labelsize=FS-3)
	# ax1.grid("on", color=TCOLOR, alpha=.1, linewidth=.5)
	# asp = np.diff(ax1.get_xlim())[0] / np.diff(ax1.get_ylim())[0]
	# ax1.set_aspect(asp)
	# ax1.legend(fontsize=FS-20)

	# fig2.savefig(outfile + '_2.png', bbox_inches='tight', transparent=False)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 09:37:58 2018

@author: nscho
"""

import os
import sys
import copy
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import colors
from math import ceil
from mpl_toolkits.axes_grid1 import make_axes_locatable

sys.path.insert(0, os.path.join(os.environ['TOOLBOX_PATH'], 'python'))
import cfl


def perform_roi_analysis(paramap, roi):

	segment = paramap * roi

	# Set zeros to be invalid for mean calculation
	segment_m = np.ma.masked_equal(segment, 0)

	return segment_m.mean(), segment_m.std()


def bSSFP_fit_func(t, a, b, c): #Schmitt, Griswold et al. 2004
	return np.abs(a - ( b + a ) * np.exp( -1 / c * t ))

FS=12
LW=2

DARK = 0 #dark layout?

VMAX = 600
VMIN = 0

GAMMA = 267.513E6   #[rad Hz/T]

GRAD = 12E-3   #[T/m]

BCOLOR='white'  # Background color
TCOLOR='black'  # Text color

if __name__ == "__main__":

	# Error if more than 1 argument
	if (len(sys.argv) < 6):
		print("plot_simulation.py: ...")
		print("Usage: python3 plot_simulation.py <savename> <values[txt]> <signals [cfl]> <b0map> <ROIs>")
		exit()

	sysargs = sys.argv

	filename = sysargs[1]

	off = np.loadtxt(sysargs[2], unpack=True)

	# Import slice profile data

	data = np.abs(cfl.readcfl(sysargs[3]).squeeze())
	print(np.shape(data))

	b0map = np.abs(cfl.readcfl(sysargs[4]).squeeze())

	# Load and stack all passed ROIs
	print("Passed ROIs are:")

	rois = []

	for i in sysargs[5:]:
	
		print("\t", i)

		current_roi = np.abs(cfl.readcfl(i).squeeze())

		rois.append(current_roi)


	# Estimate signal
	sig = np.sqrt(data[0,:,:] * data[0,:,:] + data[1,:,:] * data[1,:,:])
	print(np.shape(sig))

	tr = 0.0045
	time = np.linspace(tr, np.shape(sig)[0]*tr, np.shape(sig)[0])

	# --------------------------------------
	#         Create visualization
	# --------------------------------------

	COLORS = ['darkorange', 'r', 'g', 'b', 'm', 'y', 'c', 'k', 'w']
	
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

	fig, ax = plt.subplots(1, 2, dpi=120)

	# --------------------------------------
	#         	B0 MAP
	# --------------------------------------

	b0map_m = np.ma.masked_equal(b0map, 0)

	im = ax[0].imshow(b0map_m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

	# Add Layer with ROIs
	for i in range(len(rois)):

		# Single color for ROI
		cmap_roi = colors.ListedColormap(COLORS[i])
		roi_tmp = np.ma.masked_equal(rois[i], 0)
		
		# Plot ROI as overlay
		im = ax[0].imshow(roi_tmp, origin='upper', cmap=cmap_roi, alpha=0.6)

		# Add arrow pointing to ROI
		ybase = np.min(np.where(1 == roi_tmp)[0])
		xbase = np.max(np.where(1 == roi_tmp)[1])
		# ax[0].arrow(xbase+20, ybase+20, -12, -12, head_width=5, color=COLORS[i])
		ax[0].text(xbase+10, ybase, 'ROI '+str(i+1), fontsize=FS+5, fontweight='bold', color=COLORS[i])

	# Recreate Colorbar from image
	im = ax[0].imshow(b0map_m, origin='upper', visible=False, cmap=my_cmap, vmax=VMAX, vmin=VMIN)

	divider2 = make_axes_locatable(ax[0])
	cax2 = divider2.append_axes("bottom", size="5%", pad=0.05)
	cbar = plt.colorbar(im, cax=cax2, orientation="horizontal")
	cbar.set_label("$\Delta$B$_0$ / (rad/s)", fontsize=FS)	
	cbar.ax.tick_params(labelsize=FS-5)

	ax[0].set_yticklabels([])
	ax[0].set_xticklabels([])
	ax[0].xaxis.set_ticks_position('none')
	ax[0].yaxis.set_ticks_position('none')
	# ax[0].set_axis_off()


	# --------------------------------------
	#         Extract Off-Resonance
	# --------------------------------------

	off_values = []

	for i in rois:

		oval, ostd = perform_roi_analysis(b0map, i)
		off_values.append(oval)

		print("Off-resonance = "+ str(oval) + " rad/s")

	# --------------------------------------
	#         Print Signal and Perform Fit
	# --------------------------------------	

	texts = []

	text=r'''{\renewcommand{\arraystretch}{1.2}\begin{tabular}{c|c|c|c} $\omega$ [rad/s] & $T_1$ [s] & $T_2$ [s] & $M_0$ [a.u.] \\\hline'''
	texts.append(text)

	for i in range(0, np.shape(sig)[1]):

		fa = 45 / 180 * np.pi

		# Do fitting
		popt, pcov = curve_fit(bSSFP_fit_func, time, sig[:,i], p0=(1, 1, 1))

		#calculate error
		perr = np.sqrt(np.diag(pcov))

		#Store data
		sst  = popt[0]
		s0  = popt[1]
		t1s = popt[2]

		fit = bSSFP_fit_func(time, sst, s0, t1s)

		#Calculate Parameter from fit 
		t1 = ( t1s * ( s0 / sst ) * np.cos( fa / 2 ) )  #T1 [s]
		t2 = ( t1s * ( np.sin( fa / 2 ) )**2 * 1 / ( 1 - ( sst / s0 ) * np.cos( fa / 2 ) ) ) #T2 [s]
		m0 = s0 / ( np.sin( fa / 2 ) )

		#Determine their errors following the gaussian-error-propagation for ibSSFP
		err_t1 = np.sqrt( perr[2]**2 * (s0/sst*np.cos(fa/2))**2 + \
				perr[1]**2 * (t1s/sst*np.cos(fa/2))**2 + \
				perr[0]**2 * (-t1s*s0/(sst**2)*np.cos(fa/2)) )
		err_t2 = np.sqrt( perr[2]**2 * ( (np.sin(fa/2)*np.sin(fa/2))/(1-sst/s0*np.cos(fa/2)) )**2 + \
				perr[1]**2 * ( -t1s*np.sin(fa/2)*np.sin(fa/2) / (1-sst/s0*np.cos(fa/2))**2 * (sst/s0/s0*np.cos(fa/2)) )**2 + \
				perr[0]**2 * ( -t1s*np.sin(fa/2)*np.sin(fa/2) / (1-sst/s0*np.cos(fa/2))**2 * (-np.cos(fa/2)/s0) )**2 )
		err_m0 = perr[1]/(np.sin(fa/2))

		text = str( off[i] ) \
	        + '''&''' \
	        + str( np.round(t1, 3) ) +'$\pm$'+str( ceil(err_t1*1000)/1000 ) \
	        + '''&''' \
	        + str( np.round(t2, 3) ) +'$\pm$'+str( ceil(err_t2*1000)/1000 ) \
		+ '''&''' \
	        + str( np.round(m0, 3) ) +'$\pm$'+str( ceil(err_m0*1000)/1000 ) \
		+ r'''\\''' 
	
		texts.append(text)

		print(text)

		fit = bSSFP_fit_func(time, sst, s0, t1s)


		# Plot simulated signal
		ax[1].plot(time, sig[:,i], '.', color=COLORS[i], label='$\Delta$B$_0$= '+str(off[i])+' rad/s')

		# Plot simulated signal
		ax[1].plot(time, fit, '-', color=COLORS[i])

	text=r'''\end{tabular}}'''
	texts.append(text)
	
	ax[1].set_xlabel('time / s', fontsize=FS)
	ax[1].set_ylabel('IR-bSSFP Signal', fontsize=FS)
	ax[1].set_title('Ref: T$_1$=0.834 s, T$_2$=0.08 s', fontsize=FS)
	ax[1].legend(shadow=True, fancybox=True, loc=1, fontsize=FS-4)
	ax[1].grid("on", color=TCOLOR, alpha=.1, linewidth=.5)

	asp = np.diff(ax[1].get_xlim())[0] / np.diff(ax[1].get_ylim())[0]
	ax[1].set_aspect(asp)

	fig.tight_layout()


	if (os.path.isfile("tables.txt")):
		os.remove("tables.txt")

	f = open("tables.txt", "a")

	for t in texts:
		f.write(t+"\n")
	f.close()

	fig.savefig(filename+".png", bbox_inches='tight', transparent=False)



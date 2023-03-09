#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 09:37:58 2018

@author: nscho
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from math import ceil
from matplotlib import colors
import copy
import matplotlib.cm as cm

sys.path.insert(0, os.path.join(os.environ['TOOLBOX_PATH'], 'python'))
import cfl

FS=28
LW=7
MS=15

DARK = 0 #dark layout?

COLORS = ['darkorange', 'r', 'g', 'b', 'm', 'y', 'c', 'k', 'w']

VMAX = 2.9
VMIN = 0

GAMMA = 267.513E6   #[rad Hz/T]

GRAD = 12E-3   #[T/m]

BCOLOR='white'  # Background color
TCOLOR='black'  # Text color


def bSSFP_fit_func(t, a, b, c): #Schmitt, Griswold et al. 2004
	return a - ( b + a ) * np.exp( -1 / c * t )


def sst_func(tr1, t1, t2, fa):
	
	e1 = np.exp(-tr1/t1)
	e2 = np.exp(-tr1/t2)

	return (1-e1) * np.sin(fa * np.pi/180) / (1 - (e1-e2) * np.cos(fa * np.pi/180) - e1*e2)



if __name__ == "__main__":

	# Error if more than 1 argument
	if (len(sys.argv) < 8):
		print("plot_simulation.py: ...")
		print("Usage: python3 plot_simulation.py <T1map[cfl]> <T1map HP[cfl]> <ref-values[cfl]> <meas-signal[cfl]> <simu- signal[cfl]> <savename> <ROI 1> ... <ROI N>")
		exit()

	sysargs = sys.argv

	# Prepare output txt files

	texts = []

	text=r'''{\renewcommand{\arraystretch}{1.2}\begin{tabular}{c|c|c}  & $T_1$ [s] & $T_2$ [s] \\\hline'''
	texts.append(text)

	# Import files

	t1map = np.real(cfl.readcfl(sysargs[1]).squeeze())

	t1map_hp = np.real(cfl.readcfl(sysargs[2]).squeeze())

	ref = np.real(cfl.readcfl(sysargs[3]).squeeze())
 
	t1_m = np.ma.masked_equal(ref[:,:,0,:], 0)
	t1 = t1_m.mean(axis=(0,1))
	t1std = t1_m.std(axis=(0,1))

	t2_m = np.ma.masked_equal(ref[:,:,1,:], 0)
	t2 = t2_m.mean(axis=(0,1))
	t2std = t2_m.std(axis=(0,1))

	b1_m = np.ma.masked_equal(ref[:,:,2,:], 0)
	b1 = b1_m.mean(axis=(0,1))
	b1std = b1_m.std(axis=(0,1))

	t1_hp_m = np.ma.masked_equal(ref[:,:,3,:], 0)
	t1_hp = t1_hp_m.mean(axis=(0,1))
	t1_hpstd = t1_hp_m.std(axis=(0,1))

	t2_hp_m = np.ma.masked_equal(ref[:,:,4,:], 0)
	t2_hp = t2_hp_m.mean(axis=(0,1))
	t2_hpstd = t2_hp_m.std(axis=(0,1))


	text = "Full Model (Bloch) ROI 0" \
	        + '''&''' \
	        + str( np.round(t1[0], 3) ) +'$\pm$'+str( ceil(t1std[0]*1000)/1000 ) \
	        + '''&''' \
	        + str( np.round(t2[0], 3) ) +'$\pm$'+str( ceil(t2std[0]*1000)/1000 ) \
		+ r'''\\'''
	texts.append(text)


	text = "Analy. Approx. (Bloch) ROI 0" \
	        + '''&''' \
	        + str( np.round(t1_hp[0], 3) ) +'$\pm$'+str( ceil(t1_hpstd[0]*1000)/1000 ) \
	        + '''&''' \
	        + str( np.round(t2_hp[0], 3) ) +'$\pm$'+str( ceil(t2_hpstd[0]*1000)/1000 ) \
		+ r'''\\'''
	texts.append(text)

	text = "Full Model (Bloch) ROI 1" \
	        + '''&''' \
	        + str( np.round(t1[1], 3) ) +'$\pm$'+str( ceil(t1std[1]*1000)/1000 ) \
	        + '''&''' \
	        + str( np.round(t2[1], 3) ) +'$\pm$'+str( ceil(t2std[1]*1000)/1000 ) \
		+ r'''\\'''
	texts.append(text)


	text = "Analy. Approx. (Bloch) ROI 1" \
	        + '''&''' \
	        + str( np.round(t1_hp[1], 3) ) +'$\pm$'+str( ceil(t1_hpstd[1]*1000)/1000 ) \
	        + '''&''' \
	        + str( np.round(t2_hp[1], 3) ) +'$\pm$'+str( ceil(t2_hpstd[1]*1000)/1000 ) \
		+ r'''\\'''
	texts.append(text)

	print(t1, t2, b1, t1_hp, t2_hp)

	roi_data = np.real(cfl.readcfl(sysargs[4]).squeeze()) # [BR, BR, time, #ROI]
	roi_m = np.ma.masked_equal(roi_data, 0)
	roi = roi_m.mean(axis=(0,1))
	roistd = roi_m.std(axis=(0,1))

	data = np.real(cfl.readcfl(sysargs[5]).squeeze()) # [(x,y,z), time, #ROI]

	filename = sysargs[6]

	# Load and stack all passed ROIs
	print("Passed ROIs are:")

	rois = []

	for i in sysargs[7:]:
	
		print("\t", i)

		current_roi = np.abs(cfl.readcfl(i).squeeze())

		rois.append(current_roi)

	# --------------------------------------
	#         	Perform Fit
	# --------------------------------------

	# Analysis ROI #0

	fa = 45 * b1[0]
	far = fa*np.pi/180
	av = 5

	tr1 = 0.0045
	tinv = 0.01
	tinvspoil = 0.005

	time1 = np.linspace((tr1*av)/2, np.shape(data)[1]*tr1*av+(tr1*av)/2, np.shape(data)[1])

	# Do fitting
	popt, pcov = curve_fit(bSSFP_fit_func, time1, roi[:,0]/roi[0,0], p0=(1, 1, 1))

	#calculate error
	perr = np.sqrt(np.diag(pcov))

	#Store data
	sst  = popt[0]
	s0  = popt[1]
	t1s = popt[2]

	fit = bSSFP_fit_func(time1, sst, s0, t1s)

	#Calculate Parameter from fit 
	t1 = ( t1s * ( s0 / sst ) * np.cos( far / 2 ) )  #T1 [s]
	t2 = ( t1s * ( np.sin( far / 2 ) )**2 * 1 / ( 1 - ( sst / s0 ) * np.cos( far / 2 ) ) ) #T2 [s]
	m0 = s0 / ( np.sin( far / 2 ) )

	#Determine their errors following the gaussian-error-propagation for ibSSFP
	err_t1 = np.sqrt( perr[2]**2 * (s0/sst*np.cos(far/2))**2 + \
			perr[1]**2 * (t1s/sst*np.cos(far/2))**2 + \
			perr[0]**2 * (-t1s*s0/(sst**2)*np.cos(far/2)) )
	err_t2 = np.sqrt( perr[2]**2 * ( (np.sin(far/2)*np.sin(far/2))/(1-sst/s0*np.cos(far/2)) )**2 + \
			perr[1]**2 * ( -t1s*np.sin(far/2)*np.sin(far/2) / (1-sst/s0*np.cos(far/2))**2 * (sst/s0/s0*np.cos(far/2)) )**2 + \
			perr[0]**2 * ( -t1s*np.sin(far/2)*np.sin(far/2) / (1-sst/s0*np.cos(far/2))**2 * (-np.cos(far/2)/s0) )**2 )
	err_m0 = perr[1]/(np.sin(far/2))

	text = '---- Fitted Parameter for IR bSSFP ----\n'+\
		'| Parameter | Value±Error |\n'\
		'| :---: | :---: |\n'\
		'| T1 [s] | '+str( np.round(t1, 3) )+'±'+str( ceil(err_t1*1000)/1000 )+ ' |\n'+\
		'| T2 [s] | '+str( np.round(t2, 3) )+'±'+str( ceil(err_t2*1000)/1000 )+ ' |\n'+\
		'| M0 [a.u.] | '+str( np.round(m0, 3) )+'±'+str( ceil(err_m0*1000)/1000 )+ ' |'

	print(text)

	text = "Analytical Fit ROI 0" \
	        + '''&''' \
	        + str( np.round(t1, 3) ) +'$\pm$'+str( ceil(err_t1*1000)/1000 ) \
	        + '''&''' \
	        + str( np.round(t2, 3) ) +'$\pm$'+str( ceil(err_t2*1000)/1000 ) \
		+ r'''\\'''
	texts.append(text)


	# Analysis ROI #1

	fa = 45 * b1[1]
	far = fa*np.pi/180
	av = 5

	tr1 = 0.0045
	tinv = 0.01
	tinvspoil = 0.005

	time1 = np.linspace((tr1*av)/2, np.shape(data)[1]*tr1*av+(tr1*av)/2, np.shape(data)[1])

	# Do fitting
	popt, pcov = curve_fit(bSSFP_fit_func, time1, roi[:,1]/roi[0,1], p0=(1, 1, 1))

	#calculate error
	perr = np.sqrt(np.diag(pcov))

	#Store data
	sst  = popt[0]
	s0  = popt[1]
	t1s = popt[2]

	fit1 = bSSFP_fit_func(time1, sst, s0, t1s)

	#Calculate Parameter from fit 
	t1 = ( t1s * ( s0 / sst ) * np.cos( far / 2 ) )  #T1 [s]
	t2 = ( t1s * ( np.sin( far / 2 ) )**2 * 1 / ( 1 - ( sst / s0 ) * np.cos( far / 2 ) ) ) #T2 [s]
	m0 = s0 / ( np.sin( far / 2 ) )

	#Determine their errors following the gaussian-error-propagation for ibSSFP
	err_t1 = np.sqrt( perr[2]**2 * (s0/sst*np.cos(far/2))**2 + \
			perr[1]**2 * (t1s/sst*np.cos(far/2))**2 + \
			perr[0]**2 * (-t1s*s0/(sst**2)*np.cos(far/2)) )
	err_t2 = np.sqrt( perr[2]**2 * ( (np.sin(far/2)*np.sin(far/2))/(1-sst/s0*np.cos(far/2)) )**2 + \
			perr[1]**2 * ( -t1s*np.sin(far/2)*np.sin(far/2) / (1-sst/s0*np.cos(far/2))**2 * (sst/s0/s0*np.cos(far/2)) )**2 + \
			perr[0]**2 * ( -t1s*np.sin(far/2)*np.sin(far/2) / (1-sst/s0*np.cos(far/2))**2 * (-np.cos(far/2)/s0) )**2 )
	err_m0 = perr[1]/(np.sin(far/2))

	text = '---- Fitted Parameter for IR bSSFP ----\n'+\
		'| Parameter | Value±Error |\n'\
		'| :---: | :---: |\n'\
		'| T1 [s] | '+str( np.round(t1, 3) )+'±'+str( ceil(err_t1*1000)/1000 )+ ' |\n'+\
		'| T2 [s] | '+str( np.round(t2, 3) )+'±'+str( ceil(err_t2*1000)/1000 )+ ' |\n'+\
		'| M0 [a.u.] | '+str( np.round(m0, 3) )+'±'+str( ceil(err_m0*1000)/1000 )+ ' |'

	print(text)

	text = "Analytical Fit ROI 1" \
	        + '''&''' \
	        + str( np.round(t1, 3) ) +'$\pm$'+str( ceil(err_t1*1000)/1000 ) \
	        + '''&''' \
	        + str( np.round(t2, 3) ) +'$\pm$'+str( ceil(err_t2*1000)/1000 ) \
		+ r'''\\'''
	texts.append(text)

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

	# --------------------------------------
	#    Steady-State Signal Simulation
	# --------------------------------------

	# Analysis ROI #0

	fa = 45 * b1[0]
	far = fa*np.pi/180

	sst = sst_func(tr1, t1_hp[0], t2_hp[0], fa)
	s0 = np.sin(far/2)
	t1s = 1 / (1/t1_hp[0] * np.cos(far/2)**2 + 1/t2_hp[0] * np.sin(far/2)**2)

	analyt = bSSFP_fit_func(time1, sst, s0, t1s)

	# Analysis ROI #1

	fa = 45 * b1[1]
	far = fa*np.pi/180

	sst = sst_func(tr1, t1_hp[1], t2_hp[1], fa)
	s0 = np.sin(far/2)
	t1s = 1 / (1/t1_hp[1] * np.cos(far/2)**2 + 1/t2_hp[1] * np.sin(far/2)**2)

	analyt1 = bSSFP_fit_func(time1, sst, s0, t1s)


	# --------------------------------------
	#    	     Visualization
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
	

	fig = plt.figure(num = 1, figsize=(50, 10), dpi=120, edgecolor='w')

	outer = gridspec.GridSpec(1, 4, wspace=-0.4, hspace=0, figure=fig,
					width_ratios=(0.22,0.28,0.28,0.22))


	ax1 = plt.Subplot(fig, outer[0])
	# Layer with image

	t1map_m = np.ma.masked_equal(t1map, 0)

	im = ax1.imshow(t1map_m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

	# Add Layer with ROIs
	for i in range(len(rois)):

		# Single color for ROI
		cmap_roi = colors.ListedColormap('black')
		roi_tmp = np.ma.masked_equal(rois[i], 0)
		
		# Plot ROI as overlay
		im = ax1.imshow(roi_tmp, origin='lower', cmap=cmap_roi, alpha=0.6)

		# Add arrow pointing to ROI
		ybase = np.min(np.where(1 == roi_tmp)[0])
		xbase = np.max(np.where(1 == roi_tmp)[1])
		# ax1.arrow(xbase+20, ybase+20, -12, -12, head_width=5, color=COLORS[i])
		ax1.text(xbase+4, ybase-3, 'ROI '+str(i), fontsize=FS+5, fontweight='bold', color='k')

	# Recreate Colorbar from image
	im = ax1.imshow(t1map_m, origin='lower', visible=False, cmap=my_cmap, vmax=VMAX, vmin=VMIN)

	divider2 = make_axes_locatable(ax1)
	cax2 = divider2.append_axes("bottom", size="5%", pad=0.05)
	cbar = plt.colorbar(im, cax=cax2, orientation="horizontal")
	cbar.set_label("T$_1$ / s", fontsize=FS+5)
	cbar.ax.tick_params(labelsize=FS)

	ax1.set_title("Full Bloch Model", fontsize=FS+5)

	ax1.set_yticklabels([])
	ax1.set_xticklabels([])
	ax1.xaxis.set_ticks_position('none')
	ax1.yaxis.set_ticks_position('none')
	# ax1.set_axis_off()

	fig.add_subplot(ax1)



	ax1 = plt.Subplot(fig, outer[1])
	# Layer with image

	t1map_hp_m = np.ma.masked_equal(t1map_hp, 0)

	im = ax1.imshow(t1map_hp_m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

	divider2 = make_axes_locatable(ax1)
	cax2 = divider2.append_axes("bottom", size="5%", pad=0.05)
	cbar = plt.colorbar(im, cax=cax2, orientation="horizontal")
	cbar.set_label("T$_1$ / s", fontsize=FS+5)
	cbar.ax.tick_params(labelsize=FS)

	ax1.set_title("Analyt. Approx. with Bloch", fontsize=FS+5)

	ax1.set_yticklabels([])
	ax1.set_xticklabels([])
	ax1.xaxis.set_ticks_position('none')
	ax1.yaxis.set_ticks_position('none')
	# ax1.set_axis_off()

	fig.add_subplot(ax1)


	# Analysis ROI #0

	ax1 = plt.Subplot(fig, outer[2])

	ax1.plot(time1, -analyt / analyt[0], 'g-', linewidth=LW, label="Analyt. Approx.")
	ax1.plot(time1, -fit / fit[0], 'r-', linewidth=LW, markersize=MS, label="fit")
	ax1.plot(time1, -data[1,:,0]/data[1,0,0], 'b-', linewidth=LW, label="Full Bloch simulation")
	ax1.errorbar(time1, -roi[:,0]/roi[0,0], yerr=roistd[:,0]/roi[0,0], marker='.', color='k', linewidth=LW-3, markersize=MS, alpha=.4, label="RT-NLINV")
	
	ax1.set_xlabel('time / s', fontsize=FS+5)
	ax1.set_ylabel('Scaled Signal', fontsize=FS+5)
	ax1.set_title('ROI 0', fontsize=FS+5)
	ax1.legend(shadow=True, fancybox=True, loc='best', fontsize=FS)
	ax1.grid("on", color=TCOLOR, alpha=.1, linewidth=.5)

	ax1.xaxis.set_tick_params(labelsize=FS)
	ax1.yaxis.set_tick_params(labelsize=FS)

	ax1.set_ylim([-1.05, 0.4])

	asp = np.diff(ax1.get_xlim())[0] / np.diff(ax1.get_ylim())[0] * 1.05 # Colorbar reduces aspect ratio of imshow plot. 0.93 compensates for difference
	ax1.set_aspect(asp)

	fig.add_subplot(ax1)


	# Analysis ROI #1

	ax2 = plt.Subplot(fig, outer[3], sharey=ax1)

	ax2.plot(time1, -analyt1 / analyt1[0], 'g-', linewidth=LW, label="Analyt. Approx.")
	ax2.plot(time1, -fit1 / fit1[0], 'r-', linewidth=LW, markersize=MS, label="fit")
	ax2.plot(time1, -data[1,:,1]/data[1,0,1], 'b-', linewidth=LW, label="Full Bloch simulation") # /data[1,0,0] for same scaling!
	ax2.errorbar(time1, -roi[:,1]/roi[0,1], yerr=roistd[:,1]/roi[0,1], marker='.', color='k', linewidth=LW-3, markersize=MS, alpha=.4, label="RT-NLINV ROI")
	
	ax2.set_xlabel('time / s', fontsize=FS+5)
	ax2.set_title('ROI 1', fontsize=FS+5)
	# ax2.set_ylabel('Scaled Signal', fontsize=FS+5)
	# ax2.legend(shadow=True, fancybox=True, loc='best', fontsize=FS)
	ax2.grid("on", color=TCOLOR, alpha=.1, linewidth=.5)

	ax2.xaxis.set_tick_params(labelsize=FS)
	ax2.yaxis.set_tick_params(labelbottom=False)

	ax2.set_ylim([-1.05, 0.4])

	asp = np.diff(ax2.get_xlim())[0] / np.diff(ax2.get_ylim())[0] * 1.05 # Colorbar reduces aspect ratio of imshow plot. 0.93 compensates for difference
	ax2.set_aspect(asp)

	fig.add_subplot(ax2)

	# fa_percent = np.linspace(0.5, 1.5, 100)
	# fa_array = fa_percent * fa

	# # Compensate for scaling with -1/analyt[0]
	# ax2.plot(fa_percent, -1/analyt[0] * sst_func(tr1, t1, t2, fa_array), 'b.', label="Re(nlinv roi)")
	# ax2.plot([b1, b1], [np.min(-1/analyt[0] * sst_func(tr1, t1, t2, fa_array)), np.max(-1/analyt[0] * sst_func(tr1, t1, t2, fa_array))], 'k-')

	# ax2.grid("on", color=TCOLOR, alpha=.1, linewidth=.5)
	# ax2.set_xlabel('B1', fontsize=FS)
	# ax2.set_ylabel('Scaled Mss', fontsize=FS)


	# plt.tight_layout()

	fig.savefig(filename+".png", bbox_inches='tight', transparent=False)




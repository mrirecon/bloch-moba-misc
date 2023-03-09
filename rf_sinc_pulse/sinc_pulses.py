#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 10:42:41 2018

@author: nscho
"""

import numpy as np
import matplotlib.pyplot as plt
from pylab import savefig

from scipy.fftpack import rfftfreq, rfft

COLORS=['#a6611a', '#018571', '#dfc27d', '#80cdc1']


def sinc_window(A, alpha, N, t0, t):

	rec = np.where(abs(t) <= N*t0, 1, 0)
	
	func = A * ( (1-alpha) + alpha*np.cos(np.pi * t / (N*t0)) ) * np.sinc( np.pi * t / t0 )

	return rec*func



samples = 10000

#number of zero-crossings
nl = 6
nr = 6
n = max(nl, nr)

#amplitude at t=0
A = 1

#half time of main- and full time of side-lopes
t0 = 1

#window type: 0=no, 0.46=Hamming, 0.5=Hanning
alpha = 0.46

time = np.linspace(-(nl+1)*t0, (nr+1)*t0, samples)
time2 = np.linspace(-nl*t0, nr*t0, 10* samples)


#------------------------------------------------------
#--------------- Visualization ------------------------
#------------------------------------------------------
dark = 0 #dark layout?


if(dark):
	plt.style.use(['dark_background'])
else:
	plt.style.use(['default'])

fig = plt.figure(num = 1, figsize=(8, 6), dpi=80, edgecolor='w')

name = 'sinc'

ax1 = fig.add_subplot(1,2,1)
ax1.plot( time, sinc_window( A, 0, n, t0, time ), color=COLORS[0], label='Sinc')
ax1.plot( time, np.where(abs(time) <= nr*t0, 1, 0), ":", color=COLORS[1], label='Rec' )
ax1.set_xlabel('time t [s]', fontsize=15)
ax1.set_ylabel('amplitude [a.u.]', fontsize=15)
ax1.set_xlim([-(nl+1), (nr+1)])
#ax1.grid('on')
asp = np.diff(ax1.get_xlim())[0] / np.diff(ax1.get_ylim())[0]
ax1.set_aspect(asp)
ax1.legend(shadow=True, fancybox=True)


ax2 = fig.add_subplot(1,2,2)
#Do FFT
dt = (time[1] - time[0])
fa = 1 / dt #scan frequency
print(dt, fa)
N = 100000
X = np.linspace(-fa/2, fa/2, N, endpoint=True) # fa/2 = max frequency = nyquist frequency



T = time2[1] - time2[0] #sampling rate
freq = np.fft.fftfreq(time2.shape[-1],T)

#ax2.plot( np.fft.fftshift(freq), np.fft.fftshift( np.abs( np.fft.fft( sinc_window( A, 0, n, t0, time2 ) ) ) ), 'b-', label='FT(Sinc)' )
ax2.plot( X, np.abs(np.fft.fftshift( np.fft.fft( sinc_window( A, 0, n, t0, time ), N ) ) ), '-',  color=COLORS[0] )
#ax2.plot( sample_freq, power, 'r-', label='Sinc' )
ax2.set_xlabel('frequency f [1/Hz]', fontsize=15)
ax2.set_ylabel('amplitude [a.u.]', fontsize=15)
ax2.set_xlim([-5, 5])
#ax2.grid('on')
asp = np.diff(ax2.get_xlim())[0] / np.diff(ax2.get_ylim())[0]
ax2.set_aspect(asp)
# ax2.legend(shadow=True, fancybox=True)


plt.tight_layout()
plt.show(block=False)

fig.savefig( name+".pdf", bbox_inches='tight', transparent=True)


#------------------------------------------------------
#--------------- Visualization 2 ----------------------
#------------------------------------------------------

#number of zero-crossings
nl = 1
nr = 1
n = max(nl, nr)

#amplitude at t=0
A = 1

#half time of main- and full time of side-lopes
t0 = 1

time = np.linspace(-nl*t0, nr*t0, samples)
time2 = np.linspace(-nl*t0, nr*t0, 10* samples)


fig = plt.figure(num = 2, figsize=(8, 6), dpi=80, edgecolor='w')

name2 = 'sinc_window_comparison'

ax1 = fig.add_subplot(1,2,1)
ax1.plot(time, sinc_window( A, 0, n, t0, time ), '-', color=COLORS[0], label='No Window')
ax1.plot(time, sinc_window( A, 0.46, n, t0, time ), '-', color=COLORS[1], label='Hamming')
ax1.plot(time, sinc_window( A, 0.5, n, t0, time ), '-', color=COLORS[2], label='Hanning')
ax1.set_xlabel('time t [s]', fontsize=15)
ax1.set_ylabel('amplitude [a.u.]', fontsize=15)
#ax1.grid('on')

asp = np.diff(ax1.get_xlim())[0] / np.diff(ax1.get_ylim())[0]
ax1.set_aspect(asp)
ax1.legend(shadow=True, fancybox=True)

ax2 = fig.add_subplot(1,2,2)

#Do FFT
dt = (time[1] - time[0])
fa = 1 / dt #scan frequency
print(dt, fa)
N = 100000
X = np.linspace(-fa/2, fa/2, N, endpoint=True) # fa/2 = max frequency = nyquist frequency

T = time[1] - time[0] #sampling rate
freq = np.fft.fftfreq(time2.shape[-1], T)

ax2.plot( X, np.fft.fftshift( np.abs( np.fft.fft( sinc_window( A, 0, n, t0, time ), N ) ) ), '-', color=COLORS[0])
ax2.plot( X, np.fft.fftshift( np.abs( np.fft.fft( sinc_window( A, 0.46, n, t0, time ), N ) ) ), '-', color=COLORS[1])
ax2.plot( X, np.fft.fftshift( np.abs( np.fft.fft( sinc_window( A, 0.5, n, t0, time ), N ) ) ), '-', color=COLORS[2])
ax2.set_xlabel('frequency f [1/Hz]', fontsize=15)
ax2.set_ylabel('amplitude [a.u.]', fontsize=15)
ax2.set_xlim([-5, 5])
#ax2.grid('on')
asp = np.diff(ax2.get_xlim())[0] / np.diff(ax2.get_ylim())[0]
ax2.set_aspect(asp)
# ax2.legend(shadow=True, fancybox=True)


plt.tight_layout()
plt.show(block=False)

fig.savefig(name2+".pdf", bbox_inches='tight', transparent=True)
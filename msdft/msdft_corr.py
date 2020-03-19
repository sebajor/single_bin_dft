from msdft_test import msdft
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import numpy as np

N = 1024
k = 300
phi_1 = np.deg2rad(123)  #2*np.pi/18 #add phase for the signal, phi=20deg
phi_2 = np.deg2rad(23)
n_fft = 5        #number of FFT calculated


t = np.arange(N*n_fft)
signal_1 = 0.2*np.sin(2*np.pi*(k+0.5)*t/N+phi_1)
signal_2 = 0.8*np.sin(2*np.pi*(k+0.5)*t/N+phi_2)


msdft1 = msdft(signal_1,N=N, k=k)[0]
msdft2 = msdft(signal_2,N=N, k=k)[0]

corr_data = msdft2*np.conjugate(msdft1)
rel_pow = 20*(np.log10(np.abs(msdft2))-np.log10(np.abs(msdft1)))

fft_1 = fft(signal_1[:N])[300]
fft_2 = fft(signal_2[:N])[300]
mag = 20*(np.log10(np.abs(fft_2))-np.log10(np.abs(fft_1)))
phase = np.rad2deg(np.angle(fft_2/fft_1))

print('FFT relative magnitude %.4f'%mag)
print('FFT relative phase %.4f'%phase)

fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.plot(np.rad2deg(np.angle(corr_data)))
ax1.set_title('Relative phase')
ax1.set_ylabel('deg')
ax2.plot(rel_pow)
ax2.set_title('Relative power')
ax2.set_ylabel('[dB]')



fig2 = plt.figure()
ax3 = fig2.add_subplot(111)
ax3.plot(np.rad2deg(np.angle(msdft1)), label='msdft1 phase')
ax3.plot(np.rad2deg(np.angle(msdft2)), label='msdft2 phase')
plt.show()





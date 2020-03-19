import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import ipdb


"""
In this script we test the implementation of the msdft
compared to the standard fft algorithm.

The results is that for the bins where the signal is contained
the algorithm behaves correctly and gives similar results.

Note that in this implementation the first value at the twidd
is not 1 in the modulation.
And for the phase recovery we only multiplicate by the twiddle
factor and not demodulate, because...it works.

"""



def msdft(data, N, k):
    """calculate the msdft using the structure in duda
       data = smaples to calculate the dft, the len 
              should be larger than N
       N =  dft lenght
       k = twiddle factor
    """
    if(len(data)<N):
        raise Exception('len(data) should be larger than N!')
    twidd = np.exp(-1j*2*np.pi*k/N)
    prev_data = np.zeros(N)
    actual_twidd = 1
    resonator = 0
    mult_1 = 0
    out = np.zeros(len(data),dtype=complex)
    twidd_values = np.zeros(len(data),dtype=complex)
    for i in range(len(data)):
        comb = data[i]-prev_data[i%N]
        prev_data[i%N] = data[i]
        mult_1 = comb*actual_twidd
        twidd_values[i] = actual_twidd
        phase_mult = np.conjugate(actual_twidd) 
        actual_twidd = actual_twidd*twidd       #W_N**k(n+1)
        resonator = resonator+mult_1
        out[i] = resonator#*np.conjugate(twidd)
    return [out, twidd_values]
    

N = 1024
k = 300
phi = np.deg2rad(123)  #2*np.pi/18 #add phase for the signal, phi=20deg
n_fft = 5        #number of FFT calculated



t = np.arange(N*n_fft)
signal = 0.2*np.sin(2*np.pi*k*t/N+phi)
data_pow = np.zeros([n_fft, N/2])
data_ang = np.zeros([n_fft, N/2])
for i in range(n_fft):
    sig_fft = fft(signal[i*N:(i+1)*N])
    sig_pow = 20*np.log10(np.abs(sig_fft[:N/2]))
    sig_ang = np.rad2deg(np.angle(sig_fft[:N/2]))

    data_pow[i,:] = sig_pow
    data_ang[i,:] = sig_ang


fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.plot(sig_pow)
ax1.set_title('FFT signal power')
ax1.set_xlabel('Twiddle factor')
ax2.plot(sig_ang)
ax2.set_title('FFT signal phase')
ax2.set_xlabel('Twiddle factor')

#msdft calcualtion

msdft_calc = msdft(signal, N=N, k=k)
twidd_values = msdft_calc[1]
msdft_calc = msdft_calc[0]
msdft_pow = 20*np.log10(np.abs(msdft_calc))
msdft_ang = np.rad2deg(np.angle(msdft_calc))

fig2 = plt.figure()
ax3 = fig2.add_subplot(121)
ax4 = fig2.add_subplot(122)
ax3.plot(msdft_pow)
ax3.set_title('Msdft signal power')
ax4.plot(msdft_ang)
ax4.set_title('Msdft signal phase')


for i in range(n_fft-1):
    print('FFT magnitude %.4f [dB] \t Msdft magnitude %.4f [dB]'%(np.max(data_pow[i,300]), msdft_pow[N*(i+1)]))
    print('FFT phase %.4f \t\t Msdft phase %.4f' %(data_ang[i,300], msdft_ang[N*(i+1)]))



print("\nLeakage:")



signal = 0.5*np.sin(2*np.pi*(k+0.5)*t/N+phi)
data_pow = np.zeros([n_fft, N/2])
data_ang = np.zeros([n_fft, N/2])
for i in range(n_fft):
    sig_fft = fft(signal[i*N:(i+1)*N])
    sig_pow = 20*np.log10(np.abs(sig_fft[:N/2]))
    sig_ang = np.rad2deg(np.angle(sig_fft[:N/2]))
    data_pow[i,:] = sig_pow
    data_ang[i,:] = sig_ang


fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.plot(sig_pow)
ax1.set_title('FFT signal power(lekage)')
ax1.set_xlabel('Twiddle factor')
ax2.plot(sig_ang)
ax2.set_title('FFT signal phase(leakage)')
ax2.set_xlabel('Twiddle factor')

#msdft calcualtion

msdft_calc = msdft(signal, N=N, k=k)[0]
msdft_pow = 20*np.log10(np.abs(msdft_calc))
msdft_ang = np.rad2deg(np.angle(msdft_calc))

fig2 = plt.figure()
ax3 = fig2.add_subplot(121)
ax4 = fig2.add_subplot(122)
ax3.plot(msdft_pow)
ax3.set_title('Msdft signal power(leakage)')
ax4.plot(msdft_ang)
ax4.set_title('Msdft signal phase(leakage)')





for i in range(n_fft-1):
    print('FFT magnitude %.4f [dB] \t Msdft magnitude %.4f [dB]'%(np.max(data_pow[i,300]), msdft_pow[N*(i+1)]))
    print('FFT phase %.4f \t\t Msdft phase %.4f' %(data_ang[i,300], msdft_ang[N*(i+1)]))


plt.show()

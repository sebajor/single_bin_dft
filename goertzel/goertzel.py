import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import ipdb

def goertzel(data, N, k):
    twidd = -np.exp(-1j*2*np.pi*k/N)
    re_mult = 2*np.cos(2*np.pi*k/N)
    w_1 = 0
    w_2 = 0
    output = []
    out = 0
    for i in range(len(data)):
        out = re_mult*w_1-w_2+data[i]    
        if((i%(N))==0):
            print('i: '+str(i)+'\t i%N'+str(i%(N+1)))
            val = out+twidd*w_1
            output.append(val)
            w_1 = 0
            w_2 = 0
            out = re_mult*w_1-w_2+data[i]
        w_2 = w_1
        w_1 = out
    return output
    
    


N = 1024
k = 300
phi = np.deg2rad(123)  #2*np.pi/18 #add phase for the signal, phi=20deg
n_fft = 10        #number of FFT calculated


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
 
msdft_calc = goertzel(signal, N=N, k=k)
msdft_calc = msdft_calc
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
    print('FFT magnitude %.4f [dB] \t goertzel magnitude %.4f [dB]'%(np.max(data_pow[i,300]), msdft_pow[i]))
    print('FFT phase %.4f \t\t goertzel phase %.4f' %(data_ang[i,300], msdft_ang[i]))


    
    

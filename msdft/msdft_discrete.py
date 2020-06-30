import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import ipdb
import calandigital as calan


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
    twidd_re = calan.float2fixed(twidd.real, nbits=16, binpt=14)
    twidd_im = calan.float2fixed(twidd.imag, nbits=16, binpt=14)
    twidd = twidd_re/2.**14 + 1j*twidd_im/2.**14
    prev_data = np.zeros(N, dtype=complex)
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



N = 16384
k =  3000
n_fft = 5
t = np.arange(N*n_fft)

#signal = 1./4*np.exp(1j*2*np.pi*k*t/N)
signal = 1./2*np.sin(2*np.pi*k*t/N)
msdft_calc = msdft(signal, N=N, k=k)
msdft_vals = msdft_calc[0]
twidd_vals = msdft_calc[1]









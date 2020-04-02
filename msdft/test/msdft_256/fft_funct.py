import numpy as np
import corr
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct


def plot_fft(_fpga, _bw):
    global fpga, data, bw, freq
    fpga = _fpga
    bw = _bw
    fig = plt.figure()
    ax = fig.add_subplot(111)
    data, = ax.plot([],[],lw=2)
    ax.set_title('Xilinx FFT')
    ax.set_ylim(30,180)
    ax.set_xlim([0, bw])
    freq = np.linspace(0, bw, 128, endpoint=True)
    ani = animation.FuncAnimation(fig, animate, blit=True)
    plt.show()


def animate(i):
    powB = struct.unpack('>1024Q',fpga.read('fft_spect',2**10*8))
    powB = 10*np.log10(np.array(powB)+1)
    data.set_data(freq, powB[0:128])
    return data,


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import ipdb
from math import trunc

def plot_vv(_fpga, _bram_name):
    global data, fpga, bram_name
    bram_name = _bram_name
    fpga = _fpga
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    data1, = ax1.plot([],[], lw=2)
    data2, = ax2.plot([],[], lw=2)
        
    data = [data1, data2]
    ax1.set_title('Relative phase')
    ax1.set_xlabel('cycles')
    ax1.set_ylabel('$\phi$[rad]')
    ax2.set_title('Relative magnitude')
    ax2.set_xlabel('cycles')
    ax2.set_ylabel('[dB]')

    ax1.set_xlim(0,1024)
    ax1.set_ylim(-180,180)
    ax2.set_xlim(0,1024)
    ax2.set_ylim(-50,50)
    
    ax1.grid()
    ax2.grid()
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()        


def init():
    data[0].set_data([],[])
    data[1].set_data([],[])
    return data

def get_data():
    corr = np.array(struct.unpack('>2048q', fpga.read(bram_name[0], 2048*8)))
    a = np.array(struct.unpack('>1024Q', fpga.read(bram_name[1]
, 1024*8)))
    b = np.array(struct.unpack('>1024Q', fpga.read(bram_name[2], 1024*8)))

    pow_diff = 10*(np.log10(a+1)-np.log10(b+1))
    phase = np.rad2deg(np.arctan2(corr[1::2], corr[::2]))
    
    return [phase, pow_diff]
    


def animate(i):
    aux = get_data()
    data[0].set_data(np.arange(1024),aux[0])
    data[1].set_data(np.arange(1024), aux[1])
   # print(str(aux[1][6068])+'dB')
    return data

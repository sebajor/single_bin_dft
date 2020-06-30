import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import ipdb
from math import trunc
import time


def plot_spect(_fpga, _freq):
    global data, fpga, freq
    freq = _freq
    fpga = _fpga
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    data1, = ax1.plot([],[], lw=2)
    data2, = ax2.plot([],[], lw=2)
        
    data = [data1, data2]
    ax1.set_title('ADC0 spectrum')
    ax1.set_xlabel('cycles')
    ax1.set_ylabel('[dB]')
    ax2.set_title('ADC1 spectrum')
    ax2.set_xlabel('cycles')
    ax2.set_ylabel('[dB]')

    ax1.set_xlim(freq[0], freq[-1])
    ax1.set_ylim(80, 180)
    ax2.set_xlim(freq[0], freq[-1])
    ax2.set_ylim(80, 180)
    
    ax1.grid()
    ax2.grid()
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show() 


def init():
    data[0].set_data([],[])
    data[1].set_data([],[])
    return data

def get_data():
    a1 = struct.unpack('>Q', fpga.read('A1', 8))[0]
    a2 = struct.unpack('>Q', fpga.read('A2', 8))[0]
    a3 = struct.unpack('>Q', fpga.read('A3', 8))[0]
    a4 = struct.unpack('>Q', fpga.read('A4', 8))[0]
    a5 = struct.unpack('>Q', fpga.read('A5', 8))[0]
    A =10*np.log10(np.array([a1,a2,a3,a4,a5])+1)
    b1 = struct.unpack('>Q', fpga.read('B1', 8))[0]
    b2 = struct.unpack('>Q', fpga.read('B2', 8))[0]
    b3 = struct.unpack('>Q', fpga.read('B3', 8))[0]
    b4 = struct.unpack('>Q', fpga.read('B4', 8))[0]
    b5 = struct.unpack('>Q', fpga.read('B5', 8))[0]
    B = 10*np.log10(np.array([b1,b2,b3,b4,b5])+1)
    return [A, B]




def animate(i):
    fpga.write_int('rst_save',1)
    fpga.write_int('rst_save',0)
    fpga.write_int('sync',0)
    fpga.write_int('sync',1)
    time.sleep(0.2)
    aux = get_data()
    data[0].set_data(freq,aux[0])
    data[1].set_data(freq, aux[1])
   # print(str(aux[1][6068])+'dB')
    return data




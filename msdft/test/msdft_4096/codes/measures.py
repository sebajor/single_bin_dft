import numpy as np
import matplotlib.pyplot as plt
import struct
import time
from valon5009 import valon5009



def measures(fpga, bram_name):
    """att_vals : tuple for the s1 and s2
        bram_name: 3 value list [corr, powa, powb]
    """
    valon = valon5009()
    valon.sel_source(1)
    valon.set_att_db(21)
    valon.set_plev(3)
    valon.sel_source(2)
    valon.set_att_db(21)
    valon.set_plev(3) 
    att = np.linspace(21, 31.5, 22)
    att = np.round(att, 1)
    

    phase_val = np.zeros([40,1024])
    pow_diff_val = np.zeros([40, 1024])
    print('plev 3')
    for i in range(6):
        valon.set_att_db(att[i])
        [phase, pow_diff] = get_data(fpga,bram_name)
        phase_val[i,:] = phase
        pow_diff_val[i,:] = pow_diff

        
    valon.set_plev(2)
    print('plev 2')
    for i in range(6):
        valon.set_att_db(att[i])
        [phase, pow_diff] = get_data(fpga,bram_name)
        phase_val[i+6,:] = phase
        pow_diff_val[i+6,:] = pow_diff
    
    valon.set_plev(1)
    print('plev 1')
    for i in range(6):
        valon.set_att_db(att[i])
        [phase, pow_diff] = get_data(fpga,bram_name)
        phase_val[i+12,:] = phase
        pow_diff_val[i+12,:] = pow_diff


    valon.set_plev(0)
    print('plev 0')
    for i in range(len(att)):
        valon.set_att_db(att[i])
        [phase, pow_diff] = get_data(fpga,bram_name)
        phase_val[i+18,:] = phase
        pow_diff_val[i+18,:] = pow_diff

    return [phase_val, pow_diff_val]

        

def get_data(fpga, bram_name):
    corr = np.array(struct.unpack('>2048q', fpga.read(bram_name[0], 2048*8)))
    a = np.array(struct.unpack('>1024Q', fpga.read(bram_name[1]
, 1024*8)))
    b = np.array(struct.unpack('>1024Q', fpga.read(bram_name[2], 1024*8)))

    pow_diff = 10*(np.log10(a+1)-np.log10(b+1))
    phase = np.rad2deg(np.arctan2(corr[1::2], corr[::2]))
    
    return [phase, pow_diff]
    
    
def plot_data(data):
    phase_avg = np.mean(data[0], axis=1)
    phase_std = np.std(data[0], axis=1)
    pow_avg = np.mean(data[1], axis=1)
    pow_std = np.std(data[1], axis=1)
    
    test_pow = np.linspace(0, 19.5, 40)

    fig = plt.figure()
    ax1 = fig.add_subplot(221)  
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)
    
    ax1.set_ylabel('Avg power ratio[dB]')
    ax1.set_xlabel('Tested power ratio [dB]')
    ax1.grid()
    ax1.plot(test_pow,pow_avg, '*-')    

    ax2.set_ylabel('SD $\sigma$ power ratio[dB]')
    ax2.set_xlabel('Tested power ratio [dB]')
    ax2.grid()
    ax2.plot(test_pow, pow_std, '*-')

    ax3.set_ylabel('Avg angle diff ['+u'\xb0'+']')
    ax3.set_xlabel('Tested power ratio [dB]')
    ax3.grid()
    ax3.plot(test_pow, phase_avg, '*-')

    ax4.set_ylabel('SD $\sigma$ angle diff ['+u'\xb0'+']')
    ax4.set_xlabel('Tested power ratio [dB]')
    ax4.grid()
    ax4.plot(test_pow, phase_std, '*-')

    plt.show()


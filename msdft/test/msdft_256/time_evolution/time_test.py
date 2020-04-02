import numpy as np
import matplotlib.pyplot as plt
import corr
import struct
import calandigital as calan
import time


IP = '192.168.0.40'
bof = '../debbug.bof'
fpga = corr.katcp_wrapper.FpgaClient(IP)
time.sleep(1)
fpga.upload_program_bof(bof,3000)
time.sleep(1)

fpga.write_int('msdft_sel',0)
fpga.write_int('twidd_num',0)
fpga.write_int('acc_len', 2**10)
fpga.write_int('rst',1)
fpga.write_int('sync',0)
fpga.write_int('rst_save',1)
fpga.write_int('rst_fft',1)
fpga.write_int('start_fft',1)
fpga.write_int('rst_fft',0)

freq = np.linspace(0,67.5,128, endpoint=False)



def repetitive(n_iter, index):
    """Repeat several times one measurement reset the system
    """
    stats = np.zeros([n_iter, 4])
    for i in range(n_iter):
        fpga.write_int('rst',1)
        fpga.write_int('sync',0)
        fpga.write_int('rst_save',1)
        fpga.write_int('rst_save',0)
        fpga.write_int('msdft1_msdft_rst_bram',1)
        fpga.write_int('msdft1_msdft_rst_bram',1)
        fpga.write_int('rst',0)
        fpga.write_int('sync',1)
        time.sleep(1)
        vals = take_data()
        stats[i,:] = calc_stats(vals, index)
        print('Values iter %i' %i)
        print('mean pow: %.4f \t std pow: %.4f' %(stats[i,0], stats[i,1]))
        print('mean ang: %.4f \t std ang: %.4f' %(stats[i,2], stats[i,3]))
        print('\n')
    return stats 
        
    

def take_data():
    a1 = np.array(struct.unpack('>1024Q', fpga.read('A1', 1024*8)))
    a2 = np.array(struct.unpack('>1024Q', fpga.read('A2', 1024*8)))
    a3 = np.array(struct.unpack('>1024Q', fpga.read('A3', 1024*8)))
    a4 = np.array(struct.unpack('>1024Q', fpga.read('A4', 1024*8)))
    a5 = np.array(struct.unpack('>1024Q', fpga.read('A5', 1024*8)))

    powA = np.vstack([a1,a2,a3,a4,a5])

    b1 = np.array(struct.unpack('>1024Q', fpga.read('B1', 1024*8)))
    b2 = np.array(struct.unpack('>1024Q', fpga.read('B2', 1024*8)))
    b3 = np.array(struct.unpack('>1024Q', fpga.read('B3', 1024*8)))
    b4 = np.array(struct.unpack('>1024Q', fpga.read('B4', 1024*8)))
    b5 = np.array(struct.unpack('>1024Q', fpga.read('B5', 1024*8)))

    powB = np.vstack([b1,b2,b3,b4,b5])

    corr1 = np.array(struct.unpack('>2048q', fpga.read('corr1', 2048*8)))
    corr2 = np.array(struct.unpack('>2048q', fpga.read('corr2', 2048*8)))
    corr3 = np.array(struct.unpack('>2048q', fpga.read('corr3', 2048*8)))
    corr4 = np.array(struct.unpack('>2048q', fpga.read('corr4', 2048*8)))
    corr5 = np.array(struct.unpack('>2048q', fpga.read('corr5', 2048*8)))

    ang1 =  np.rad2deg(np.arctan2(corr1[1::2], corr1[::2]))
    ang2 =  np.rad2deg(np.arctan2(corr2[1::2], corr2[::2]))
    ang3 =  np.rad2deg(np.arctan2(corr3[1::2], corr3[::2]))
    ang4 =  np.rad2deg(np.arctan2(corr4[1::2], corr4[::2]))
    ang5 =  np.rad2deg(np.arctan2(corr5[1::2], corr5[::2]))

    angs = np.vstack([ang1, ang2, ang3, ang4, ang5])

    return (powA, powB, angs)


def calc_stats(data, index):
    powA = data[0][index,:]
    powB = data[1][index,:]
    angs = data[2][index,:]
    mean_pow = np.mean(10*(np.log10(powA)-np.log10(powB)))
    std_pow = np.std(10*(np.log10(powA)-np.log10(powB)))
    mean_ang = np.mean(angs)
    std_ang = np.std(angs)
    return np.array([mean_pow, std_pow, mean_ang, std_ang])
    


def continuos(n_iter, index):
    fpga.write_int('rst',1)
    fpga.write_int('sync',0)
    fpga.write_int('rst_save',1)
    fpga.write_int('rst_save',0)
    fpga.write_int('rst',0)
    fpga.write_int('sync',1)
    stats = np.zeros([n_iter, 4])
    for i in range(n_iter):
        fpga.write_int('rst_save',1)
        fpga.write_int('rst_save',0)
        time.sleep(5)
        vals = take_data()
        stats[i,:] = calc_stats(vals, index)
        print('Values iter %i' %i)
        print('mean pow: %.4f \t std pow: %.4f' %(stats[i,0], stats[i,1]))
        print('mean ang: %.4f \t std ang: %.4f' %(stats[i,2], stats[i,3]))
        print('\n')
    return stats

    
def spect_evolution(n_iter):
    fpga.write_int('rst',1)
    fpga.write_int('sync',0)
    fpga.write_int('rst_save',1)
    fpga.write_int('rst_save',0)
    fpga.write_int('rst',0)
    fpga.write_int('sync',1)
    powA = np.zeros([n_iter, 5])
    powB = np.zeros([n_iter, 5])
    for i in range(n_iter):
        fpga.write_int('rst_save',1)
        fpga.write_int('rst_save',0)
        time.sleep(1)
        vals = take_data()
        powA[i,:] = vals[0][:,200]
        powB[i,:] = vals[1][:,200]
    return (powA, powB)
                





    

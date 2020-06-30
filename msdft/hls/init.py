import numpy as np
import corr, time
import struct
import matplotlib.pyplot as plt
import calandigital as calan
import os

def write_twidd(fpga, k, bram_name='twidd'):
    N=2**14
    t = np.arange(N)
    twidd = np.exp(-1j*2*np.pi*k/N*t)
    twidd_re = twidd.real
    twidd_im = twidd.imag
    re_data = calan.float2fixed(twidd_re, nbits=16, binpt=14)
    im_data = calan.float2fixed(twidd_im, nbits=16, binpt=14)
    twidd_data = np.zeros(2*len(re_data), dtype='int')
    twidd_data[1::2] = re_data
    twidd_data[::2] = im_data
    twid_data = twidd_data.tolist()
    raw_data = struct.pack('>32768h', *twidd_data)
    fpga.write(bram_name, raw_data) 
    return 1 



IP = '192.168.0.40'
fpga = corr.katcp_wrapper.FpgaClient(IP)
time.sleep(3)
fpga.upload_program_bof('hls_efficient.bof.gz', 3000)
time.sleep(3)

k = 5596

write_twidd(fpga,k=k)
time.sleep(1)

#autoreset the machine with a given period
rst_period = 2**15
fpga.write_int('thresh', rst_period)
fpga.write_int('en_rst_cycle',1)

#set accumulation len
acc_len = 2**0
fpga.write_int('acc_len', acc_len)

#reset everything
fpga.write_int('ap_rst',1)
fpga.write_int('rst_app',1)
fpga.write_int('rst_cnt',1)
fpga.write_int('ap_rst',0)
fpga.write_int('ap_start',1)
fpga.write_int('rst_cnt',0)

fpga.write_int('rst_app',0)

def check_twidd(fpga):
    N = 2**14
    k = 5596
    t = np.arange(N)
    re_data = struct.unpack('>16384h', fpga.read('twidd_re', 2**14*2))
    im_data = struct.unpack('>16384h', fpga.read('twidd_im', 2**14*2))
    gold = np.exp(-1j*2*np.pi*k/N*t)
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.set_title('real')
    ax2.set_title('imag')
    ax1.grid()
    ax2.grid()
    ax1.plot(np.array(re_data)/2.**14, label='roach')
    ax1.plot(gold.real, label='gold')
    ax2.plot(np.array(im_data)/2.**14)
    ax2.plot(gold.imag)
    plt.show()


def read_data(fpga):
    powA = struct.unpack('>1024Q', fpga.read('powA', 1024*8))
    powB = struct.unpack('>1024Q', fpga.read('powB', 1024*8))
    phase = struct.unpack('>2048q', fpga.read('phase', 1024*2*8))
    re = phase[::2]
    im = phase[1::2]
    ang = np.rad2deg(np.arctan2(im,re))
    pow_diff = 10*(np.log10(np.array(powA)+1)-np.log10(np.array(powB)+1))
    return [pow_diff, ang]



def plot_data(fpga):
    [pow_diff, ang] = read_data(fpga)
    fig = plt.figure()
    
    print('avg_pow: '+str(np.mean(pow_diff)))
    print('std_pow: '+str(np.std(pow_diff)))
    print('avg_ang: '+str(np.mean(ang)))
    print('std_ang: '+str(np.std(ang)))
        
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.grid()
    ax2.grid()
    ax1.set_title('Power diff')
    ax1.plot(pow_diff)
    ax2.set_title('Phase diff')
    ax2.plot(ang)
    plt.show()



def meas(fpga):
    att_list = []
    glob_pow_avg = []
    glob_pow_std = []
    glob_ang_avg = []
    glob_ang_std = []

    while(1):
        cont = raw_input('continue?')
        if(cont=='n'):
            break
        att = input('att_lev')
        att_list.append(att)
        os.mkdir(str(att)) 
        os.chdir(str(att))
        pow_burst = []
        ang_burst = []
        pow_avg_burst = np.zeros(30)
        pow_std_burst = np.zeros(30)
        ang_avg_burst = np.zeros(30)
        ang_std_burst = np.zeros(30)
        for i in range(30):
            fpga.write_int('rst_cnt',1)
            fpga.write_int('rst_cnt',0)
            vals = read_data(fpga)
            pow_burst.append(vals[0])
            ang_burst.append(vals[1])
            pow_avg_burst[i] = np.mean(vals[0])
            pow_std_burst[i] = np.std(vals[0])
            ang_avg_burst[i] = np.mean(vals[1])
            ang_std_burst[i] = np.std(vals[1])
            time.sleep(0.5) 
        np.savetxt('pow_burst',np.array(pow_burst))
        np.savetxt('ang_burst',np.array(ang_burst))
        np.savetxt('pow_avg',pow_avg_burst)
        np.savetxt('pow_std',pow_std_burst)
        np.savetxt('ang_avg',ang_avg_burst)
        np.savetxt('ang_std',ang_std_burst)
        os.chdir('..')
        print('pow_lev: '+str(np.mean(pow_avg_burst)))
        print('phase: '+str(np.mean(ang_avg_burst)))
        print('phase error: '+str(np.std(ang_avg_burst)))
        glob_pow_avg.append(np.mean(pow_avg_burst))
        glob_pow_std.append(np.std(pow_avg_burst))
        glob_ang_avg.append(np.mean(ang_avg_burst))
        glob_ang_std.append(np.std(ang_avg_burst))
        
    np.savetxt('pow_avg',np.array(glob_pow_avg))
    np.savetxt('pow_std',np.array(glob_pow_std))
    np.savetxt('ang_avg',np.array(glob_ang_avg))
    np.savetxt('ang_std',np.array(glob_ang_std))
    np.savetxt('att_lev',np.array(att_list))
    #generate plots
    fig = plt.figure()
    ax1 = fig.add_subplot(221)
    ax1.set_ylabel('avg pow diff dB')
    ax1.set_xlabel('dB')
    ax1.grid()
    ax1.plot(att_list, glob_pow_avg, '-*')    

    ax2 = fig.add_subplot(222)
    ax2.set_ylabel('std pow diff dB')
    ax2.set_xlabel('db')
    ax2.grid()
    ax2.plot(att_list, glob_pow_std, '-*')    

    ax3 = fig.add_subplot(223)
    ax3.set_ylabel('avg phase diff')
    ax3.set_xlabel('dB')
    ax3.grid()
    ax3.plot(att_list, glob_ang_avg, '-*')
    
    ax4 = fig.add_subplot(224)
    ax4.set_ylabel('std phase diff')
    ax4.set_xlabel('dB')
    ax4.grid()
    ax4.plot(att_list, glob_ang_avg, '-*')
    plt.show()

    











        
















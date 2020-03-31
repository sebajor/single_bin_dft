import numpy as np
import matplotlib.pyplot as plt
import corr
from fft_funct import plot_fft
import struct
import calandigital as calan
import time

IP = '192.168.0.40'
bof = 'debbug.bof'
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

plot_fft(fpga, 67.5)
fpga.write_int('rst_save',0)
fpga.write_int('msdft1_msdft_rst_bram',1)
fpga.write_int('msdft1_msdft_rst_bram',1)
fpga.write_int('rst',0)
fpga.write_int('sync',1)


fft_data = np.array(struct.unpack('>1024Q', fpga.read('fft_spect', 1024*8)))

time.sleep(5)

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


fig = plt.figure()
ax1 = fig.add_subplot(121)
ax1.plot(10*(np.log10(powA[1,:])-np.log10(powB[1,:])))
ax1.grid()
ax1.set_title('Power difference')
ax1.set_ylabel('dB')
ax1.set_xlabel('cycles')
ax2 = fig.add_subplot(122)
ax2.plot(angs[1,:])
ax2.grid()
ax2.set_ylabel('deg')
ax2.set_xlabel('cycles')
ax2.set_title('Relative phase')

fig1 = plt.figure()
ax3 = fig1.add_subplot(111)
ax3.plot(freq[78:83],10*np.log10(powA[:,100]), label='ZDOK0')
ax3.plot(freq[78:83],10*np.log10(powB[:,100]), label='ZDOK1')
ax3.set_ylabel('dB')
ax3.legend()
ax3.set_title('Spectrum')
ax3.grid()

plt.show()


print('Relative phase mean: '+str(np.mean(angs[1,:])))
print('Relative phase std: '+str(np.std(angs[1,:])))
print('Mean Pow: '+str(np.mean(10*(np.log10(powA[1,:])-np.log10(powB[1,:])))))
print('std Pow: '+str(np.std(10*(np.log10(powA[1,:])-np.log10(powB[1,:])))))


















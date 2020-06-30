import numpy as np
import matplotlib.pyplot as plt
import corr
import struct
import calandigital as calan
import time
from plot_old import plot_vv
from plot_spect import plot_spect


IP = '192.168.0.40'
bof = 'msdft_12_v2.bof.gz' #tiene comb 2.. la otra tiene la version anterior
fpga = corr.katcp_wrapper.FpgaClient(IP)
time.sleep(1)
fpga.upload_program_bof(bof,3000)
time.sleep(1)


fpga.write_int('rst_cycles', 1200)
fpga.write_int('msdft_sel',0)
fpga.write_int('twidd_num',0)
#fpga.write_int('acc_len', 2**10)
fpga.write_int('rst',1)
fpga.write_int('sync',0)
fpga.write_int('rst_save',1)
#fpga.write_int('rst_fft',1)
#fpga.write_int('start_fft',1)
#fpga.write_int('rst_fft',0)

fpga.write_int('rst_save',0)
fpga.write_int('msdft1_msdft_rst_bram',1)
fpga.write_int('msdft1_msdft_rst_bram',1)
fpga.write_int('rst',0)
fpga.write_int('sync',1)
freq = np.linspace(0,67.5,2**11, endpoint=False)


a_brams = ['A1','A2','A3','A4','A5']
b_brams = ['B1','B2','B3','B4','B5']
corr_bram = ['corr1', 'corr2', 'corr3', 'corr4', 'corr5']

msdft_frec = freq[1397:1402]






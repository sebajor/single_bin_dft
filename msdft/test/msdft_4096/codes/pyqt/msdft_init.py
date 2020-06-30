import numpy as np
import corr
import struct
import time
from msdft_plots import *


class Msdft():

    def __init__(self, ip, bof, bw):
        """Connect to the roach and upload the bof file
        """
        self.bw = bw
        self.fpga = corr.katcp_wrapper.FpgaClient(ip)
        time.sleep(1)
        self.fpga.upload_program_bof(bof,3000)
        time.sleep(1)
        self.a_brams = ['A1', 'A2', 'A3', 'A4', 'A5']
        self.b_brams = ['B1', 'B2', 'B3', 'B4', 'B5']
        self.corr_brams = ['corr1', 'corr2', 'corr3', 'corr4', 'corr5']
        self.freq = np.linspace(0, bw, 2**12, endpoint=False)
        self.msdft_freq = [self.freq[1397], self.freq[1398], self.freq[1399], self.freq[1400], self.freq[1401]] #default frequencies
    
    def init_sys(self, rst_cycles=2048):
        """Initialize the system and set the
           reset period of the msdft.
        """
        fpga.write_int('rst_cycles', rst_cycles)
        fpga.write_int('msdft_sel',0)
        fpga.write_int('twidd_num',0)
        fpga.write_int('rst',1)
        fpga.write_int('sync',0)
        fpga.write_int('rst_save',1)
        fpga.write_int('rst_save',0)
        fpga.write_int('msdft1_msdft_rst_bram',1)
        fpga.write_int('msdft1_msdft_rst_bram',1)
        fpga.write_int('rst',0)
        fpga.write_int('sync',1)


    def set_freq(index, new_freq):
        #TODO
        df = self.bw/2048. 
        new_freq = np.rint(new_freq/index)
        
    def plots(self,  plots=[1,1,0,0], pow_brams=['A1', 'B2'], phase_brams=['corr1'], bw=67.5, bins=[1397, 1398, 1399, 1400, 1401]):
        app = QtGui.QApplication([])
        plot_data = Main_thread(self.fpga, plots=[1,1,0,0], pow_brams=['A1', 'B2'], phase_brams=['corr1'], bw=67.5, bins=[1397, 1398, 1399, 1400, 1401])
        app.exec_()














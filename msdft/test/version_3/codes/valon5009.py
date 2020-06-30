#!/usr/bin/env python

import serial 
import time

class valon5009(object):
    """Class to interface with valon5009
    """
    def __init__(self, port='/dev/ttyUSB0', baud=115200):
        self.com = serial.Serial(port=port, baudrate=baud)
        time.sleep(0.5)
        
    def sel_source(self, source):
        msg = 's'+str(source)+'\r\n'
        self.com.write(msg)
        time.sleep(0.5)
        resp_size = self.com.inWaiting()
        resp = self.com.read(resp_size)
        print(resp)


    def set_freq_mhz(self, f):
        """available frequencies [25,6000] MHz
           with a .0001 step resolution
        """
        msg = 'f '+str(f)+'\r\n'
        self.com.write(msg)
        time.sleep(0.5)
        resp_size = self.com.inWaiting()
        resp = self.com.read(resp_size)
        print(resp)
    
    def set_att_db(self, att):
        """Attenuation could takes values in 
           the range  [0, 31.5] dB with a 5dB
           step.
           Carefull, the output power depends of the
           attenuation value and the power level of 
           valon  
        """
        msg = 'att '+str(att)+'\r\n'
        self.com.write(msg)
        time.sleep(0.5)
        resp_size = self.com.inWaiting()
        resp = self.com.read(resp_size)
        print(resp)
    
    def set_plev(self, plev):
        """set the power level of the valon.
            plev could be [0,1,2,3].
            the approx power values of each
            level (without attenuation) are:
                0 ----> 17dBm
                1 ----> 14dBm
                2 ----> 11dBm
                3 ----> 9 dBm
        """
        
        if(plev in [0,1,2,3]):
            msg = 'plev '+str(plev)+'\r\n'
            self.com.write(msg)
            time.sleep(0.5)
            resp_size = self.com.inWaiting()
            resp = self.com.read(resp_size)
            print(resp)
        else:
            print('Power level could only take values in [0,1,2,3]')


    def get_frequency(self):
        self.com.write('f\r\n')
        time.sleep(0.5)
        resp_size = self.com.inWaiting()
        resp = self.com.read(resp_size)
        self.freq = resp[3:7]


    def get_approx_output_level(self):
        self.com.write('plev\r\n')
        time.sleep(0.5)
        resp_size = self.com.inWaiting()
        resp = self.com.read(resp_size)
        self.plev = resp[3:7]
        self.com.write('att\r\n')
        time.sleep(0.5)
        resp_size = self.com.inWaiting()
        resp = self.com.read(resp_size)
        self.att = resp[3:7]
        
        self.power = 9+3*plev-att
        print('Output power:'+str(self.power)+'dBm')

        
    









    




    

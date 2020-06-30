from pyqtgraph import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import sys
import ipdb

class Workersignal(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(tuple)
    result = QtCore.pyqtSignal(tuple)
    #prorgress = QtCore.pyqtSignal(tuple)


class Worker(QtCore.QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = Workersignal()
        #self.kwargs['progress_callback'] = [0,0]

    @QtCore.pyqtSlot()   
    def run(self):
        try:
            #print('trying...')
            result = self.fn(*self.args, **self.kwargs)
        except:
            print('exception..')
            #traceback.print_exc()
            #exctype, value = sys.exc_info()[:2]
            #self.signal.error.emit((0, value, traceback.format_exc()))
            self.signals.error.emit(('asdqew', 'error'))
        else:
            #print('else...')
            self.signals.result.emit(result)



class Main_thread(QtGui.QMainWindow):
    
    def __init__(self,fpga, plots=[1,1,0,0], pow_brams=['A1', 'B2'], phase_brams=['corr1'], bw=67.5, bins=[1397, 1398, 1399, 1400, 1401]):
        """Plots: [relative_pow, relative_phase, spect1, spect2]
                  put a 1 in teh plot that you want to add
        """
        super(Main_thread, self).__init__()
        self.fpga = fpga
        self.plots = plots
        self.pow_brams = pow_brams
        self.phase_brams = phase_brams
        self.win = pg.GraphicsWindow()
        self.curves = []

        ##maybe modify this
        self.freq = np.linspace(0,bw,2**11,endpoint=False)
        self.bins = bins
        ###

        self.threadpool = QtCore.QThreadPool()
        if(plots[0]):
            fig = self.win.addPlot(title='Power difference')
            fig.setRange(yRange=[-40,40], xRange=[0,1024])
            fig.showGrid(x=True, y=True)
            curve = fig.plot(pen='y')
            curve.setData(np.arange(1024), np.zeros(1024))
            self.curves.append(curve)
        else:
            self.curves.append(0)        


        if(plots[1]):
            fig = self.win.addPlot(title='Phase difference')
            fig.setRange(yRange=[-180, 180], xRange=[0,1024])
            fig.showGrid(x=True, y=True)
            curve = fig.plot(pen='y')     
            curve.setData(np.arange(1024), np.zeros(1024))
            self.curves.append(curve)
        else:
            self.curves.append(0)


        if(plots[2]):
            fig = self.win.addPlot(title='ADC0 spectrum')
            fig.setRange(yRange=[80, 140], xRange=[-1,5])
            fig.showGrid(x=True, y=True)
            curve = fig.plot(pen='y')     
            curve.setData(np.arange(5), np.zeros(5))
            self.curves.append(curve)
        else:
            self.curves.append(0)


        if(plots[3]):
            fig = self.win.addPlot(title='ADC1 spectrum')
            fig.setRange(yRange=[80, 140], xRange=[-1,5])
            fig.showGrid(x=True, y=True)
            curve = fig.plot(pen='y')     
            curve.setData(np.arange(5), np.zeros(5))
            self.curves.append(curve)


        self.Update()



    def Update(self):
        QtGui.QApplication.processEvents()
        workers = []
        if(self.plots[0]):
            worker1 = Worker(self, self.plot_pow, self.fpga)
            worker1.signals.result.connect(self.plot1)
            workers.append(worker1)
        if(self.plots[1]):
            worker2 = Worker(self, self.plot_phase, self.fpga)
            worker2.signals.result.connect(self.plot2)
            workers.append(worker2)
        if(self.plots[2]):
            worker3 = Worker(self, self.plot_spect,self.fpga,0)
            worker3.signals.result.connect(self.plot3)
            workers.append(worker3)
        if(self.plots[2]):
            worker4 = Worker(self, self.plot_spect,self.fpga,1)
            worker4.signals.result.connect(self.plot4)
            workers.append(worker4)
        for i in range(len(workers)):
             self.threadpool.start(workers[i])
        QtCore.QTimer.singleShot(1, self.Update)




    def plot_pow(self, fpga):
        print('powaa')
        a = np.array(struct.unpack('>1024Q', fpga.read(self.pow_brams[0], 1024*8)))
        b = np.array(struct.unpack('>1024Q', fpga.read(self.pow_brams[1], 1024*8)))
        pow_diff = 10*(np.log10(a+1)-np.log(b+1))
        return (np.arange(1024), pow_diff)
    
    
    def plot_phase(self, fpga):
        corr = np.array(struct.unpack('>2048q', fpga.read(self.phase_brams, 2048*8)))
        phase = np.rad2deg(np.arctan2(corr[1::2], corr[::2]))
        return (np.arange(1024), phase)


    def plot_spect(self,fpga, adc_n):
        if(adc_n):
            a1 = struct.unpack('>Q', fpga.read('A1',8))[0]
            a2 = struct.unpack('>Q', fpga.read('A2',8))[0]
            a3 = struct.unpack('>Q', fpga.read('A3',8))[0]
            a4 = struct.unpack('>Q', fpga.read('A4',8))[0]
            a5 = struct.unpack('>Q', fpga.read('A5',8))[0]
            spect = np.array([a1,a2,a3,a4,a5])
        else:
            b1 = struct.unpack('>Q', fpga.read('B1',8))[0]
            b2 = struct.unpack('>Q', fpga.read('B2',8))[0]
            b3 = struct.unpack('>Q', fpga.read('B3',8))[0]
            b4 = struct.unpack('>Q', fpga.read('B4',8))[0]
            b5 = struct.unpack('>Q', fpga.read('B5',8))[0]
            spect = np.array([b1,b2,b3,b4,b5])
        return (spect,1)


    def plot1(self, *args):
        self.curves[0].set_data(args[0][0], args[0][1])
    
    def plot2(self, *args):
        self.curves[1].set_data(args[0][0], args[0][1])
    
    def plot3(self, *args):
        self.curves[2].set_data(self.freqs[self.bins], args[0][0])

    def plot4(self, *args):
        self.curves[3].set_data(self.freqs[self.bins], args[0][0])




















        




























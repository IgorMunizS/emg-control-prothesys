import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore
import numpy as np
import emgClass
import data as dt
import caracteristicas as crt


#raw_data = np.zeros(5000)
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
def plotar_grafico(graficos, emgData, sampleRate):
    app = QtGui.QApplication([])
    win = pg.GraphicsWindow(title="Gráficos EMG")

    win.resize(1000, 600)

    for c in graficos:
        string = "Canal " + str(c)
        p = win.addPlot(title = string)
        p.showGrid(x=True, y=True)
        p.setLabels(left='Amplitude (mV)', bottom='Time(s)')
        time = len(emgData[c])/sampleRate
        cordx = np.linspace(0,time, len(emgData[c]))
        p.plot(cordx, emgData[c], size= 100, pen = 'r')
        p.setRange(yRange=[-4,4])
        win.nextRow()

    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app.instance().exec_()


def realTimePlot(graficos):
    app = QtGui.QApplication([])
    win = pg.GraphicsWindow(title="Real Time EMG")
    win.resize(1000, 600)

    #for c in graficos:
    p = win.addPlot(title = "Real time Canal" + str(c))
    curve= p.plot(pen = 'blue')
    p.setRange(yRange=[-5, 5])
    p.enableAutoRange('xy', False)


    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(100)
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()



sinal = dt.get_data('igormuniz',[0,1,0,0,0,0])
full_sinal = dt.windowing(sinal)




plotar_grafico([0,1,2,3,4,5,6],sinal,1000)




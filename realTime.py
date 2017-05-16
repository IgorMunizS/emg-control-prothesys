# -*- coding: utf-8 -*-
from ctypes import *
import time
import numpy as np
from collections import deque
import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore



handle = c_ulong()
currentSampleRate = c_double()
canais = 1
sampleRate = c_double(1000)
t = 0
emgData = []

sample = c_double()
nsample = c_ulong(int(0.1 * sampleRate.value))
emgbuffer = (c_double * nsample.value)()




isSampling = c_ulong()
cnt = 0

app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="Real Time EMG")
win.resize(1000, 600)


p = win.addPlot(title = "Real time Canal")

p.setRange(yRange=[-5, 5], xRange=[0,10000])
p.enableAutoRange('xy', False)

emgDataPlot = np.zeros(100, dtype=float)
curve = p.plot(pen = 'r')
lib = CDLL("C:\EMG System do Brasil\EMGLab\emgdlib.dll")  # Inicia biblioteca. Usar CDLL ao invés de WinDLL para fazer a chamada convencional em C. Evita confusões na passagem de parâmetros

# Referenciando as funções

emgOpenDriver = lib.emgOpenDriver
emgCloseDriver = lib.emgCloseDriver
emgGetEquipmentHandle = lib.emgGetEquipmentHandleByOrder
emgSetDesiredSampleRate = lib.emgSetDesiredSampleRate
emgRemoveAllChannels = lib.emgRemoveAllChannels
emgAddChannel = lib.emgAddChannel
emgSampleNSeconds = lib.emgSampleNSeconds
emgSampleNValues = lib.emgSampleNValues
emgReleaseEquipmentHandle = lib.emgReleaseEquipmentHandle
emgGetRawData = lib.emgGetRawData
emgGetRealUnitData = lib.emgGetRealUnitData
emgStopSample = lib.emgStopSample
emgGetCurrentSampleRate = lib.emgGetCurrentSampleRate
emgIsSampling = lib.emgIsSampling
emgGetRealUnitDataBlock = lib.emgGetRealUnitDataBlock
emgGetRawDataBlock = lib.emgGetRawDataBlock

emgOpenDriver.restype = c_ulong
emgCloseDriver.restype = c_ulong
emgGetEquipmentHandle.restype = c_ulong
emgSetDesiredSampleRate.restype = c_ulong
emgRemoveAllChannels.restype = c_ulong
emgAddChannel.restype = c_ulong
emgSampleNSeconds.restype = c_ulong
emgReleaseEquipmentHandle.restype = c_ulong
emgGetRawData.restype = c_ulong
emgGetRealUnitData.restype = c_ulong
emgStopSample.restype = c_ulong
emgGetCurrentSampleRate.restype = c_ulong
emgIsSampling.restype = c_ulong
emgGetRealUnitDataBlock.restype = c_ulong
emgGetRawDataBlock.restype = c_ulong




def conecta_equip():
    status = emgOpenDriver()  # Abre driver
    if status == 0:
        print("Driver aberto")

    else:
        print("Driver não pode ser aberto")

    status = emgGetEquipmentHandle(0, byref(handle))  # Pega o handle do equipamento
    if status == 0:
        print("Pegou Handle")
    else:
        print("Erro ao pegar Handle")

    status = emgGetCurrentSampleRate(handle.value, 0, byref(currentSampleRate))
    if status == 0:
        print("Pegou Taxa de amostragem atual")
        print(currentSampleRate.value)
    else:
        print("Erro ao pegar taxa de amostragem atual")


def configura_equip():
    status = emgRemoveAllChannels(handle.value)
    if status == 0:
        print("Canais removidos")
    else:
        print("Não foi possível remover canais")

    for c in range(canais):
        status = emgAddChannel(handle.value, c)
        if status == 0:
            print("Canal", c, "adicionado")
        else:
            print("Não foi possivel adicionar canal")

    for c in range(canais):
        status = emgSetDesiredSampleRate(handle.value, c, byref(sampleRate))
        if status == 0:
            print("Canal", c, " taxa de amostragem colocada em ", sampleRate.value)
        else:
            print("Não foi possivel adicionar canal")


def coleta():
    global cnt
    global t



    status = emgSampleNSeconds(handle.value, 30)

    if status == 0:
        print("Inicia a amostragem")
    else:
        print("Não foi possível iniciar a amostragem")
    emgIsSampling(handle.value, byref(isSampling))







def update():
    global emgDataPlot

    canal = c_ulong(0)
    emgGetRealUnitDataBlock(handle.value, canal.value, emgbuffer, byref(nsample))

    #for value in emgbuffer:
        #emgDataPlot.append(value)

    emgData = np.frombuffer(emgbuffer)
    print(emgData)iiuu
    emgDataPlot = np.concatenate([emgDataPlot, emgData])

    if len(emgDataPlot) > 10000:
        emgDataPlot = emgDataPlot[nsample.value:]

    curve.setData(emgDataPlot)
    emgIsSampling(handle.value, byref(isSampling))



def desliga_equip():
    status = emgReleaseEquipmentHandle(handle.value)

    if status == 0:
        print("Handle liberado")
    else:
        print("Handle não pode ser liberado")
    status = emgCloseDriver()

    if status == 0:
        print("Driver Fechado")
    else:
        print("Erro ao fechar driver")


conecta_equip()
configura_equip()


coleta()
time.sleep(0.01)
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(100)


if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

desliga_equip()

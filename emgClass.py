from ctypes import *
import threading
import numpy as np
import plotGrafico as grafico




class EmgEquipment(object):
    def __init__(self, sampleRate, sampleTime, canais, graficos):
        self.sampleRate = c_double(sampleRate)
        self.sampleTime = int(sampleTime)
        self.canais = canais
        self.graficos = graficos
        self.handle = c_ulong()
        self.isSampling = c_ulong()

        lib = CDLL("C:\EMG System do Brasil\EMGLab\emgdlib.dll")  # Inicia biblioteca. Usar CDLL ao invés de WinDLL para fazer a chamada convencional em C. Evita confusões na passagem de parâmetros
        self.emgOpenDriver = lib.emgOpenDriver
        self.emgCloseDriver = lib.emgCloseDriver
        self.emgGetEquipmentHandle = lib.emgGetEquipmentHandleByOrder
        self.emgSetDesiredSampleRate = lib.emgSetDesiredSampleRate
        self.emgRemoveAllChannels = lib.emgRemoveAllChannels
        self.emgAddChannel = lib.emgAddChannel
        self.emgSampleNSeconds = lib.emgSampleNSeconds
        self. emgSampleNValues = lib.emgSampleNValues
        self.emgReleaseEquipmentHandle = lib.emgReleaseEquipmentHandle
        self.emgGetRawData = lib.emgGetRawData
        self.emgGetRealUnitData = lib.emgGetRealUnitData
        self.emgStopSample = lib.emgStopSample
        self.emgGetCurrentSampleRate = lib.emgGetCurrentSampleRate
        self. emgIsSampling = lib.emgIsSampling
        self.emgGetRealUnitDataBlock = lib.emgGetRealUnitDataBlock
        self.emgGetRawDataBlock = lib.emgGetRawDataBlock

        self.emgOpenDriver.restype = c_ulong
        self.emgCloseDriver.restype = c_ulong
        self.emgGetEquipmentHandle.restype = c_ulong
        self.emgSetDesiredSampleRate.restype = c_ulong
        self.emgRemoveAllChannels.restype = c_ulong
        self.emgAddChannel.restype = c_ulong
        self.emgSampleNSeconds.restype = c_ulong
        self.emgReleaseEquipmentHandle.restype = c_ulong
        self.emgGetRawData.restype = c_ulong
        self.emgGetRealUnitData.restype = c_ulong
        self.emgStopSample.restype = c_ulong
        self.emgGetCurrentSampleRate.restype = c_ulong
        self.emgIsSampling.restype = c_ulong
        self.emgGetRealUnitDataBlock.restype = c_ulong
        self.emgGetRawDataBlock.restype = c_ulong


    def conecta_equip(self):
        status = self.emgOpenDriver()  # Abre driver
        if status == 0:
            print("Driver aberto")

        else:
            print("Driver não pode ser aberto")

        status = self.emgGetEquipmentHandle(0, byref(self.handle))  # Pega o handle do equipamento
        if status == 0:
            print("Pegou Handle")
        else:
            print("Erro ao pegar Handle")

        self.config_equip()
        return True

    def config_equip(self):
        status = self.emgRemoveAllChannels(self.handle.value)
        if status == 0:
            print("Canais removidos")
        else:
            print("Não foi possível remover canais")

        for c in self.canais:
            status = self.emgAddChannel(self.handle.value, c)
            if status == 0:
                print("Canal", c, "adicionado")
            else:
                print("Não foi possivel adicionar canal")

        for c in self.canais:
            status = self.emgSetDesiredSampleRate(self.handle.value, c, byref(self.sampleRate))
            if status == 0:
                print("Canal", c, " taxa de amostragem colocada em ", self.sampleRate.value)
            else:
                print("Não foi possivel adicionar canal")

    def coleta(self):


        self.emgData = np.array([0,1,2,3,4,5,6,7], dtype=object)
        for c in self.canais:
            self.emgData[c] = []


        self.nsample = c_ulong(int(0.1 * self.sampleRate.value))
        self.emgbuffer = (c_double * self.nsample.value)()


        status = self.emgSampleNSeconds(self.handle.value, self.sampleTime)
        if status == 0:
            print("Inicia a amostragem")

        else:
            print("Não foi possível iniciar a amostragem")

        self.emgIsSampling(self.handle.value, byref(self.isSampling))



    def loopColeta(self):
        if self.isSampling:
            for c in self.canais:
                self.emgGetRealUnitDataBlock(self.handle.value, c, self.emgbuffer, byref(self.nsample))
                emgCapture = np.frombuffer(self.emgbuffer)

                self.emgData[c] = np.concatenate([self.emgData[c], emgCapture])
                #for value in self.emgbuffer:
                    #self.emgData[c].append(value)



            self.emgIsSampling(self.handle.value, byref(self.isSampling))



    def coletaRT(self):
        self.emgDataRT = np.array([0, 1, 2, 3, 4, 5, 6, 7], dtype=object)
        for c in self.canais:
            self.emgDataRT[c] = []



        self.nsample = c_ulong(int(0.1 * self.sampleRate.value))
        self.emgbuffer = (c_double * self.nsample.value)()

        status = self.emgSampleNSeconds(self.handle.value, self.sampleTime)
        if status == 0:
            print("Inicia a amostragem")

        else:
            print("Não foi possível iniciar a amostragem")

        self.emgIsSampling(self.handle.value, byref(self.isSampling))

    def loopColetaRT(self):
        if self.isSampling:
            i=0
            for c in self.canais:
                self.emgDataRT[i] = []
                self.emgGetRealUnitDataBlock(self.handle.value, c, self.emgbuffer, byref(self.nsample))
                emgCapture = np.frombuffer(self.emgbuffer)
                # for value in self.emgbuffer:
                #     self.emgDataRT[i].append(value)
                self.emgDataRT[i] = np.concatenate([self.emgDataRT[i], emgCapture])

                i += 1

            self.emgIsSampling(self.handle.value, byref(self.isSampling))
            # print(self.emgDataRT)

    def pararColeta(self):

        self.emgStopSample(self.handle.value)

        if len(self.graficos) > 0:
            t = threading.Thread(target=grafico.plotar_grafico, args=(self.graficos, self.emgData, self.sampleRate.value, ))
            t.start()
           # grafico.plotar_grafico(self.graficos, self.emgData, self.sampleRate.value)

    def pararColetaRT(self):

        self.emgStopSample(self.handle.value)


    def desliga_equip(self):
        status = self.emgReleaseEquipmentHandle(self.handle.value)

        if status == 0:
            print("Handle liberado")
        else:
            print("Handle não pode ser liberado")
        status = self.emgCloseDriver()

        if status == 0:
            print("Driver Fechado")
        else:
            print("Erro ao fechar driver")

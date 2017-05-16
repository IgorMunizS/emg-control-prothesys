import numpy as np
from pybrain.datasets import ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer, TanhLayer, SigmoidLayer, LSTMLayer, LinearLayer
from pybrain.tools.customxml import NetworkWriter
from pybrain.tools.customxml import NetworkReader
import classifica_sinal as cs
import matplotlib.pyplot as plt


def loadfnn(file, n_mov):

    fnn = NetworkReader.readFrom(file)
    print('aqui')
    data, tam = cs.get_data_infile('luanrt_caract.txt')
    alldata = ClassificationDataSet(7 * 4, 1, nb_classes=n_mov)
    mov = 1
    i = -1

    print(len(data))

    for n in range(len(data)):
        i += 1
        if i <= 13:
            alldata.addSample(data[n], [0])
        if i >= 14 and i <= 133:
            alldata.addSample(data[n], [mov])
        if i >= 134 and i <= 173:
            alldata.addSample(data[n], [0])
        if i >= 174 and i <= 293:
            alldata.addSample(data[n], [mov])
        if i >= 294 and i <= 333:
            alldata.addSample(data[n], [0])
        if i >= 334 and i <= 453:
            alldata.addSample(data[n], [mov])
        if i >= 454 and i <= 493:
            alldata.addSample(data[n], [0])
        if i >= 494 and i <= 613:
            alldata.addSample(data[n], [mov])
        if i >= 614 and i <= 653:
            alldata.addSample(data[n], [0])
        if i >= 654 and i <= 773:
            alldata.addSample(data[n], [mov])
        if i == 773:
            i = -1
            mov += 1


    error_tstdata =[]
    error_valida = []
    for j in range(10):
        tstdata_temp, trndata_temp = alldata.splitWithProportion(0.5)

        tstdata = ClassificationDataSet(7 * 4, 1, nb_classes=n_mov)
        for n in range(0, tstdata_temp.getLength()):
            tstdata.addSample(tstdata_temp.getSample(n)[0], tstdata_temp.getSample(n)[1])

        trndata = ClassificationDataSet(7 * 4, 1, nb_classes=n_mov)
        for n in range(0, trndata_temp.getLength()):
            trndata.addSample(trndata_temp.getSample(n)[0], trndata_temp.getSample(n)[1])

        trndata._convertToOneOfMany()
        tstdata._convertToOneOfMany()



        ris = fnn.activateOnDataset(tstdata)
        out = ris.argmax(axis=1)

        percenterrortest = percentError(out, tstdata['class'])

#         ris = fnn.activate([0.0085100085100059605, 0.47863247863209, 0.010044675295438284, 0.0, 0.0085100085100059605, 0.47863247863209, 0.010044675295438284, 0.0, 0.0085100085100059605, 0.47863247863209, 0.010044675295438284, 0.0, 0.0085100085100059605, 0.47863247863209, 0.010044675295438284, 0.0, 0.0085100085100059605, 0.47863247863209, 0.010044675295438284, 0.0, 0.0085100085100059605, 0.47863247863209, 0.010044675295438284, 0.0, 0.0085100085100059605, 0.47863247863209, 0.010044675295438284, 0.0]
#
#
#
# )
#         ris2 = fnn.activate([0.0081646748313420215, 0.15628815628796, 0.0087360840562707258, 0.0, 0.0081646748313420215, 0.15628815628796, 0.0087360840562707258, 0.0, 0.0081646748313420215, 0.15628815628796, 0.0087360840562707258, 0.0, 0.0081646748313420215, 0.15628815628796, 0.0087360840562707258, 0.0, 0.0081646748313420215, 0.15628815628796, 0.0087360840562707258, 0.0, 0.0081646748313420215, 0.15628815628796, 0.0087360840562707258, 0.0, 0.0081646748313420215, 0.15628815628796, 0.0087360840562707258, 0.0]
#
#
#
# )
#
#         out =  ris.argmax(axis=0)
#         out2 = ris2.argmax(axis=0)
#
#         print(out,out2)

        ris = fnn.activateOnDataset(trndata)
        out = ris.argmax(axis=1)
        percenterrortrn = percentError(out, trndata['class'])
        error_tstdata.append(percenterrortest)
        error_valida.append(percenterrortrn)

    print('Acerto validação medio', (100 - np.mean(error_valida)))
    print('Acerto teste medio', (100 - np.mean(error_tstdata)))

    ris = fnn.activateOnDataset(tstdata)
    out = ris.argmax(axis=1)
    print(out)
    percenterrortest = percentError(out, tstdata['class'])

    # plt.boxplot(error_tstdata)
    # plt.show()



loadfnn('luanrt123456_fnn7.xml', 7)
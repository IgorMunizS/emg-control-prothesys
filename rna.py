import numpy as np
from pybrain.datasets import ClassificationDataSet, SupervisedDataSet
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer, TanhLayer, SigmoidLayer, LSTMLayer, LinearLayer
from pybrain.tools.customxml import NetworkWriter
from pybrain.tools.customxml import NetworkReader



def get_data_infile(file, n_carac):
    arq = open(file, 'r')
    matriz = []
    linha = 0
    vetor_caract = []

    for value in arq:
        linha += 1
        vetor_caract.append(float(value))
        if linha == 7 * n_carac:
            matriz.append(vetor_caract)
            linha = 0
            vetor_caract = []

    # print(len(matriz))
    # print(matriz[0])
    # print(matriz[4642])
    return matriz


def rna_mlp(data, n_mov, n_caract):
    alldata = SupervisedDataSet(7 * n_caract,n_mov)
    mov = 1
    i = -1
    hiddenlayer = int(n_caract*n_mov*1.8)

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

    # tstdata_temp, trndata_temp = alldata.splitWithProportion(0.15)
    #
    # tstdata = ClassificationDataSet(7 * n_caract, 1, nb_classes=n_mov)
    # for n in range(0, tstdata_temp.getLength()):
    #     tstdata.addSample(tstdata_temp.getSample(n)[0], tstdata_temp.getSample(n)[1])
    #
    # trndata = ClassificationDataSet(7 * n_caract, 1, nb_classes=n_mov)
    # for n in range(0, trndata_temp.getLength()):
    #     trndata.addSample(trndata_temp.getSample(n)[0], trndata_temp.getSample(n)[1])
    #
    # trndata._convertToOneOfMany()
    # tstdata._convertToOneOfMany()
    # alldata._convertToOneOfMany()
    #
    # print("Number of training patterns: ", len(alldata))
    # print("Input, hidden and output dimensions: ", alldata.indim, hiddenlayer, alldata.outdim)
    # print("First sample (input, target, class):")
    # print(trndata['input'][0], trndata['target'][0], trndata['class'][0])

    # 7 Mov - 64 hidden layer
    # 5 MOV   48 hidden layer
    # 3 MOV - 36 2 hidden layer
    #1 MOV - 20 HIdden layer
    fnn = buildNetwork(alldata.indim, 64, alldata.outdim, outclass=SoftmaxLayer)
    # fnn = buildNetwork(trndata.indim, 20, 20,  trndata.outdim, hiddenclass= SigmoidLayer)
    trainer = BackpropTrainer(fnn, dataset=alldata, verbose=True, learningrate=0.01)
    bestTrainer = trainer
    tstresult_temp = 4
    # for i in range(1000):
    #     trainer.trainEpochs(1)
    #     trnresult = percentError(trainer.testOnClassData(dataset=trndata), trndata['class'])
    #     tstresult = percentError(trainer.testOnClassData(dataset=tstdata), tstdata['class'])
    #
    #     print("epoch: %4d" % trainer.totalepochs, "  train error: %2.2f%%" % trnresult,
    #           "  test error: %5.2f%%" % tstresult)
    #     if tstresult < tstresult_temp:
    #         bestTrainer = trainer
    #         tstdata_temp = tstresult
    #
    # trnresult = percentError(bestTrainer.testOnClassData(dataset=trndata), trndata['class'])
    # tstresult = percentError(bestTrainer.testOnClassData(dataset=tstdata), tstdata['class'])
    #
    # print("epoch: %4d" % trainer.totalepochs, "  train error: %2.2f%%" % trnresult,
    #       "  test error: %5.2f%%" % tstresult)

    trainer.trainUntilConvergence(dataset=alldata, validationProportion=0.25, maxEpochs= 1000, continueEpochs=10)


    ris = fnn.activateOnDataset(alldata)
    out = ris.argmax(axis=1)
    percenterrortest = percentError(out, alldata)
    print(percenterrortest)
    print(out)


    # trnresult = percentError(trainer.testOnClassData(), trndata['class'])
    # tstresult = percentError(trainer.testOnClassData(dataset=tstdata), tstdata['class'])
    # print("epoch: %4d" % trainer.totalepochs, "  train error: %2.2f%%" % trnresult,
    #       "  test error: %5.2f%%" % tstresult)
    #
    # NetworkWriter.writeToFile(fnn, 'Coletas\Luan\ fnn_luanmota_mov.xml')

data = get_data_infile('Coletas\Luan\caract_mov6.txt', 4)

rna_mlp(data, 7, 4)
print("Até convergir com ALLDATA e 1 HIDDEN LAYER 64 4 carct e 6 mov")
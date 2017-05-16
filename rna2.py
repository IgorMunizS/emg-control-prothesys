from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.tools.validation     import Validator
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from numpy.random import multivariate_normal
from scipy import diag, arange, meshgrid, where

means = [(-1,0),(2,4),(3,1)]
cov = [diag([1,1]), diag([0.5,1.2]), diag([1.5,0.7])]
alldata = ClassificationDataSet(2, 1, nb_classes=3)
for n in range(400):
    for klass in range(3):
        input = multivariate_normal(means[klass],cov[klass])
        alldata.addSample(input, [klass])

tstdata_temp, trndata_temp = alldata.splitWithProportion(0.25)

tstdata = ClassificationDataSet(2, 1, nb_classes=3)
for n in range(0, tstdata_temp.getLength()):
    tstdata.addSample( tstdata_temp.getSample(n)[0], tstdata_temp.getSample(n)[1])

trndata = ClassificationDataSet(2, 1, nb_classes=3)
for n in range(0, trndata_temp.getLength()):
    trndata.addSample(trndata_temp.getSample(n)[0], trndata_temp.getSample(n)[1])

trndata._convertToOneOfMany()
tstdata._convertToOneOfMany()

print("Number of training patterns: ", len(trndata))
print("Input and output dimensions: ", trndata.indim, trndata.outdim)
print("First sample (input, target, class):")
print(trndata['input'][0], trndata['target'][0], trndata['class'][0])

fnn = buildNetwork(trndata.indim, 5, trndata.outdim, outclass=SoftmaxLayer )
trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.3, verbose=True, weightdecay=0.01)
#
for i in range(20):
    trainer.trainEpochs(1)
    trnresult = percentError(trainer.testOnClassData(), trndata['class'])
    tstresult = percentError(trainer.testOnClassData(dataset=tstdata), tstdata['class'])

    print("epoch: %4d" % trainer.totalepochs, "  train error: %2.2f%%" % trnresult, "  test error: %5.2f%%" % tstresult)
# trnerror, valerror = trainer.trainUntilConvergence(dataset=trndata, validationProportion=0.125, maxEpochs=50)
# trnresult = percentError(trainer.testOnClassData(), trndata['class'])
# tstresult = percentError(trainer.testOnClassData(dataset=tstdata), tstdata['class'])
# print("epoch: %4d" % trainer.totalepochs, "  train error: %2.2f%%" % trnresult,
#       "  test error: %5.2f%%" % tstresult)

testdata = ClassificationDataSet(2, 1, nb_classes=3)
input2 = multivariate_normal(means[2], cov[2])
testdata.addSample(input2, [2])
testdata._convertToOneOfMany()

ris = fnn.activateOnDataset(testdata)
out=ris.argmax(axis=1)
percenterrortest=percentError(out, testdata['class'] )
print(percenterrortest)
print(out)

ris2 = fnn.activate(multivariate_normal(means[2], cov[2]))
print(ris2)
out=ris2.argmax(axis=0)
print(out)


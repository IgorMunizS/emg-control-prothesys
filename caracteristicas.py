import numpy as np


def rms(data):
    valor_rms = np.sqrt(np.mean(np.square(data)))
    return valor_rms


def mav(data):
    valor_mav = np.mean(np.abs(data))
    return valor_mav


def myop(data):
    m = 0
    for value in data:
        if value > 0.04:
            m += 1
    return m/len(data)


def zc(data):
    zc = 0
    for i in range(len(data) -1):
        if (data[i] >0 and data[i+1] < 0) or (data[i] < 0 and data[i+1]> 0) and (abs(data[i+1] - data[i]) >= 0.01):
            zc +=1
    return zc


def wl(data):
    wl = 0
    for i in range (len(data) -1):
        delta_wl = abs(data[i+1] - data[i])
        wl += delta_wl
    return wl

def ssc(data):
    ssc = 0
    for i in range(1, len(data)-1):
        if (data[i] > data[i -1] and data[i] > data[i+1]) or (data[i] < data[i-1] and data[i] < data[i+1]) and (abs(data[i] - data[i+1]) >= 0.1 or abs(data[i] - data[i-1]) >= 0.001):
            ssc += 1
    return ssc

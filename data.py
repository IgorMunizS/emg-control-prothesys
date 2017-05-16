import numpy as np
import caracteristicas as crt

#filepath2, filepath3, filepath4, filepath5

def get_data(filepath, vetor_mov):
    arquivo = []
    # stringMovs = ''

    if vetor_mov[0]:
        arquivo.append(open(filepath + '_Abdução do punho.txt', 'r'))
        # arquivo.append(open(filepath2 + '_Abdução do punho.txt', 'r'))
        # arquivo.append(open(filepath3 + '_Abdução do punho.txt', 'r'))
        # arquivo.append(open(filepath4 + '_Abdução do punho.txt', 'r'))
        # arquivo.append(open(filepath5 + '_Abdução do punho.txt', 'r'))
        # stringMovs = stringMovs + '1'
    if vetor_mov[1]:
        arquivo.append(open(filepath + '_Adução do punho.txt', 'r'))
        # arquivo.append(open(filepath2 + '_Adução do punho.txt', 'r'))
        # arquivo.append(open(filepath3 + '_Adução do punho.txt', 'r'))
        # arquivo.append(open(filepath4 + '_Adução do punho.txt', 'r'))
        # arquivo.append(open(filepath5 + '_Adução do punho.txt', 'r'))
        #stringMovs = stringMovs + '2'
    if vetor_mov[2]:
        arquivo.append(open(filepath + '_Contração da mão.txt', 'r'))
        # arquivo.append(open(filepath2 + '_Contração da mão.txt', 'r'))
        # arquivo.append(open(filepath3 + '_Contração da mão.txt', 'r'))
        # arquivo.append(open(filepath4 + '_Contração da mão.txt', 'r'))
        # arquivo.append(open(filepath5 + '_Contração da mão.txt', 'r'))
       # stringMovs = stringMovs + '3'
    if vetor_mov[3]:
        arquivo.append(open(filepath + '_Extensão do punho.txt', 'r'))
        # arquivo.append(open(filepath2 + '_Extensão do punho.txt', 'r'))
        # arquivo.append(open(filepath3 + '_Extensão do punho.txt', 'r'))
        # arquivo.append(open(filepath4 + '_Extensão do punho.txt', 'r'))
        # arquivo.append(open(filepath5 + '_Extensão do punho.txt', 'r'))
        #stringMovs = stringMovs + '4'
    if vetor_mov[4]:
        arquivo.append(open(filepath + '_Flexão do punho.txt', 'r'))
        # arquivo.append(open(filepath2 + '_Flexão do punho.txt', 'r'))
        # arquivo.append(open(filepath3 + '_Flexão do punho.txt', 'r'))
        # arquivo.append(open(filepath4 + '_Flexão do punho.txt', 'r'))
        # arquivo.append(open(filepath5 + '_Flexão do punho.txt', 'r'))
        #stringMovs = stringMovs + '5'
    if vetor_mov[5]:
        arquivo.append(open(filepath + '_Rotação do antebraço.txt', 'r'))
        # arquivo.append(open(filepath2 + '_Rotação do antebraço.txt', 'r'))
        # arquivo.append(open(filepath3 + '_Rotação do antebraço.txt', 'r'))
        # arquivo.append(open(filepath4 + '_Rotação do antebraço.txt', 'r'))
        # arquivo.append(open(filepath5 + '_Rotação do antebraço.txt', 'r'))
       # stringMovs = stringMovs + '6'


    vec = []
    print(len(arquivo))
    for x in range(7):
        vec.append([])

    i = 0

    for c in range(len(arquivo)):
        n = -1
        for line in arquivo[c]:
            if len(line) == 39:
                i = 0
                n += 1

            if len(line) != 39 and line != '\n': #and i < 38700:
                vec[n].append(float(line))
                i += 1

    print(len(vec[0]))
    return vec
def get_data_RT(filepath):
    arquivo = []
    arquivo.append(open(filepath, 'r'))


    vec = []
    # print(len(arquivo))
    for x in range(7):
        vec.append([])

    i = 0

    for c in range(len(arquivo)):
        n = -1
        for line in arquivo[c]:
            if len(line) == 39:
                i = 0
                n += 1

            if len(line) != 39 and line != '\n' and i < 38700:
                vec[n].append(float(line))
                i += 1

    # print(len(vec[0]))
    return vec

def windowing(data):
    fs = 1000
    janela_tamanho = 0.1*fs
    full_data = []
    for c in range(7):
        full_data.append([])
    for x in range(len(data)):

        if (len(data[x]) % janela_tamanho) != 0:
            for c in range(int(janela_tamanho) - len(data[x])%100):
                data[x].append(0.0)

        n = 50
        while n < len(data[x]):
            full_data[x].extend(data[x][n-int(janela_tamanho/2):n+int(janela_tamanho/2)])
            n += int(0.5*janela_tamanho)



    return full_data

def extrair_caract(data):
    n = 0
    matrix_rna = []



    while n < len(data[0]):
        vetor_caract = []
        for c in range(7):
            vetor_temp = data[c][n:n+99]

            valor_mav = crt.mav(vetor_temp)
            valor_wl = crt.wl(vetor_temp)
            valor_rms = crt.rms(vetor_temp)
            #
            valor_myop = crt.myop(vetor_temp)
            # valor_zc = crt.zc(vetor_temp)

            # valor_ssc = crt.ssc(vetor_temp)

            vetor_caract.append(valor_mav)
            vetor_caract.append(valor_wl)
            vetor_caract.append(valor_rms)
            vetor_caract.append(valor_myop)
            # vetor_caract.append(valor_zc)

            # vetor_caract.append(valor_ssc)

        n += 100
        matrix_rna.append(vetor_caract)

    # print(matrix_rna[0])
    # print(matrix_rna[20])
    # print(matrix_rna[4642])

    return matrix_rna


def salva_caract(matrix, path):
    arquivo = open(path +'_caract.txt', 'w')
    for c in range(len(matrix)):
        for value in matrix[c]:
            arquivo.write(str(value) + '\n')


def salva_caract_visual(matrix, path):
    arquivo = open(path +'_vis.txt', 'w')
    for value in matrix:
        arquivo.write(str(value) + '\n')


# dados_igor = get_data('Coletas\Shima\shima', [1,1,1,1,1,1])
#
# data = windowing(dados_igor)
# matrix = extrair_caract(data)
# salva_caract(matrix, stringMov)
# salva_caract_visual(matrix)
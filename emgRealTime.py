from pybrain.tools.customxml import NetworkReader
import data as dt
import udpConnection as udpC
import time

mov_anterior = 0
time_before = time.time()
contador = 0
mov_transition = 0
def loadRNA(path, vetor_mov):

    rna = NetworkReader.readFrom(path)
    vetor_msg = []
    for j in range(len(vetor_mov)):
        if vetor_mov[j]:
            vetor_msg.append(j+1)

    print(vetor_msg)
    return rna, vetor_msg

def emgrt(rna, matrix_dados, vetor_msg):

    caract =  dt.extrair_caract(matrix_dados)

    # arq = open('caract_rt', 'a')
    # arq.write(caract[0])
    # print(caract[0])
    ris = rna.activate(caract[0])

    out = ris.argmax(axis=0)
    print(out)
    virtualArmOn(out, vetor_msg)

def virtualArmOn(mov, vetor_msg):
    global mov_anterior
    global time_before
    global contador
    global mov_transition

    if mov == mov_anterior:
        contador += 1
    else:
        contador = 0



    if(time.time() - time_before) > 1:

        if mov == 0 and mov_transition != 0 and contador >= 3:

            if mov_transition == 1:
                udpC.msgRT('abp_r')
            if mov_transition == 2:
                udpC.msgRT('adp_r')

            if mov_transition == 3:
                udpC.msgRT('contm_r')

            if mov_transition == 4:
                udpC.msgRT('extp_r')

            if mov_transition == 5:
                udpC.msgRT('flxp_r')

            if mov_transition == 6:
                udpC.msgRT('rotab_r')

            mov_transition = mov
            time_before = time.time()




        if mov != 0 and mov_transition == 0 and contador >= 3:

            if vetor_msg[mov - 1] == 1:
                udpC.msgRT('abp')
            if vetor_msg[mov - 1] == 2:
                udpC.msgRT('adp')

            if vetor_msg[mov - 1] == 3:
                udpC.msgRT('contm')

            if vetor_msg[mov - 1] == 4:
                udpC.msgRT('extp')

            if vetor_msg[mov - 1]== 5:
                udpC.msgRT('flxp')

            if vetor_msg[mov - 1] == 6:
                udpC.msgRT('rotab')

            mov_transition = vetor_msg[mov - 1]
            time_before = time.time()


    mov_anterior = mov


# vetor_msg = [1,2]
# vetor_test = [0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,0,0,0,0,0,0,0,0,0,0]
# for value in vetor_test:
#     virtualArmOn(value,vetor_msg)
#     time.sleep(0.1)





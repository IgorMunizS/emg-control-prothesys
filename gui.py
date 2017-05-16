from tkinter import *
from emgClass import *
import udpConnection as udpC
import threading
import time
import data as dt
import classifica_sinal as rna
import emgRealTime as emgRT
from tkinter import filedialog
import matplotlib.pyplot as plt

class EmgGui(object):
    def __init__(self, janela):

        self.janela = janela
        self.isSampling = False
        #Primeiro frame pra label
        self.frameMain = Frame (janela)
        self.frameMain.pack()
        self.frameLabel = Frame(self.frameMain)

        self.frameLabel.pack()

        #Define tipo de fonte para Labels Canais e Grafico
        self.font = ('Verdana', '10', 'bold')

        #Frame para checkbuttons
        self.frameCheck = Frame(self.frameMain)

        self.frameCheck.pack()

        #Instancia os Labels
        self.labelCanal = Label(self.frameLabel, text="Canais", pady = 30, padx = 50, font =self.font)
        self.labelGrafico = Label(self.frameLabel, text="Gráfico", pady = 3, padx = 50, font =self.font)
        self.labelCanal.pack(side=LEFT)
        self.labelGrafico.pack(side=LEFT)

        #Variaveis do checkbutton

        self.C1 = BooleanVar()
        self.C2 = BooleanVar()
        self.C3 = BooleanVar()
        self.C4 = BooleanVar()
        self.C5 = BooleanVar()
        self.C6 = BooleanVar()
        self.C7 = BooleanVar()
        self.C8 = BooleanVar()

        self.G1 = IntVar()
        self.G2 = IntVar()
        self.G3 = IntVar()
        self.G4 = IntVar()
        self.G5 = IntVar()
        self.G6 = IntVar()
        self.G7 = IntVar()
        self.G8 = IntVar()

        self.m1 = IntVar(janela)
        self.m2 = IntVar(janela)
        self.m3 = IntVar(janela)
        self.m4 = IntVar(janela)
        self.m5 = IntVar(janela)
        self.m6 = IntVar(janela)

        #Cria um subframe pra cada linda de checkbuttons. Instancia e empacota os checkbuttons
        subframe = Frame(self.frameCheck)
        subframe.pack()

        self.checkBC1 = Checkbutton(subframe, text="1", variable=self.C1, padx=20)
        self.checkBC1.select()
        self.checkBC2 = Checkbutton(subframe, text="2", variable=self.C2, padx=20)
        self.checkBC2.select()
        self.checkGC1 = Checkbutton(subframe, text="1", variable=self.G1, padx=20)
        self.checkGC1.select()
        self.checkGC2 = Checkbutton(subframe, text="2", variable=self.G2, padx=20)
        self.checkGC2.select()

        self.checkBC1.pack(side=LEFT)

        self.checkBC2.pack(side=LEFT)
        self.checkGC1.pack(side=LEFT)
        self.checkGC2.pack(side=LEFT)

        subframe = Frame(self.frameCheck)
        subframe.pack()

        self.checkBC3 = Checkbutton(subframe, text="3", variable=self.C3, padx=20)
        self.checkBC3.select()
        self.checkBC4 = Checkbutton(subframe, text="4", variable=self.C4, padx=20)
        self.checkBC4.select()
        self.checkGC3 = Checkbutton(subframe, text="3", variable=self.G3, padx=20)
        self.checkGC3.select()
        self.checkGC4 = Checkbutton(subframe, text="4", variable=self.G4, padx=20)
        self.checkGC4.select()

        self.checkBC3.pack(side=LEFT)
        self.checkBC4.pack(side=LEFT)
        self.checkGC3.pack(side=LEFT)
        self.checkGC4.pack(side=LEFT)

        subframe = Frame(self.frameCheck)
        subframe.pack()

        self.checkBC5 = Checkbutton(subframe, text="5", variable=self.C5, padx=20)
        self.checkBC5.select()
        self.checkBC6 = Checkbutton(subframe, text="6", variable=self.C6, padx=20)
        self.checkBC6.select()
        self.checkGC5 = Checkbutton(subframe, text="5", variable=self.G5, padx=20)
        self.checkGC5.select()
        self.checkGC6 = Checkbutton(subframe, text="6", variable=self.G6, padx=20)
        self.checkGC6.select()

        self.checkBC5.pack(side=LEFT)
        self.checkBC6.pack(side=LEFT)
        self.checkGC5.pack(side=LEFT)
        self.checkGC6.pack(side=LEFT)

        subframe = Frame(self.frameCheck)
        subframe.pack()

        self.checkBC7 = Checkbutton(subframe, text="7", variable=self.C7, padx=20)
        self.checkBC7.select()
        self.checkBC8 = Checkbutton(subframe, text="8", variable=self.C8, padx=20)
        self.checkBC8.select()

        self.checkGC7 = Checkbutton(subframe, text="7", variable=self.G7, padx=20)
        self.checkGC7.select()
        self.checkGC8 = Checkbutton(subframe, text="8", variable=self.G8, padx=20)
        self.checkGC8.select()

        self.checkBC7.pack(side=LEFT)
        self.checkBC8.pack(side=LEFT)
        self.checkGC7.pack(side=LEFT)
        self.checkGC8.pack(side=LEFT)



        self.desconectado = True
        self.frameEntry = Frame(self.frameMain)
        self.frameEntryData = Frame(self.frameMain)
        self.frameButtons = Frame(self.frameMain)

        self.frameEntry.pack()
        self.frameEntryData.pack()
        self.frameButtons.pack()


        self.sampleRateValue = Label(self.frameEntry, text="Sample Rate(Hz): ", pady=20)
        self.sampleRateValue.pack(side=LEFT)



        self.form = Entry(self.frameEntry, width= 10)
        self.form.insert(0, "1000")
        self.form.pack(side=LEFT, padx = 5)

        self.sampleTimeValue = Label(self.frameEntry, text="Sample Time(seconds): ", pady=20)
        self.sampleTimeValue.pack(side=LEFT)

        self.form2 = Entry(self.frameEntry, width= 10)
        self.form2.insert(0, "0")
        self.form2.pack(side=LEFT, padx = 5)

        self.nameText = Label(self.frameEntryData, text='Nome: ', pady=10)
        self.nameText.pack(side=LEFT)

        self.nameEntry = Entry(self.frameEntryData, width = 18)
        self.nameEntry.pack(side=LEFT)

        self.movText = Label(self.frameEntryData, text="Movimento: ")
        self.movText.pack(side=LEFT, padx=5)


        self.listMov = Spinbox(self.frameEntryData, width='20', value=('Abdução do punho', 'Adução do punho', 'Contração da mão', 'Extensão do punho', 'Flexão do punho', 'Rotação do antebraço'))
        self.listMov.pack(side=LEFT)

        subframeb = Frame(self.frameButtons)
        subframeb.pack()
        self.conecta = Button(subframeb, text="Conectar", command=self.conectar, width=15)
        self.conecta.pack(side=LEFT, padx = 2)

        self.desconecta = Button(subframeb, text="Desconectar", command=self.desconectar, width=15)
        self.desconecta.pack(side=LEFT, pady=5)

        subframeb = Frame(self.frameButtons)
        subframeb.pack()
        self.coleta = Button(subframeb, text ="Coletar", command=self.coletar, width=15)
        self.coleta.pack(side = LEFT, padx = 2)

        self.stopColeta = Button(subframeb, text = "Parar", command=self.pararColeta, width=15)
        self.stopColeta.pack(side = LEFT, pady = 5)

        subframeb = Frame(self.frameButtons)
        subframeb.pack()
        self.stopColeta = Button(subframeb, text="Movimentos", command=self.movimentos, width=15)
        self.stopColeta.pack(side = LEFT, padx= 2)

        self.treina = Button(subframeb, text="Treinar", width=15, command=self.treina)
        self.treina.pack(side=LEFT, pady=5)

        self.frameLabel = Frame(self.frameMain)

        self.frameLabel.pack()

        self.online = Label(self.frameLabel, text='Emg Tempo Real ', font=self.font)
        self.online.pack(pady=20)

        subframe_check = Frame(self.frameLabel)
        subframe_check.pack()

        self.check1 = Checkbutton(subframe_check, text="ABP", variable=self.m1)
        self.check1.select()
        self.check1.pack(side=LEFT)

        self.check2 = Checkbutton(subframe_check, text="ADP", variable=self.m2)
        self.check2.select()
        self.check2.pack(side=LEFT)

        self.check3 = Checkbutton(subframe_check, text="CONTM", variable=self.m3)
        self.check3.select()
        self.check3.pack(side=LEFT)

        self.check4 = Checkbutton(subframe_check, text="EXTP", variable=self.m4)
        self.check4.select()
        self.check4.pack(side=LEFT)

        self.check5 = Checkbutton(subframe_check, text="FLXP", variable=self.m5)
        self.check5.select()
        self.check5.pack(side=LEFT)

        self.check6 = Checkbutton(subframe_check, text="ROTAB", variable=self.m6)
        self.check6.select()
        self.check6.pack(side=LEFT)

        self.frameOnline = Frame(self.frameMain)
        self.frameOnline.pack()

        self.nome_on = Label(self.frameOnline, text='Rede: ')
        self.nome_on.pack(side=LEFT, padx=10, pady=10)

        self.entry_on = Entry(self.frameOnline, width=15)
        self.entry_on.pack(side=LEFT)

        self.btt_entry_on = Button(self.frameOnline, width=2, text='..', command=self.openFile)
        self.btt_entry_on.pack(side=LEFT)


        self.btt_on = Button(self.frameOnline, width=7, text='Testar', command=self.testar)
        self.btt_on.pack(side=LEFT, padx=10)

        self.btt_stop_on = Button(self.frameOnline, width=7, text='Parar', command=self.pararColetaRT)
        self.btt_stop_on.pack(side=LEFT)

        self.frameLabel = Frame(self.frameMain)

        self.frameLabel.pack()

        self.msgLabel = Label(self.frameLabel, text ="Desconectado", fg='red')
        self.msgLabel.pack(pady=20)

    def conectar(self):
        canal_marcado = [self.C1.get(), self.C2.get(), self.C3.get(), self.C4.get(), self.C5.get(), self.C6.get(),
                         self.C7.get(), self.C8.get()]

        grafico_marcado = [self.G1.get(), self.G2.get(), self.G3.get(), self.G4.get(), self.G5.get(), self.G6.get(),
                         self.G7.get(), self.G8.get()]


        self.vetor_canal = []

        self.vetor_grafico = []

        x = 0
        for i in canal_marcado:
            if i:
                self.vetor_canal.append(x)
            x += 1

        x = 0
        for i in grafico_marcado:
            if i:
                self.vetor_grafico.append(x)
            x += 1


        self.desconectado = False

        self.emg = EmgEquipment(float(self.form.get()), self.form2.get(), self.vetor_canal, self.vetor_grafico)
        isConnect =  self.emg.conecta_equip()
        if isConnect:
            self.msgLabel['text'] = 'Conectado'
            self.msgLabel['fg'] = 'green'


    def coletar(self):

        self.msgLabel['text'] = "Coletando..."
        self.msgLabel['fg'] = 'blue'
        self.isSampling = True

        self.emg.coleta()

        self.mov = self.listMov.get()

        if self.mov == 'Abdução do punho':
            t = threading.Thread(target=udpC.aux_coleta, args=('abp', ))
            t.start()


        if self.mov == 'Adução do punho':
            t = threading.Thread(target=udpC.aux_coleta, args=('adp', ))
            t.start()

        if self.mov == 'Contração da mão':
            t = threading.Thread(target=udpC.aux_coleta, args=('contm', ))
            t.start()

        if self.mov == 'Extensão do punho':
            t = threading.Thread(target=udpC.aux_coleta, args=('extp', ))
            t.start()

        if self.mov == 'Flexão do punho':
            t = threading.Thread(target=udpC.aux_coleta, args=('flxp', ))
            t.start()

        if self.mov == 'Rotação do antebraço':
            t = threading.Thread(target=udpC.aux_coleta, args=('rotab', ))
            t.start()

        time.sleep(0.2)
        self.loopColeta()


    def loopColeta(self):
        self.emg.loopColeta()
        if self.emg.isSampling:
            self.coleta.after(100, self.loopColeta)
        if not self.emg.isSampling and self.isSampling:
            self.pararColeta()



    def pararColeta(self):
        self.isSampling =False
        self.msgLabel['text'] = 'Conectado'
        self.msgLabel['fg'] = 'green'
        self.emg.pararColeta()
        self.salvarArq()


    def movimentos(self):
        janelaMov = Tk()

        MovGui(janelaMov)

        janelaMov.title('Mov')

        janelaMov.geometry("200x400")

        janelaMov.mainloop()

    def treina(self):

        janelaTreina = Tk()
        TreinaGui(janelaTreina)
        janelaTreina.title('Treinamento')
        janelaTreina.geometry("400x600")
        janelaTreina.mainloop()


    def salvarArq(self):
        arqname = self.nameEntry.get()
        arqname = arqname + '_' + self.mov + '.txt'

        arq = open(arqname, 'w')

        for c in self.emg.canais:
            arq.write('===============Canal' + str(c) + '=================\n\n')
            for value in self.emg.emgData[c]:
                arq.write(str(value) + '\n')
        arq.close()

    def testar(self):
        self.msgLabel['text'] = "Testando..."
        self.msgLabel['fg'] = 'blue'
        self.isSampling = True
        self.vetor_mov = [self.m1.get(), self.m2.get(), self.m3.get(), self.m4.get(), self.m5.get(), self.m6.get()]
        self.RNA, self.vetor_msg = emgRT.loadRNA(self.entry_on.get(), self.vetor_mov)
        self.delay = []


        self.emg.coletaRT()



        time.sleep(0.2)
        self.loopColetaRT()

    def loopColetaRT(self):
        now = time.time()
        self.emg.loopColetaRT()
        self.salvarArqRT()
        vec = dt.get_data_RT('data_rt.txt')

        t = threading.Thread(target=emgRT.emgrt, args=(self.RNA, self.emg.emgDataRT, self.vetor_msg,))
        t.start()
        tempo = int(100-(time.time() - now)*1000)
        self.delay.append((time.time() - now)*1000)

        if self.emg.isSampling:
            self.btt_on.after(tempo, self.loopColetaRT)
        if not self.emg.isSampling and self.isSampling:
            self.pararColetaRT()

    def pararColetaRT(self):
        self.isSampling = False
        self.msgLabel['text'] = 'Pronto!'
        self.msgLabel['fg'] = 'green'
        self.emg.pararColetaRT()
        plt.plot(self.delay)
        plt.show()

    def salvarArqRT(self):
        arqname = 'data_rt.txt'


        arq = open(arqname, 'w')

        for c in self.emg.canais:
            arq.write('===============Canal' + str(c) + '=================\n\n')
            for value in self.emg.emgDataRT[c]:
                arq.write(str(value) + '\n')
        arq.close()

    def openFile(self):

        self.path = filedialog.askopenfilename()
        self.entry_on.insert(0, self.path)



    def desconectar(self):
        self.desconectado = True
        self.emg.desliga_equip()
        self.msgLabel['text'] = 'Desconectado'
        self.msgLabel['fg'] = 'red'


class MovGui(object):
    def __init__(self, janela):

        self.frameButtons = Frame(janela)
        self.frameButtons.pack()

        self.frameLabel = Frame(janela)
        self.frameLabel.pack()

        self.font = ('Verdana', '10', 'bold')

        #botões

        self.but_abp = Button(self.frameButtons, text='abp', command= lambda: self.mov('abp'), width='10')
        self.but_abp.pack(pady = 5)
        self.but_adp = Button(self.frameButtons, text='adp', command=lambda: self.mov('adp'), width='10')
        self.but_adp.pack(pady = 5)
        self.but_contm = Button(self.frameButtons, text='contm', command=lambda: self.mov('contm'), width='10')
        self.but_contm.pack(pady = 5)
        self.but_extp = Button(self.frameButtons, text='extp', command=lambda: self.mov('extp'), width='10')
        self.but_extp.pack(pady = 5)
        self.but_flxp = Button(self.frameButtons, text='flxp', command=lambda: self.mov('flxp'), width='10')
        self.but_flxp.pack(pady = 5)
        self.but_rotab = Button(self.frameButtons, text='rotab', command=lambda: self.mov('rotab'), width='10')
        self.but_rotab.pack(pady = 5)

        self.movLabel = Label(self.frameLabel, pady = 30, padx = 50, font=self.font)
        self.movLabel.pack()


    def mov(self, msg):

        if msg == 'abp':
            self.movLabel['text'] = 'Abdução do Punho'

        if msg == 'adp':
            self.movLabel['text'] = 'Adução do Punho'

        if msg == 'contm':
            self.movLabel['text'] = 'Contração da mão'

        if msg == 'extp':
            self.movLabel['text'] = 'Extensão do punho'

        if msg == 'flxp':
            self.movLabel['text'] = 'Flexão do punho'

        if msg == 'rotab':
            self.movLabel['text'] = 'Rotação do antebraço'


        t = threading.Thread(target=self.conectar, args=(msg,))
        t.start()

    def conectar(self, msg):
        udpC.connect(msg)


class TreinaGui(object):
    def __init__(self, janela):

        self.m1 = IntVar(janela)
        self.m2 = IntVar(janela)
        self.m3 = IntVar(janela)
        self.m4 = IntVar(janela)
        self.m5 = IntVar(janela)
        self.m6 = IntVar(janela)


        self.frameMain = Frame(janela)
        self.frameMain.pack()
        self.frameLabel = Frame(self.frameMain)

        self.frameLabel.pack()
        self.frameCaract = Frame(self.frameMain)
        self.frameCaract.pack()

        # Define tipo de fonte para Labels
        self.font = ('Verdana', '10', 'bold')
        self.caract = Label(self.frameLabel, text='Características ', font=self.font)
        self.caract.pack(pady=20)

        subframe_check = Frame(self.frameCaract)
        subframe_check.pack()

        self.check1 = Checkbutton(subframe_check, text="ABP", variable=self.m1, padx=20)
        self.check1.select()
        self.check1.pack(side=LEFT)

        self.check2 = Checkbutton(subframe_check, text="ADP", variable=self.m2, padx=20)
        self.check2.select()
        self.check2.pack(side=LEFT)

        self.check3 = Checkbutton(subframe_check, text="CONTM", variable=self.m3, padx=20)
        self.check3.select()
        self.check3.pack(side=LEFT, pady=10)

        subframe_check2 = Frame(self.frameCaract)
        subframe_check2.pack()

        self.check4 = Checkbutton(subframe_check2, text="EXTP", variable=self.m4, padx=20)
        self.check4.select()
        self.check4.pack(side=LEFT)

        self.check5 = Checkbutton(subframe_check2, text="FLXP", variable=self.m5, padx=20)
        self.check5.select()
        self.check5.pack(side=LEFT)

        self.check6 = Checkbutton(subframe_check2, text="ROTAB", variable=self.m6, padx=20)
        self.check6.select()
        self.check6.pack(side=LEFT, pady=10)

        self.nome_caract = Label(self.frameCaract, text='Nome: ')
        self.nome_caract.pack(side=LEFT, padx=10)

        self.entry_caract = Entry(self.frameCaract, width=18)
        self.entry_caract.pack(side = LEFT)

        self.btt_caract = Button(self.frameCaract, text='Extrair', width= 10, command=self.extrair)
        self.btt_caract.pack(side=LEFT, padx=10)

        self.frameLabel = Frame(self.frameMain)

        self.frameLabel.pack()



        self.caract = Label(self.frameLabel, text='Rede Neural ', font=self.font)
        self.caract.pack(pady=20)

        self.frameRNA = Frame(self.frameMain)
        self.frameRNA.pack()





        self.nome_rna = Label(self.frameRNA, text='Características: ')
        self.nome_rna.pack(side=LEFT, padx=10, pady= 10)

        self.entry_rna = Entry(self.frameRNA, width=18)
        self.entry_rna.pack(side = LEFT)

        self.rna_btt = Button(self.frameRNA, text='Treinar', width=10, command=self.treinar)
        self.rna_btt.pack(side=LEFT, padx= 10)



        self.frameMSG = Frame(self.frameMain)
        self.frameMSG.pack()

        self.msgLabel = Label(self.frameMSG, font=self.font)
        self.msgLabel.pack(pady=40)



    def extrair(self):
        def extrair_thread():
            self.msgLabel['text'] = 'Extraindo características...'
            self.msgLabel['fg'] = 'red'
            vetor_mov = [self.m1.get(), self.m2.get(), self.m3.get(), self.m4.get(), self.m5.get(), self.m6.get()]
            print(vetor_mov)
            self.stringMov =''
            for j in range(len(vetor_mov)):
                if vetor_mov[j]:
                    self.stringMov = self.stringMov + str(j+1)


            dados = dt.get_data(self.entry_caract.get(), vetor_mov)
            data = dt.windowing(dados)
            matrix = dt.extrair_caract(data)
            dt.salva_caract(matrix, self.entry_caract.get())
            dt.salva_caract_visual(matrix, self.entry_caract.get())
            self.msgLabel['text'] = 'Pronto!'
            self.msgLabel['fg'] = 'green'


        t = threading.Thread(target=extrair_thread)
        t.start()

    def treinar(self):
        def treinar_thread():
            self.msgLabel['text'] = 'Treinando a rede...'
            self.msgLabel['fg'] = 'red'
            data, self.tam = rna.get_data_infile(self.entry_rna.get() + '_caract.txt')
            res = rna.rna_mlp(data,int(self.tam/773) +1, self.entry_rna.get() + self.stringMov)
            self.msgLabel['text'] = 'Melhor resultado: ',str(res) + '%!'
            self.msgLabel['fg'] = 'green'
        t = threading.Thread(target=treinar_thread)
        t.start()







janela = Tk()

inst = EmgGui(janela)

janela.title("Análise de sinais EMG")

janela.geometry("400x600")

janela.mainloop()

if inst.desconectado == False:
    inst.emg.desliga_equip()

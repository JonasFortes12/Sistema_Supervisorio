import tkinter as tk
from tkinter import Frame, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial as sr

#janelas
root1 = tk.Tk()
root2 = tk.Tk()

#Instância da porta serial lida
serialPort = sr.Serial('COM8',9600) 
serialPort.reset_input_buffer()

#variáveis do intervalo dos graficos
a = 0
b = 100

#parâmetros iniciais
i = 1 #eixo x
activation = False #ativar/desativar o gráfico

#dados de plotagem
xData = []
yData = []

class Grafic():

    def __init__(self):
        #criando uma figura 1:
        self.figure1 = plt.figure(figsize=(10, 6), dpi=70) #Define as dimensões da figura
        self.g1 = self.figure1.add_subplot(111) #Coloca a figura dentro da variavel grafico
        self.g1.set_title('Serial Data')
        self.g1.set_xlabel('Sample')
        self.g1.set_ylabel('Tension')
        self.g1.set_xlim(a, b)
        self.g1.set_ylim(-1,1100)

        self.lines1 = self.g1.plot([],[])[0] #(Explicar)

        self.canva1 = FigureCanvasTkAgg(self.figure1, master = root2) #Instancia a figura dentro da janela  
        self.canva1.get_tk_widget().place(relx=0.2, rely=0.05,
                                        relwidth=0.60, relheight=0.70)# Tamnaho e posição na tela
        self.canva1.draw()

        self.plot_data()

    def update_data(self):
        global i, a, b

        self.data = serialPort.readline()
        print(self.data)
        self.data.decode()
        
        xData.append(i)
        yData.append(int(self.data))

        i = i+1

        if(i>b):
            a = a + 1
            b = b + 1
            self.g1.set_xlim(a, b)

    def plot_data(self):
        if(activation == True):
            self.update_data()
            
            self.lines1.set_xdata(xData)
            self.lines1.set_ydata(yData)
                
            self.canva1.draw()
                
            root2.after(1,self.plot_data)
        else:
            root2.after(1,self.plot_data)

    def changeActivation(self):
        global activation
        activation = not activation

    def reset(self):
        global xData, yData, i, a, b
        xData = []
        yData = []
        i = 1 #eixo x
        a = 0
        b = 100
        
        self.g1.set_xlim(a, b)
        self.plot_data()

class Application(Grafic):

    def __init__(self):
        self.root1 = root1
        self.root2 = root2
        self.screen1()
        self.widgetsScreen1()
        root1.mainloop()

    def screen1(self):
        self.root1.title("Configurações")
        self.root1.configure(background='#371E30')
        self.root1.geometry("900x500")
        self.root1.resizable(False, False)

    def screen2(self):
        self.root2.title("Dados")
        self.root2.configure(background='#371E30')
        self.root2.resizable(True, True) #Responsividade
        self.root2.geometry("1100x700")
    
    def widgetsScreen1(self):

        def confirmButtonAction(): 
            
            self.bitSec = self.cbBitSec.get()
            self.bitData = self.cbBitData.get()
            self.bitStop = self.cbBitStop.get()
            self.port = self.entryPort.get()
            self.parity = self.cbParity.get()
            self.fluxContr = self.cbFluxContr.get()

            self.root1.destroy()
            self.screen2()
            self.widgetsScreen2()
            self.frameScreen2()#frames da tela 2
            self.infoConfig()
       
        def cancelButtonAction(): 
            self.root1.destroy()


        #Botão Confirmar
        self.confirmButton = tk.Button(self.root1, text="Confirm", font = ('calbiri',15), 
        command=confirmButtonAction)
        self.confirmButton.place(relx=0.73, rely=0.85, relwidth=0.15, relheight=0.08)

        #Botão Cancelar
        self.cancelButton = tk.Button(self.root1, text="Cancel", font = ('calbiri',15),
        command=cancelButtonAction)
        self.cancelButton.place(relx=0.15, rely=0.85, relwidth=0.15, relheight=0.08)


        #criando labels e entradas
        bitSecValues = ["9600", "700", "580"]
        bitDataValues = ["10", "9", "8", "7", "6", "5", "4"]
        parityValues = ["Nenhum", "12", "Padrão"]
        bitsStopValues = ["1", "2", "4"]
        fluxContrValues = ["Nenhum", "Padrão", "Automático"]
        

        self.lbBitSec = tk.Label(self.root1, text= "Bits por segundo", font=('calbiri',15))
        self.lbBitSec.place(relx= 0.20, rely= 0.30, relwidth= 0.18)
        self.cbBitSec = ttk.Combobox(self.root1, values=bitSecValues, font=('calbiri',15))
        self.cbBitSec.place(relx= 0.20, rely= 0.35, relwidth= 0.18)
        self.cbBitSec.set("9600")

        self.lbBitData = tk.Label(self.root1, text= "Bits de dados", font=('calbiri',15))
        self.lbBitData.place(relx= 0.20, rely= 0.42, relwidth= 0.18)
        self.cbBitData = ttk.Combobox(self.root1, values=bitDataValues, font=('calbiri',15))
        self.cbBitData.place(relx= 0.20, rely= 0.47, relwidth= 0.18)
        self.cbBitData.set("8")

        self.lbBitStop = tk.Label(self.root1, text= "Bits de Parada", font=('calbiri',15))
        self.lbBitStop.place(relx= 0.20, rely= 0.54, relwidth= 0.18)
        self.cbBitStop = ttk.Combobox(self.root1, values=bitsStopValues, font=('calbiri',15))
        self.cbBitStop.place(relx= 0.20, rely= 0.59, relwidth= 0.18)
        self.cbBitStop.set("1")
        
        self.lbPort= tk.Label(self.root1, text="Porta", font=('calbiri',15))
        self.lbPort.place(relx= 0.65, rely= 0.30, relwidth= 0.18)
        self.entryPort = tk.Entry(self.root1, font=('calbiri',15))
        self.entryPort.place(relx= 0.65, rely= 0.35, relwidth= 0.18)
        
        
        self.lbParity = tk.Label(self.root1, text= "Paridade", font=('calbiri',15))
        self.lbParity.place(relx= 0.65, rely= 0.42, relwidth= 0.18)
        self.cbParity = ttk.Combobox(self.root1, values=parityValues, font=('calbiri',15))
        self.cbParity.place(relx= 0.65, rely= 0.47, relwidth= 0.18)
        self.cbParity.set("Nenhum")


        self.lbFluxContr = tk.Label(self.root1, text= "Controle de fluxo", font=('calbiri',15))
        self.lbFluxContr.place(relx= 0.65, rely= 0.54, relwidth= 0.18)
        self.cbFluxContr = ttk.Combobox(self.root1, values=fluxContrValues, font=('calbiri',15))
        self.cbFluxContr.place(relx= 0.65, rely= 0.59, relwidth= 0.18)
        self.cbFluxContr.set("Nenhum")

    def widgetsScreen2(self):
         
        btStart = tk.Button(root2, text = "Start/Stop", font = ('calbiri',15), 
            command = lambda: self.changeActivation())
        btStart.place(relx = 0.54, rely = 0.77, relwidth=0.12, relheight=0.07)

        btReset = tk.Button(root2, text = "Reset", font = ('calbiri',15), 
            command = lambda: self.reset())
        btReset.place(relx = 0.34, rely = 0.77, relwidth=0.12, relheight=0.07)

        Grafic()

    def frameScreen2(self):
        self.frame1 = Frame(self.root2, bg='#a1026c', 
            highlightbackground='#1e372c', highlightthickness=2)
        self.frame1.place(relx=0.05 , rely= 0.87, relwidth=0.9, relheight=0.12)

    def infoConfig(self):
        #Label info bits por segundo
        self.lbInfoBitSec = tk.Label(self.frame1, 
            text= 'Bits por Segundo: ' + str(self.bitSec), font=('calbiri',12))
        self.lbInfoBitSec.place(relx= 0.03, rely= 0.1, relwidth= 0.3)

        #Label info bits de dados
        self.lbInfoBitData = tk.Label(self.frame1, 
            text= 'Bits de Dados: ' + str(self.bitData), font=('calbiri',12))
        self.lbInfoBitData.place(relx= 0.36, rely= 0.1, relwidth= 0.3)

        #Label info bit de parada
        self.lbInfoBitStop = tk.Label(self.frame1, 
            text= 'Bit de Parada: ' + str(self.bitStop), font=('calbiri',12))
        self.lbInfoBitStop.place(relx= 0.69, rely= 0.1, relwidth= 0.3)

        #Label info porta
        self.lbInfoPort = tk.Label(self.frame1, 
            text= 'Porta: ' + str(self.port), font=('calbiri',12))
        self.lbInfoPort.place(relx= 0.03, rely= 0.6, relwidth= 0.3)

        #Label info paridade
        self.lbInfoParity = tk.Label(self.frame1, 
            text= 'Paridade: ' + str(self.parity), font=('calbiri',12))
        self.lbInfoParity.place(relx= 0.36, rely= 0.6, relwidth= 0.3)

        #Label info paridade
        self.lbInfoFluxContr = tk.Label(self.frame1, 
            text= 'Controle de Fluxo: ' + str(self.fluxContr), font=('calbiri',12))
        self.lbInfoFluxContr.place(relx= 0.69, rely= 0.6, relwidth= 0.3)


Application()

import tkinter
from tkinter import *
import time
import customtkinter
from PIL import ImageTk, Image, ImageOps
import serial, time
from pyvidplayer import Video
import pygame,sys




arduino = serial.Serial(port='COM4', baudrate=115200, bytesize=8,timeout=1)

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class juego:
    def __init__(self, master): 
        self.buttons_pressed = []
        
        def videoEmpate():
            root.destroy()
            WIDTH, HEIGHT = 1200, 900
            SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
            vid = Video("TIe Video.mp4")
            vid.set_size((1200,900))
            while True:
                vid.draw(SCREEN, (0, 0))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        vid.close()
                        pygame.quit()
                        break

        def videoVictoria():
            root.destroy()
            WIDTH, HEIGHT = 1200, 900
            SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
            vid = Video("Victory_Screen.mp4")
            vid.set_size((1200,900))
            while True:
                vid.draw(SCREEN, (0, 0))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        vid.close()
                        pygame.quit()
                        break


        def videoDerrota():
            root.destroy()
            WIDTH, HEIGHT = 1200, 900
            SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
            vid = Video("Defeat_Screen.mp4")
            vid.set_size((1200,900))
            while True:
                vid.draw(SCREEN, (0, 0))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        vid.close()
                        pygame.quit()
                        break

        

        self.misilesDisponibles = 10
        self.barcosDisponibles = 10

        self.turno = 1
        
        self.orientacion = ""
        
        self.cont3 = 3

        self.cont2 = 2

        self.cont1 = 1

        self.tipoBarco = 0

        self.pos = 0

        self.posX = 0
        self.posY = 0
        
        self.master = master
        root.geometry('1000x600')
        root.minsize(1000, 600)
        root.maxsize(1000, 600)
        root.resizable(0, 0)
  
        #Imagenes-------------------------------------------------------------------------------------------
        
        imagenFondo = customtkinter.CTkImage(Image.open("imagen1.jpg"),size=(1000, 600))
       
        #---------------------------------------------------------------------------------------------------
       
        self.__background = customtkinter.CTkLabel(root,
                                  image=imagenFondo,text='')
        self.__background.place(relx=0,
                                rely=0,
                                relwidth=1,
                                relheight=1)
        
        #Labels--------------------------------------------------------------------------------------------
        self.labelBarcos = customtkinter.CTkLabel(master=root, text="BARCOS DISPONIBLES: 10",font=("Roboto",30),fg_color=("white","#2b2b2b"))
        self.labelBarcos.place(x= 25,y=10)

        self.labelMisiles = customtkinter.CTkLabel(master=root, text="MISILES DISPONIBLES: 10",font=("Roboto",30),fg_color=("white","#2b2b2b"))
        self.labelMisiles.place(x= 25,y=309)

       
        #Funciones---------------------------------------------------------------------------------------------------------
        def sendCoordenates(x,y):
            pos_x = bytes(str(x-1), 'utf-8')      # Si quiero que sean numeros, le quito str
            pos_y = bytes(str(y-1), 'utf-8')      # pero me va a dar error de encode.
            arduino.write(pos_x)
            arduino.write(pos_y)
            print(f'Posicion ({pos_x},{pos_y}) ENVIADA al Arduino')
          
        def eliminar():
         root.destroy() 
        
        frameRonda = customtkinter.CTkFrame(master=root,
                               width=260,
                               height=50,
                               corner_radius=0)
        frameRonda.place(x=650, y=5)
        frameRonda.labelRonda = customtkinter.CTkLabel(frameRonda, text="Ronda 1", width=250,height=40,font=("Roboto",25))
        frameRonda.labelRonda.grid(row=0, column=0, padx=3, pady=7)

        def ventanaResultados():
            ventanaEspera = customtkinter.CTkToplevel(root)
            ventanaEspera.geometry("400x200")
            label = customtkinter.CTkLabel(ventanaEspera, text="ESPERANDO RESULTADOS...")
            label.pack(side="top", fill="both", expand=True, padx=40, pady=40)

        def esperandoResultado():
            puntajeJA = 0
            puntajeJB = 0
            num = 0
            while True:
                resultado = arduino.readline()
                if(resultado != b''):
                    if(num == 0):
                     puntajeJA = int(resultado.decode())*100
                     num += 1
                     print(" ")
                     print("*PUNTAJES*")
                     print("----------------------------------------------")
                     print("-Puntaje del juagdor de Python:"+str(puntajeJA))
                    else:
                     puntajeJB = int(resultado.decode())*100
                     num += 1
                     print("-Puntaje del jugador de Arduino:"+str(puntajeJB))
                     print("----------------------------------------------")
                     break
            if  puntajeJA > puntajeJB:
                videoVictoria()
            elif puntajeJA < puntajeJB:
                videoDerrota()
            elif puntajeJA == puntajeJB:
                videoEmpate()

        def habilitarBotones():
            frameMenu.botonBarco3.configure(state = "normal",fg_color ="#1c6ca4",hover_color="#144c74")
            frameMenu.botonBarco2.configure(state = "normal",fg_color ="#1c6ca4",hover_color="#144c74") 
            frameMenu.botonBarco1.configure(state = "normal",fg_color ="#1c6ca4",hover_color="#144c74")
            frameMenu.botonDireccionH.configure(state = "normal",fg_color ="#1c6ca4",hover_color="#144c74")
            frameMenu.botonDireccionV.configure(state = "normal",fg_color ="#1c6ca4",hover_color="#144c74") 

        def verificarPosicion(x,y):
            bool = False
            if self.orientacion == "H":          
                if self.tipoBarco == 3:
                    if (self.cont3 > 0):
                        if (self.pos == 0):
                            self.pos =+ 1
                            self.posX = x
                            self.posY = y
                            self.cont3 -= 1
                            bool = True
                        else:
                            if((y == self.posY + 1 or y == self.posY -1) and x == self.posX):
                                self.posY = y
                                self.cont3 -= 1
                                bool = True
                        if (self.cont3 == 0):
                            habilitarBotones()
                            self.barcosDisponibles -= 1 
                            self.pos = 0
                            self.posX = 0
                            self.posY = 0
                            self.cont3 = 3
                            self.orientacion = ""
                            self.tipoBarco = 0
                            bool = True
                elif  self.tipoBarco == 2:
                    if (self.cont2 > 0):
                        if (self.pos == 0):
                            self.pos =+ 1
                            self.posX = x
                            self.posY = y
                            self.cont2 -= 1
                            bool = True
                        else:
                            if((y == self.posY + 1 or y == self.posY -1) and x == self.posX):
                                self.posY = y
                                self.cont2 -= 1
                                bool = True
                        if (self.cont2 == 0):
                            habilitarBotones()
                            self.barcosDisponibles -= 1 
                            self.pos = 0
                            self.posX = 0
                            self.posY = 0
                            self.cont2 = 2
                            self.orientacion = ""
                            self.tipoBarco = 0
                            bool = True
                elif self.tipoBarco == 1:
                     habilitarBotones()
                     self.barcosDisponibles -= 1 
                     self.pos = 0
                     self.posX = 0
                     self.posY = 0
                     self.cont1 = 1
                     self.orientacion = ""
                     self.tipoBarco = 0
                     bool = True
            elif self.orientacion == "V":
                if self.tipoBarco == 3:
                    if (self.cont3 > 0):
                        if (self.pos == 0):
                            self.pos =+ 1
                            self.posX = x
                            self.posY = y
                            self.cont3 -= 1
                            bool = True
                        else:
                            if((x == self.posX + 1 or x == self.posX -1) and y == self.posY):
                                self.posX = x
                                self.cont3 -= 1
                                bool = True
                        if (self.cont3 == 0):
                            habilitarBotones()
                            self.barcosDisponibles -= 1 
                            self.pos = 0
                            self.posX = 0
                            self.posY = 0
                            self.cont3 = 3
                            self.orientacion = ""
                            self.tipoBarco = 0
                            bool = True
                elif  self.tipoBarco == 2:
                    if (self.cont2 > 0):
                        if (self.pos == 0):
                            self.pos =+ 1
                            self.posX = x
                            self.posY = y
                            self.cont2 -= 1
                            bool = True
                        else:
                            if((x == self.posX + 1 or x == self.posX -1) and y == self.posY):
                                self.posX = x
                                self.cont2 -= 1
                                bool = True
                        if (self.cont2 == 0):
                            habilitarBotones()
                            self.barcosDisponibles -= 1 
                            self.pos = 0
                            self.posX = 0
                            self.posY = 0
                            self.cont2 = 2
                            self.orientacion = ""
                            self.tipoBarco = 0
                            bool = True
                elif self.tipoBarco == 1:
                     habilitarBotones()
                     self.barcosDisponibles -= 1 
                     self.pos = 0
                     self.posX = 0
                     self.posY = 0
                     self.cont1 = 1
                     self.orientacion = ""
                     self.tipoBarco = 0
                     bool = True
            return bool


        def enviarBarcos(boton,x,y):
         if (self.barcosDisponibles > 0 and self.orientacion != "" and self.tipoBarco != 0):
            if verificarPosicion(x,y):
                boton.configure(fg_color = "green")#--------------------------------------------------------------
                boton.configure(state = "disabled")
                sendCoordenates(x,y)
                self.buttons_pressed.append(boton)
                self.labelBarcos.configure(text = "BARCOS DISPONIBLES: "+str(self.barcosDisponibles))
                if(self.barcosDisponibles == 0):
                   final = bytes("P", 'utf-8')      # pero me va a dar error de encode.
                   arduino.write(final) 

        def enviarMisiles(boton,x,y):
         if (self.misilesDisponibles > 0 and self.barcosDisponibles == 0):
            boton.configure(fg_color ="#a5c5c2")
            boton.configure(text = "X",text_color="red")#---------------------------------------------------------------
            boton.configure(state = "disabled")
            self.buttons_pressed.append(boton) 
            sendCoordenates(x,y)
            self.misilesDisponibles -= 1  
            self.labelMisiles.configure(text = "MISILES DISPONIBLES: "+str(self.misilesDisponibles))
            if(self.misilesDisponibles == 0):
                self.turno += 1
                nuevaRonda()
                if self.turno == 2:
                    esperandoResultado()
        
        def nuevaRonda():
            for button in self.buttons_pressed:
                button.configure(state = "normal",fg_color ="#1c6ca4",hover_color="#144c74",text="")
            self.labelBarcos.configure(text="BARCOS DISPONIBLES: 10")
            self.labelMisiles.configure(text="MISILES DISPONIBLES: 10")
            self.misilesDisponibles = 10
            self.barcosDisponibles = 10
            frameRonda.labelRonda.configure(text="Ronda "+str(self.turno + 1),font=("Roboto",25))



#-------------------------------------------------------------------------------------------------------------------------
        #FrameMenu
        def elegirDireccion(direccion,boton1,boton2):
            if direccion == "H":
                boton1.configure(state = "disabled")
                boton1.configure(fg_color = "#ff9800")
                boton2.configure(state = "disabled")
                self.orientacion = direccion 
            else:
                self.orientacion = direccion
                boton1.configure(state = "disabled")
                boton1.configure(fg_color = "#ff9800")
                boton2.configure(state = "disabled")

        def elegirTipoBarco(num,boton1,boton2,boton3):
            if num == 3:
                boton1.configure(state = "disabled")
                boton1.configure(fg_color = "#ff9800")
                boton2.configure(state = "disabled")
                boton3.configure(state = "disabled")
                self.tipoBarco = num 
            elif num == 2:
                self.tipoBarco = num 
                boton1.configure(state = "disabled")
                boton1.configure(fg_color = "#ff9800")
                boton2.configure(state = "disabled")
                boton3.configure(state = "disabled")
            else:
                self.tipoBarco = num 
                boton1.configure(state = "disabled")
                boton1.configure(fg_color = "#ff9800")
                boton2.configure(state = "disabled")
                boton3.configure(state = "disabled")


        frameMenu = customtkinter.CTkFrame(master=root,
                               width=300,
                               height=400,
                               corner_radius=0)
        frameMenu.place(x=650, y=100)
        frameMenu.labelTitulo = customtkinter.CTkLabel(frameMenu, text="Menu", width=250,height=40,font=("Roboto",25))
        frameMenu.labelTitulo.grid(row=0, column=0, padx=3, pady=7)

        frameMenu.botonDireccionH = customtkinter.CTkButton(frameMenu,width=100,height=40,text="Horizontal",command=lambda:elegirDireccion("H",frameMenu.botonDireccionH,frameMenu.botonDireccionV))
        frameMenu.botonDireccionH.grid(row=1, column=0, padx=3, pady=7)
        frameMenu.botonDireccionV = customtkinter.CTkButton(frameMenu,width=100,height=40,text="Vertical",command=lambda:elegirDireccion("V", frameMenu.botonDireccionV,frameMenu.botonDireccionH))
        frameMenu.botonDireccionV.grid(row=2, column=0, padx=3, pady=7)

        frameMenu.label = customtkinter.CTkLabel(frameMenu, text="", width=250,height=1)
        frameMenu.label.grid(row=3, column=0, padx=3, pady=7)

        frameMenu.botonBarco3 = customtkinter.CTkButton(frameMenu,width=100,height=40,text="Barco de 3",command=lambda:elegirTipoBarco(3,frameMenu.botonBarco3,frameMenu.botonBarco2,frameMenu.botonBarco1))
        frameMenu.botonBarco3.grid(row=4, column=0, padx=3, pady=7)
        frameMenu.botonBarco2 = customtkinter.CTkButton(frameMenu,width=100,height=40,text="Barco de 2",command=lambda:elegirTipoBarco(2,frameMenu.botonBarco2,frameMenu.botonBarco3,frameMenu.botonBarco1))
        frameMenu.botonBarco2.grid(row=5, column=0, padx=3, pady=7)
        frameMenu.botonBarco1 = customtkinter.CTkButton(frameMenu,width=100,height=40,text="Barco de 1",command=lambda:elegirTipoBarco(1,frameMenu.botonBarco1,frameMenu.botonBarco2,frameMenu.botonBarco3))
        frameMenu.botonBarco1.grid(row=6, column=0, padx=3, pady=7)

        frameMenu.label1 = customtkinter.CTkLabel(frameMenu, text="", width=250,height=1,font=("Roboto",25))
        frameMenu.label1.grid(row=7, column=0, padx=1, pady=1)

        

        
       
#----------------------------------------------------------------------------------------------------------------------------------------------      
        #Frame barcos
        frameBarcos = customtkinter.CTkFrame(master=root,
                               width=200,
                               height=250,
                               corner_radius=0)
        frameBarcos.place(x=25, y=50)

        #filas labels barcos 
        frameBarcos.indice = customtkinter.CTkLabel(frameBarcos, text=" ", width=20,height=40,font=("Roboto",15))
        frameBarcos.indice.grid(row=0, column=0, padx=3, pady=7)
        frameBarcos.labelA = customtkinter.CTkLabel(frameBarcos, text="A", width=40,height=40,font=("Roboto",15),fg_color=("white", "#E78D1E"))
        frameBarcos.labelA.grid(row=1, column=0, padx=7, pady=1)
        frameBarcos.labelB = customtkinter.CTkLabel(frameBarcos,width=40,height=40,text="B",font=("Roboto",15),fg_color=("white", "#E78D1E"))
        frameBarcos.labelB.grid(row=2, column=0, padx=7, pady=1)
        frameBarcos.labelC = customtkinter.CTkLabel(frameBarcos,width=40,height=40,text="C",font=("Roboto",15),fg_color=("white", "#E78D1E"))
        frameBarcos.labelC.grid(row=3, column=0, padx=7, pady=1)
        frameBarcos.labelD = customtkinter.CTkLabel(frameBarcos,width=40,height=40,text="D",font=("Roboto",15),fg_color=("white", "#E78D1E"))
        frameBarcos.labelD.grid(row=4, column=0, padx=7, pady=1)
        frameBarcos.indice1 = customtkinter.CTkLabel(frameBarcos,width=40,height=5,text=" ",font=("Roboto",15))
        frameBarcos.indice1.grid(row=5, column=0, padx=7, pady=1)

        #filas columnas barcos
        frameBarcos.label1 = customtkinter.CTkLabel(frameBarcos, text="1", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameBarcos.label1.grid(row=0, column=1, padx=1, pady=7)
        frameBarcos.label2 = customtkinter.CTkLabel(frameBarcos, text="2", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameBarcos.label2.grid(row=0, column=2, padx=1, pady=7)
        frameBarcos.label3 = customtkinter.CTkLabel(frameBarcos, text="3", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameBarcos.label3.grid(row=0, column=3, padx=1, pady=7)
        frameBarcos.label4 = customtkinter.CTkLabel(frameBarcos, text="4", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameBarcos.label4.grid(row=0, column=4, padx=1, pady=7)
        frameBarcos.label5 = customtkinter.CTkLabel(frameBarcos, text="5", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameBarcos.label5.grid(row=0, column=5, padx=1, pady=7)
        frameBarcos.label6 = customtkinter.CTkLabel(frameBarcos, text="6", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameBarcos.label6.grid(row=0, column=6, padx=1, pady=7)
        frameBarcos.label7 = customtkinter.CTkLabel(frameBarcos, text="7", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameBarcos.label7.grid(row=0, column=7, padx=1, pady=7)
        frameBarcos.label8 = customtkinter.CTkLabel(frameBarcos, text="8", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameBarcos.label8.grid(row=0, column=8, padx=1, pady=7)
        frameBarcos.label9 = customtkinter.CTkLabel(frameBarcos, text="9", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameBarcos.label9.grid(row=0, column=9, padx=1, pady=7)
        frameBarcos.label10 = customtkinter.CTkLabel(frameBarcos, text="10", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameBarcos.label10.grid(row=0, column=10, padx=1, pady=7)
        frameBarcos.indice2 = customtkinter.CTkLabel(frameBarcos,width=10,height=2,text="")
        frameBarcos.indice2.grid(row=0, column=11, padx=1, pady=2)

        #Botones del panel A barcos
        frameBarcos.A1 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.A1,1,1))
        frameBarcos.A1.grid(row=1, column=1)
        frameBarcos.A2 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.A2,1,2))
        frameBarcos.A2.grid(row=1, column=2)
        frameBarcos.A3 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.A3,1,3))
        frameBarcos.A3.grid(row=1, column=3)
        frameBarcos.A4 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.A4,1,4))
        frameBarcos.A4.grid(row=1, column=4)
        frameBarcos.A5 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.A5,1,5))
        frameBarcos.A5.grid(row=1, column=5)
        frameBarcos.A6 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.A6,1,6))
        frameBarcos.A6.grid(row=1, column=6)
        frameBarcos.A7 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.A7,1,7))
        frameBarcos.A7.grid(row=1, column=7)
        frameBarcos.A8 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.A8,1,8))
        frameBarcos.A8.grid(row=1, column=8)
        frameBarcos.A9 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.A9,1,9))
        frameBarcos.A9.grid(row=1, column=9)
        frameBarcos.A10 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.A10,1,10))
        frameBarcos.A10.grid(row=1, column=10)


        #Botones del panel B barcos
        frameBarcos.B1 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.B1,2,1))
        frameBarcos.B1.grid(row=2, column=1)
        frameBarcos.B2 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.B2,2,2))
        frameBarcos.B2.grid(row=2, column=2)
        frameBarcos.B3 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.B3,2,3))
        frameBarcos.B3.grid(row=2, column=3)
        frameBarcos.B4 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.B4,2,4))
        frameBarcos.B4.grid(row=2, column=4)
        frameBarcos.B5 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.B5,2,5))
        frameBarcos.B5.grid(row=2, column=5)
        frameBarcos.B6 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.B6,2,6))
        frameBarcos.B6.grid(row=2, column=6)
        frameBarcos.B7 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.B7,2,7))
        frameBarcos.B7.grid(row=2, column=7)
        frameBarcos.B8 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.B8,2,8))
        frameBarcos.B8.grid(row=2, column=8)
        frameBarcos.B9 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.B9,2,9))
        frameBarcos.B9.grid(row=2, column=9)
        frameBarcos.B10 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.B10,2,10))
        frameBarcos.B10.grid(row=2, column=10)

        #Botones del panel C barcos
        frameBarcos.C1 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.C1,3,1))
        frameBarcos.C1.grid(row=3, column=1)
        frameBarcos.C2 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.C2,3,2))
        frameBarcos.C2.grid(row=3, column=2)
        frameBarcos.C3 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.C3,3,3))
        frameBarcos.C3.grid(row=3, column=3)
        frameBarcos.C4 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.C4,3,4))
        frameBarcos.C4.grid(row=3, column=4)
        frameBarcos.C5 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.C5,3,5))
        frameBarcos.C5.grid(row=3, column=5)
        frameBarcos.C6 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.C6,3,6))
        frameBarcos.C6.grid(row=3, column=6)
        frameBarcos.C7 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.C7,3,7))
        frameBarcos.C7.grid(row=3, column=7)
        frameBarcos.C8 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.C8,3,8))
        frameBarcos.C8.grid(row=3, column=8)
        frameBarcos.C9 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.C9,3,9))
        frameBarcos.C9.grid(row=3, column=9)
        frameBarcos.C10 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.C10,3,10))
        frameBarcos.C10.grid(row=3, column=10)

        #Botones del panel D barcos
        frameBarcos.D1 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.D1,4,1))
        frameBarcos.D1.grid(row=4, column=1)
        frameBarcos.D2 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.D2,4,2))
        frameBarcos.D2.grid(row=4, column=2)
        frameBarcos.D3 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.D3,4,3))
        frameBarcos.D3.grid(row=4, column=3)
        frameBarcos.D4 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.D4,4,4))
        frameBarcos.D4.grid(row=4, column=4)
        frameBarcos.D5 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.D5,4,5))
        frameBarcos.D5.grid(row=4, column=5)
        frameBarcos.D6 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.D6,4,6))
        frameBarcos.D6.grid(row=4, column=6)
        frameBarcos.D7 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.D7,4,7))
        frameBarcos.D7.grid(row=4, column=7)
        frameBarcos.D8 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.D8,4,8))
        frameBarcos.D8.grid(row=4, column=8)
        frameBarcos.D9 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.D9,4,9))
        frameBarcos.D9.grid(row=4, column=9)
        frameBarcos.D10 = customtkinter.CTkButton(frameBarcos,width=40,height=40,text=" ",command=lambda:enviarBarcos(frameBarcos.D10,4,10))
        frameBarcos.D10.grid(row=4, column=10)
#----------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------------------
        #Frame misiles
        frameMisiles = customtkinter.CTkFrame(master=root,
                               width=200,
                               height=200,
                               corner_radius=0)
        frameMisiles.place(x=25, y=349)
        
        imagenIcon = customtkinter.CTkImage(Image.open("target.png"),size=(25, 25))


        #filas labels barcos 
        frameMisiles.indice = customtkinter.CTkLabel(frameMisiles, text=" ", width=20,height=40,font=("Roboto",15))
        frameMisiles.indice.grid(row=0, column=0, padx=3, pady=7)
        frameMisiles.labelA = customtkinter.CTkLabel(frameMisiles, text="A", width=40,height=40,font=("Roboto",15),fg_color=("white", "#E78D1E"))
        frameMisiles.labelA.grid(row=1, column=0, padx=7, pady=1)
        frameMisiles.labelB = customtkinter.CTkLabel(frameMisiles,width=40,height=40,text="B",font=("Roboto",15),fg_color=("white", "#E78D1E"))
        frameMisiles.labelB.grid(row=2, column=0, padx=7, pady=1)
        frameMisiles.labelC = customtkinter.CTkLabel(frameMisiles,width=40,height=40,text="C",font=("Roboto",15),fg_color=("white", "#E78D1E"))
        frameMisiles.labelC.grid(row=3, column=0, padx=7, pady=1)
        frameMisiles.labelD = customtkinter.CTkLabel(frameMisiles,width=40,height=40,text="D",font=("Roboto",15),fg_color=("white", "#E78D1E"))
        frameMisiles.labelD.grid(row=4, column=0, padx=7, pady=1)
        frameMisiles.indice1 = customtkinter.CTkLabel(frameMisiles,width=40,height=5,text=" ",font=("Roboto",15))
        frameMisiles.indice1.grid(row=5, column=0, padx=7, pady=1)

        #filas columnas barcos
        frameMisiles.label1 = customtkinter.CTkLabel(frameMisiles, text="1", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameMisiles.label1.grid(row=0, column=1, padx=1, pady=7)
        frameMisiles.label2 = customtkinter.CTkLabel(frameMisiles, text="2", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameMisiles.label2.grid(row=0, column=2, padx=1, pady=7)
        frameMisiles.label3 = customtkinter.CTkLabel(frameMisiles, text="3", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameMisiles.label3.grid(row=0, column=3, padx=1, pady=7)
        frameMisiles.label4 = customtkinter.CTkLabel(frameMisiles, text="4", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameMisiles.label4.grid(row=0, column=4, padx=1, pady=7)
        frameMisiles.label5 = customtkinter.CTkLabel(frameMisiles, text="5", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameMisiles.label5.grid(row=0, column=5, padx=1, pady=7)
        frameMisiles.label6 = customtkinter.CTkLabel(frameMisiles, text="6", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameMisiles.label6.grid(row=0, column=6, padx=1, pady=7)
        frameMisiles.label7 = customtkinter.CTkLabel(frameMisiles, text="7", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameMisiles.label7.grid(row=0, column=7, padx=1, pady=7)
        frameMisiles.label8 = customtkinter.CTkLabel(frameMisiles, text="8", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameMisiles.label8.grid(row=0, column=8, padx=1, pady=7)
        frameMisiles.label9 = customtkinter.CTkLabel(frameMisiles, text="9", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameMisiles.label9.grid(row=0, column=9, padx=1, pady=7)
        frameMisiles.label9 = customtkinter.CTkLabel(frameMisiles, text="10", width=40,height=40,font=("Roboto",15),fg_color=("black", "#45769e"))
        frameMisiles.label9.grid(row=0, column=10, padx=1, pady=7)
        frameMisiles.indice2 = customtkinter.CTkLabel(frameMisiles,width=10,height=2,text=" ")
        frameMisiles.indice2.grid(row=0, column=11, padx=1, pady=2)

        #Botones del panel A barcos
        frameMisiles.A1 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.A1,1,1))
        frameMisiles.A1.grid(row=1, column=1)
        frameMisiles.A2 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.A2,1,2))
        frameMisiles.A2.grid(row=1, column=2)
        frameMisiles.A3 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.A3,1,3))
        frameMisiles.A3.grid(row=1, column=3)
        frameMisiles.A4 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.A4,1,4))
        frameMisiles.A4.grid(row=1, column=4)
        frameMisiles.A5 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.A5,1,5))
        frameMisiles.A5.grid(row=1, column=5)
        frameMisiles.A6 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.A6,1,6))
        frameMisiles.A6.grid(row=1, column=6)
        frameMisiles.A7 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.A7,1,7))
        frameMisiles.A7.grid(row=1, column=7)
        frameMisiles.A8 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.A8,1,8))
        frameMisiles.A8.grid(row=1, column=8)
        frameMisiles.A9 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.A9,1,9))
        frameMisiles.A9.grid(row=1, column=9)
        frameMisiles.A10 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.A10,1,10))
        frameMisiles.A10.grid(row=1, column=10)

        #Botones del panel B barcos
        frameMisiles.B1 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.B1,2,1))
        frameMisiles.B1.grid(row=2, column=1)
        frameMisiles.B2 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.B2,2,2))
        frameMisiles.B2.grid(row=2, column=2)
        frameMisiles.B3 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.B3,2,3))
        frameMisiles.B3.grid(row=2, column=3)
        frameMisiles.B4 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.B4,2,4))
        frameMisiles.B4.grid(row=2, column=4)
        frameMisiles.B5 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.B5,2,5))
        frameMisiles.B5.grid(row=2, column=5)
        frameMisiles.B6 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.B6,2,6))
        frameMisiles.B6.grid(row=2, column=6)
        frameMisiles.B7 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.B7,2,7))
        frameMisiles.B7.grid(row=2, column=7)
        frameMisiles.B8 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.B8,2,8))
        frameMisiles.B8.grid(row=2, column=8)
        frameMisiles.B9 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.B9,2,9))
        frameMisiles.B9.grid(row=2, column=9)
        frameMisiles.B10 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.B10,2,10))
        frameMisiles.B10.grid(row=2, column=10)

        #Botones del panel C barcos
        frameMisiles.C1 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.C1,3,1))
        frameMisiles.C1.grid(row=3, column=1)
        frameMisiles.C2 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.C2,3,2))
        frameMisiles.C2.grid(row=3, column=2)
        frameMisiles.C3 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.C3,3,3))
        frameMisiles.C3.grid(row=3, column=3)
        frameMisiles.C4 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.C4,3,4))
        frameMisiles.C4.grid(row=3, column=4)
        frameMisiles.C5 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.C5,3,5))
        frameMisiles.C5.grid(row=3, column=5)
        frameMisiles.C6 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.C6,3,6))
        frameMisiles.C6.grid(row=3, column=6)
        frameMisiles.C7 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.C7,3,7))
        frameMisiles.C7.grid(row=3, column=7)
        frameMisiles.C8 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.C8,3,8))
        frameMisiles.C8.grid(row=3, column=8)
        frameMisiles.C9 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.C9,3,9))
        frameMisiles.C9.grid(row=3, column=9)
        frameMisiles.C10 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.C10,3,10))
        frameMisiles.C10.grid(row=3, column=10)

        #Botones del panel D barcos
        frameMisiles.D1 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.D1,4,1))
        frameMisiles.D1.grid(row=4, column=1)
        frameMisiles.D2 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.D2,4,2))
        frameMisiles.D2.grid(row=4, column=2)
        frameMisiles.D3 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.D3,4,3))
        frameMisiles.D3.grid(row=4, column=3)
        frameMisiles.D4 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.D4,4,4))
        frameMisiles.D4.grid(row=4, column=4)
        frameMisiles.D5 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.D5,4,5))
        frameMisiles.D5.grid(row=4, column=5)
        frameMisiles.D6 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.D6,4,6))
        frameMisiles.D6.grid(row=4, column=6)
        frameMisiles.D7 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.D7,4,7))
        frameMisiles.D7.grid(row=4, column=7)
        frameMisiles.D8 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.D8,4,8))
        frameMisiles.D8.grid(row=4, column=8)
        frameMisiles.D9 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.D9,4,9))
        frameMisiles.D9.grid(row=4, column=9)
        frameMisiles.D10 = customtkinter.CTkButton(frameMisiles,width=40,height=40,text="",command=lambda:enviarMisiles(frameMisiles.D10,4,10))
        frameMisiles.D10.grid(row=4, column=10)

        botonSalir = customtkinter.CTkButton(root,width=150,height=40,text="Salir",font=("Roboto",20),command=eliminar,fg_color='#F20530',text_color='white',
                                            hover_color='#F299AB')
        botonSalir.place(x=700, y=520)






root=customtkinter.CTk()
MainFrame = juego(root)
root.mainloop()


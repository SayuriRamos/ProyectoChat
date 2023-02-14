import socket
import threading
from tkinter import *

PORT = 5001
SERVER = "192.168.1.133"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

# Se crea un cliente y se conecta al servidor
client = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
client.connect(ADDRESS)


class chat:
    # constructor
    def __init__(self):

        self.Window = Tk()

        # Se esconde el chat
        self.Window.withdraw()

        # pantalla de iniciar sesión
        self.iniciarSesion = Toplevel()
        self.iniciarSesion.title("Ingreso Nombre")
        self.iniciarSesion.configure(width=400,
                                     height=400,
                                     background="#f8daff")

        # Label Bienvenido
        self.bienvenidoLabel = Label(self.iniciarSesion,
                                     text="Bienvenido!!",
                                     justify=CENTER,
                                     font="Verdana 17 bold",
                                     fg="#7f3490")
        self.bienvenidoLabel.place(relx=0.27,
                                   rely=0.07)

        # Label de "ingresa tu nombre"
        self.label = Label(self.iniciarSesion,
                           text="Ingresa tu nombre",
                           justify=CENTER,
                           font="Verdana 18 bold",
                           background="#7f3490",
                           fg="#ffffff")
        self.label.place(relx=0.18,
                         rely=0.30)

        # Entrada de Nombre
        self.nombreEntrada = Entry(self.iniciarSesion,
                                   font="Helvetica 15",
                                   justify=CENTER)
        self.nombreEntrada.place(relwidth=0.4,
                                 relheight=0.12,
                                 relx=0.30,
                                 rely=0.44)

        # Diseño de botón para iniciar chat
        self.iniciarChatButton = Button(self.iniciarSesion,
                                        text="Iniciar Chat",
                                        font="Verdana 14 bold",
                                        # cuando seleccione "iniciar chat" se va a llamar a la función "iniciarchar" y
                                        # se obtiene el nombre que escribió el cliente
                                        command=lambda: self.iniciarChat(self.nombreEntrada.get()))
        self.iniciarChatButton.place(relx=0.32,
                                     rely=0.66)
        self.Window.mainloop()

    # Funcion para iniciar el chat y se crea un thread para recibir los mensajes
    def iniciarChat(self, name):
        self.iniciarSesion.destroy()
        self.chatPrincipal(name)

        # thread que recibe mensajes
        recibirThread = threading.Thread(target=self.recibirMensajes)
        recibirThread.start()

    # Diseño del chat
    def chatPrincipal(self, name):

        self.name = name

        # mostrar pantalla de chat
        self.Window.deiconify()

        self.Window.title("Chat")
        self.Window.configure(width=470,
                              height=550,
                              bg="#17202A")

        # Label del nombre del cliente
        self.nombreCliente = Label(self.Window,
                                   bg="#7f3490",
                                   fg="#ffffff",
                                   text=self.name,
                                   font="Verdana 13 bold",
                                   pady=4)
        self.nombreCliente.place(relwidth=1)

        # diseño de mensajes
        self.mensajes = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#f8daff",
                             fg="#7f3490",
                             font="Verdana 14",
                             padx=4,
                             pady=4)
        self.mensajes.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)

        # label de la parte de abajo, donde esta la entrada y el botón
        self.labelAbajo = Label(self.Window,
                                bg="#7f3490",
                                height=80)
        self.labelAbajo.place(relwidth=1,
                              rely=0.825)

        # Entrada del mensaje
        self.entryMsg = Entry(self.labelAbajo,
                              bg="#f8daff",
                              fg="#17202A",
                              font="Verdana 13")
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)

        self.entryMsg.focus()

        # Diseño botón mandar menajes
        self.botonMandarMensages = Button(self.labelAbajo,
                                          text="Enviar",
                                          font="Verdana 10 bold",
                                          width=10,
                                          bg="#f8daff",
                                          command=lambda: self.sendButton(self.entryMsg.get()))
        self.botonMandarMensages.place(relx=0.77,
                                       rely=0.008,
                                       relheight=0.06,
                                       relwidth=0.22)

        self.mensajes.config(cursor="arrow")

        # scroll bar
        scrollbar = Scrollbar(self.mensajes)
        scrollbar.place(relheight=1,
                        relx=0.974)
        scrollbar.config(command=self.mensajes.yview)
        self.mensajes.config(state=DISABLED)

    # función que se llama cuando se selecciona botón "enviar", se
    #  se manda llamar a la función "mandarMensaje"
    def sendButton(self, mensage):
        self.mensajes.config(state=DISABLED)
        self.mensaje = mensage
        if mensage == "":  # cuando se hace clic en "enviar" cuando no se ha escrito nada
            print("no se mandó nada")
        else:
            self.entryMsg.delete(0, END)  # limpiar caja de entrada

            # crear thread para enviar mensaje
            enviarThread = threading.Thread(target=self.mandarMensaje)
            enviarThread.start()

    # recibe los mensajes y los muestra en la interfaz
    def recibirMensajes(self):
        while True:
            try:
                mensaje = client.recv(1024).decode(FORMAT)  # recibir mensaje del servidor

                # Se le manda el nombre del cliente al servidor si se recibe "nombre"

                if mensaje == 'nombre':
                    client.send(self.name.encode(FORMAT))
                elif mensaje.find("lista,") == 0:
                    print(mensaje)
                    self.mensajes.config(state=NORMAL)
                    self.mensajes.config(state=NORMAL)
                    self.mensajes.insert(END,
                                         mensaje + "\n\n")

                    self.mensajes.config(state=DISABLED)
                    self.mensajes.see(END)
                elif mensaje == 'cleanL':
                    # limpiar la caja de texto
                    self.mensajes.config(state=NORMAL)
                    self.mensajes.config(state=NORMAL)
                    self.mensajes.delete('1.0', END)
                    self.mensajes.config(state=DISABLED)
                    self.mensajes.see(END)
                else:
                    if mensaje.find(":") == -1:
                        print(" ")
                    else:
                        print(mensaje)

                    # Si el servidor no quiere el nombre, se imprime el mensaje
                    self.mensajes.config(state=NORMAL)
                    self.mensajes.insert(END,
                                         mensaje + "\n\n")

                    self.mensajes.config(state=DISABLED)
                    self.mensajes.see(END)
            except:
                print("Error :c")
                client.close()
                break

    # mandar mensajes al servidor
    def mandarMensaje(self):
        self.mensajes.config(state=DISABLED)
        while True:
            message = (f"{self.mensaje}")
            client.send(message.encode(FORMAT))
            break


g = chat()

import socket
import random
import threading
import time

PORT = 5001
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

# Crear listas que almacenan los nombres del cliente
clientes, names = [], []
inicio = []
numeros = []

# Crear socket para servidor
server = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
server.bind(ADDRESS)


# función para empezar la conexión
def comenzarchat():
    print("Servidor: " + SERVER)

    # Escucha por conexiones
    server.listen()

    while True:
        # Acepta la conexión y pide el nombre del cliente
        conn, addr = server.accept()
        conn.send("nombre".encode(FORMAT))

        # 1024 maxima cantidad de datos que se pueden recibir (bytes)
        # Aquí se recibe el nombre del cliente
        nombre = conn.recv(1024).decode(FORMAT)

        # Se añade el nombre y la conexión del cliente a las listas correspondientes.
        names.append(nombre)
        clientes.append(conn)

        if len(clientes) <= 1:
            print(f"Se conectó :{nombre}")
            broadcastMensage(f"---{nombre} se ha conectado---".encode(FORMAT))
            thread = threading.Thread(target=handle,
                                      args=(conn, addr))
            thread.start()

        elif len(clientes) == 4:
            print("Ya se tienen los 4 jugadores")
            break

# handle mensajes que llegan
def handle(conn, addr):
    print(f"Nueva conexión: {addr}")
    estaConectado = True

    while estaConectado:
        # Se reciben mensajes
        message = conn.recv(1024)
        print(message.decode(FORMAT))

        if (message.decode(FORMAT)).find("100") == 0:
            x = message.decode(FORMAT).split(" ")

            broadcastMensage(("HA GANADO " + str(x[1])).encode(FORMAT))
        else:
            if message.decode(FORMAT) == "ya":
                inicio.append(message)
                print("si")

                if len(inicio) == 1:
                    contador = 10
                    broadcastMensage("cleanL".encode(FORMAT))
                    while True:
                        broadcastMensage(("Se inicia el juego en: " + str(contador)).encode(FORMAT))
                        time.sleep(1)
                        contador = contador - 1
                        broadcastMensage("cleanL".encode(FORMAT))
                        if contador == 0:
                            break
                    listanum = "lista"
                    for x in range(25): #Agregar num del juego en el array
                        num = random.randint(11, 19)
                        numeros.append(num)
                        listanum = listanum + ", " + str(num)
                    print(numeros)
                    broadcastMensage(("Se inicia el juego: \n" + listanum).encode(FORMAT))

        # Se envían mensajes
        if len(inicio) == len(clientes):
            print("s einicia")



    # cerrar conexión
    conn.close()


# mandar mensaje a los clientes, se envía a todos
def broadcastMensage(mensaje):
    for client in clientes:
        client.send(mensaje)

# llamar método para empezar la comunicación
comenzarchat()
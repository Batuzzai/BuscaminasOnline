import socket
import sys
import threading
import Juego
from Juego import main, Tablero
from _thread import *
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = ''
puerto = 2020

ipServer = socket.gethostbyname(server)

try:
    s.bind((ipServer, puerto))

except socket.error as e:
    print("Error al iniciar servidor, verifique Puerto")


s.listen(2)
print("Esperando a jugadores...")
                             


JugadorActual = 0
while True:
    (conexion, direccion) = s.accept()
    print("Cliente conectado!: ", direccion)
    JugadorActual = JugadorActual + 1
    ##start_new_thread(hilos, (conexion,JugadorActual))
    ##mensaje = ''

    while True:
        respuesta = conexion.recv(1024)
        print("Recibido por cliente: ",str(respuesta.decode('utf-8')))
        if not respuesta:
            break
        ##mensaje = mensaje + gstr(respuesta)
        conexion.send(str.encode("ABRIENDO BUSCAMINAS..."))
        conexion.sendall(pickle.dumps(main()))

    conexion.close()
    print('Cliente desconectado')

  

    

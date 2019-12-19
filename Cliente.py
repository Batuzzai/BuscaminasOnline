import socket
import Juego
from Juego import *
import pickle


host = '127.0.0.1'
puerto = 2020

##host = str(input("Ingrese IP del servidor: "))
##puerto = input("Ingrese puerto: ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((host,puerto))
    print("CONECTADO")
except:
    print("Error al conectar")

mensaje = "JUGANDO"
lose = "DERROTA"
win = "VICTORIA"

while True:

    s.send(str.encode(mensaje))
    
    comunica = s.recv(1024)
    print('Recibido por el servidor :',str(comunica.decode('utf-8')))
    datos = pickle.loads(s.recv(2048))
    if not datos:
         print("PERDISTE")
         ##s.send(str.encode(mensaje))
         s.close()
         break
    ##s.send(str.encode(mensaje2))
    s.close()




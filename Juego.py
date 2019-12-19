import sys
import pygame
import random
from pygame.locals import *
from ctypes import byref, c_int, pointer

#VARIABLES GLOBALES
ANCHO = 600
ALTO = 600
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0,255,0)
NEGRO = (0,0,0)
dimensiones_tablero = [ANCHO, ALTO]
ultimaPosicion = [-1, -1]
global finJuego
finJuego = False


class Player:
    def __init__(self, ID, color):
        self.ID = ID
        self.color = color
        posicion = ([0,0][0,0])
        ##self.cursor = pygame.mouse.get_pos()

    

class Text:
    def __init__(self, FontName = None, FontSize = 50):
        pygame.font.init()
        self.font = pygame.font.Font(FontName, FontSize)
        self.size = FontSize

    def render(self, surface, text, color, pos):
        text = str(text)
        x, y = pos
        for i in text.split("\r"):
            surface.blit(self.font.render(i, 1, color), (x, y))
            y += self.size

class Tablero:
    ancho = 0
    alto = 0
    borde = 0
    numero_cuadros = 0
    ancho_cuadro = 0
    alto_cuadro = 0
    tablero=[]
    text = Text()
    #finJuego = False

    def __init__(self, ancho, alto, borde, numero_cuadros):
        self.ancho = ancho
        self.alto = alto
        self.borde = borde
        self.numero_cuadros = numero_cuadros
        self.ancho_cuadro = ancho/numero_cuadros
        self.alto_cuadro = alto/numero_cuadros
        #self.finJuego = False

        for i in range(numero_cuadros):
            self.tablero.append(['X']*numero_cuadros)

        for i in range(10):
            f = random.randrange(numero_cuadros-1)
            c = random.randrange(numero_cuadros-1)
            while(self.tablero[f][c] == 'B'):
                f = random.randrange(numero_cuadros-1)
                c = random.randrange(numero_cuadros-1)

            self.tablero[f][c] = 'B'

    def dibujaTablero(self, ventana, posicion):
        aumento_ancho=0
        aumento_alto=0

        pygame.draw.rect(ventana, BLANCO, pygame.Rect(0, 0, self.borde, self.alto), 0)
        pygame.draw.rect(ventana, BLANCO, pygame.Rect(0, 0, self.ancho, self.borde), 0)
        pygame.draw.rect(ventana, BLANCO, pygame.Rect(self.ancho-self.borde, 0, self.borde, self.alto), 0)
        pygame.draw.rect(ventana, BLANCO, pygame.Rect(0, self.alto-self.borde, self.ancho, self.borde), 0)

        for i in range(self.numero_cuadros):
            aumento_ancho += self.ancho_cuadro
            aumento_alto += self.alto_cuadro
            pygame.draw.rect(ventana, BLANCO, pygame.Rect(aumento_ancho, 0, self.borde, self.alto), 0)
            pygame.draw.rect(ventana, BLANCO, pygame.Rect(0, aumento_alto, self.ancho, self.borde), 0)

        #Segundo pinto el color interno de cada cuadro del tablero
        aumento_ancho=0
        aumento_alto=0

        for i in range(self.numero_cuadros):
            for j in range(self.numero_cuadros):
                aumento_ancho = j*self.ancho_cuadro
                aumento_alto = i*self.alto_cuadro

                #El primer if pinta el cuadro centrar a excepción de los filos
                #El segundo if pinta filos de arriba y de la izquierda
                #El tercer if pinta filos de la derecha y de abajo
                if i!=0 and j!=0 and i!=self.numero_cuadros-1 and j!=self.numero_cuadros-1:
                    if(posicion[0]>aumento_ancho and posicion[0]<aumento_ancho+self.ancho_cuadro and posicion[1]>aumento_alto and posicion[1]<aumento_alto+self.alto_cuadro):
                        ultimaPosicion[0] = i
                        ultimaPosicion[1] = j

                    self.compruebaCasilla(ultimaPosicion[0], ultimaPosicion[1])

                    if self.tablero[i][j]!='X' and self.tablero[i][j]!='B':
                        pygame.draw.rect(ventana, AZUL, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                        if self.tablero[i][j]!='0':
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                    elif self.tablero[i][j]=='B' and i==ultimaPosicion[0] and j==ultimaPosicion[1]:
                        pygame.draw.rect(ventana, VERDE, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                        self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                    else:
                        pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                elif i==0 or j==0:
                    if i==0 and j==self.numero_cuadros-1:
                        if(posicion[0]>aumento_ancho and posicion[0]<aumento_ancho+self.ancho_cuadro and posicion[1]>aumento_alto and posicion[1]<aumento_alto+self.alto_cuadro):
                            ultimaPosicion[0] = i
                            ultimaPosicion[1] = j

                        self.compruebaCasilla(ultimaPosicion[0], ultimaPosicion[1])

                        if self.tablero[i][j]!='X' and self.tablero[i][j]!='B':
                            pygame.draw.rect(ventana, AZUL, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-2*self.borde, self.alto_cuadro-self.borde), 0)
                            if self.tablero[i][j]!='0':
                                self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        elif self.tablero[i][j]=='B' and i==ultimaPosicion[0] and j==ultimaPosicion[1]:
                            pygame.draw.rect(ventana, VERDE, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        else:
                            pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-2*self.borde, self.alto_cuadro-self.borde), 0)
                    elif j==0 and i==self.numero_cuadros-1:
                        if(posicion[0]>aumento_ancho and posicion[0]<aumento_ancho+self.ancho_cuadro and posicion[1]>aumento_alto and posicion[1]<aumento_alto+self.alto_cuadro):
                            ultimaPosicion[0] = i
                            ultimaPosicion[1] = j

                        self.compruebaCasilla(ultimaPosicion[0], ultimaPosicion[1])

                        if self.tablero[i][j]!='X' and self.tablero[i][j]!='B':
                            pygame.draw.rect(ventana, AZUL, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-2*self.borde), 0)
                            if self.tablero[i][j]!='0':
                                self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        elif self.tablero[i][j]=='B' and i==ultimaPosicion[0] and j==ultimaPosicion[1]:
                            pygame.draw.rect(ventana, VERDE, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        else:
                            pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-2*self.borde), 0)
                    else:
                        if(posicion[0]>aumento_ancho and posicion[0]<aumento_ancho+self.ancho_cuadro and posicion[1]>aumento_alto and posicion[1]<aumento_alto+self.alto_cuadro):
                            ultimaPosicion[0] = i
                            ultimaPosicion[1] = j

                        self.compruebaCasilla(ultimaPosicion[0], ultimaPosicion[1])

                        if self.tablero[i][j]!='X' and self.tablero[i][j]!='B':
                            pygame.draw.rect(ventana, AZUL, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            if self.tablero[i][j]!='0':
                                self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        elif self.tablero[i][j]=='B' and i==ultimaPosicion[0] and j==ultimaPosicion[1]:
                            pygame.draw.rect(ventana, VERDE, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        else:
                            pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                elif i==self.numero_cuadros-1 or j==self.numero_cuadros-1:
                    if i==self.numero_cuadros-1 and j==self.numero_cuadros-1:
                        if(posicion[0]>aumento_ancho and posicion[0]<aumento_ancho+self.ancho_cuadro and posicion[1]>aumento_alto and posicion[1]<aumento_alto+self.alto_cuadro):
                            ultimaPosicion[0] = i
                            ultimaPosicion[1] = j

                        self.compruebaCasilla(ultimaPosicion[0], ultimaPosicion[1])

                        if self.tablero[i][j]!='X' and self.tablero[i][j]!='B':
                            pygame.draw.rect(ventana, AZUL, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-2*self.borde, self.alto_cuadro-2*self.borde), 0)
                            if self.tablero[i][j]!='0':
                                self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        elif self.tablero[i][j]=='B' and i==ultimaPosicion[0] and j==ultimaPosicion[1]:
                            pygame.draw.rect(ventana, VERDE, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        else:
                            pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-2*self.borde, self.alto_cuadro-2*self.borde), 0)
                    elif i==self.numero_cuadros-1:
                        if(posicion[0]>aumento_ancho and posicion[0]<aumento_ancho+self.ancho_cuadro and posicion[1]>aumento_alto and posicion[1]<aumento_alto+self.alto_cuadro):
                            ultimaPosicion[0] = i
                            ultimaPosicion[1] = j

                        self.compruebaCasilla(ultimaPosicion[0], ultimaPosicion[1])

                        if self.tablero[i][j]!='X' and self.tablero[i][j]!='B':
                            pygame.draw.rect(ventana, AZUL, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-2*self.borde), 0)
                            if self.tablero[i][j]!='0':
                                self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        elif self.tablero[i][j]=='B' and i==ultimaPosicion[0] and j==ultimaPosicion[1]:
                            pygame.draw.rect(ventana, VERDE, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        else:
                            pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-2*self.borde), 0)
                    elif j==self.numero_cuadros-1:
                        if(posicion[0]>aumento_ancho and posicion[0]<aumento_ancho+self.ancho_cuadro and posicion[1]>aumento_alto and posicion[1]<aumento_alto+self.alto_cuadro):
                            ultimaPosicion[0] = i
                            ultimaPosicion[1] = j

                        self.compruebaCasilla(ultimaPosicion[0], ultimaPosicion[1])

                        if self.tablero[i][j]!='X' and self.tablero[i][j]!='B':
                            pygame.draw.rect(ventana, AZUL, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-2*self.borde, self.alto_cuadro-self.borde), 0)
                            if self.tablero[i][j]!='0':
                                self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.06))
                        elif self.tablero[i][j]=='B' and i==ultimaPosicion[0] and j==ultimaPosicion[1]:
                            pygame.draw.rect(ventana, VERDE, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        else:
                            pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-2*self.borde, self.alto_cuadro-self.borde), 0)

    def imprimeTablero(self):
        for i in self.tablero:
            print(i)

    def compruebaCasilla(self, f, c):
        contador = 0
        if f>=0 and c>=0 and f<self.numero_cuadros and c<self.numero_cuadros and self.tablero[f][c]!='B' and self.tablero[f][c]=='X':
            compruebaBomba = False

            for i in [f-1, f, f+1]:
                for j in [c-1, c, c+1]:
                    if i>=0 and j>=0 and i<self.numero_cuadros and j<self.numero_cuadros and self.tablero[i][j]=='B' and compruebaBomba==False:
                        compruebaBomba=True
                        contador = contador + 1
                    elif i>=0 and j>=0 and i<self.numero_cuadros and j<self.numero_cuadros and self.tablero[i][j]=='B':
                        contador = contador + 1


            self.tablero[f][c] = chr(contador+48)

          ##  if compruebaBomba==False:
          ##      for i in [f-1, f, f+1]:
          ##          for j in [c-1, c, c+1]:
          ##              self.compruebaCasilla(i,j)
        elif f>=0 and c>=0 and f<self.numero_cuadros and c<self.numero_cuadros and self.tablero[f][c]=='B':
            global finJuego
            finJuego = True

def main():
    pygame.init()
    ventana = pygame.display.set_mode(dimensiones_tablero)
    pygame.display.set_caption("Buscaminas")
    clock = pygame.time.Clock()

    pos = [-1,-1]
    #ancho, alto, borde, numero_cuadros
    tablero = Tablero(600, 600, 2, 8)
    #tablero.imprimeTablero()

    while not finJuego:
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                print("FIN: \n")
                #tablero.imprimeTablero()
                sys.exit(0)

        tablero.dibujaTablero(ventana, pos)

        botones = pygame.mouse.get_pressed()
        if botones[0]:
            pos = pygame.mouse.get_pos()

        pygame.display.flip()
        clock.tick(60)

    if finJuego == True:
        pygame.quit()
    
    return 0

if __name__ == "__main__":
    main()

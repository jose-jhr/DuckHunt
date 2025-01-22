import os.path
import random

import numpy as np
import pygame

class AvesSprites(pygame.sprite.Sprite):

    def __init__(self,screenWidth,screenHeight):
        super(AvesSprites, self).__init__()
        #vector aves in folder .png
        self.aves = [pygame.image.load("../img/ave/ave1.png"),
                     pygame.image.load("../img/ave/ave2.png"),
                     pygame.image.load("../img/ave/ave3.png"),
                     pygame.image.load("../img/ave/ave4.png"),
                     pygame.image.load("../img/ave/ave5.png"),
                     pygame.image.load("../img/ave/ave6.png"),
                     pygame.image.load("../img/ave/ave7.png"),
                     pygame.image.load("../img/ave/ave8.png"),
                     pygame.image.load("../img/ave/ave9.png"),
                     pygame.image.load("../img/ave/ave10.png")]

        #selecciòn de sprite
        self.index = 0
        #cantidad de movimiento de sprite
        self.movAve = 5
        #imagen de inicio
        self.image = self.aves[self.index]
        #rectangle object
        self.rect = pygame.Rect(0, 0, 50, 50)
        #time init
        self.last_update = pygame.time.get_ticks()
        #is end position
        self.isEndPosition = False
        #generar numero aleatorio con ancho y alto
        self.randomX = random.randint(0, screenWidth - self.rect.width)
        self.randomY = random.randint(0, screenHeight - screenHeight * 0.35)
        #guardamos los valores de la pantalla
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        #distancia de movimiento
        self.distanciax = 0
        self.distanciay = 0


    def movX(self):
        self.index += 1
        if self.index == 2:
            self.index = 0

    def movY(self):
        self.index += 1
        if self.index == 7:
            self.index = 5


    #actuaización de sprites en pantalla
    def update(self):
        #current time
        now = pygame.time.get_ticks()
        #if current time is greater than 100ms
        if now - self.last_update > 33:

            #en caso de que la posicion este mas o menos a 10 de distancia entonces recargamos los valores
            #aleatorios
            self.distanceX = abs(self.rect.x - self.randomX)
            self.distanceY = abs(self.rect.y - self.randomY)
            if self.distanceX < 40 and self.distanceY < 40:
                #hacemos un bucle para que no se repita la misma posicion y ademas
                #resolvemos el problema de que la nueva posicion este dentro de los 40 pixeles
                while self.distanceX < 40 and self.distanceY < 40:
                    self.randomX = random.randint(0, self.screenWidth - self.rect.width)
                    self.randomY = random.randint(0, self.screenHeight - self.rect.height)
                    self.distanceX = abs(self.rect.x - self.randomX)
                    self.distanceY = abs(self.rect.y - self.randomY)
                    self.isEndPosition = True
                    self.index = 0
                    self.image = self.aves[self.index]
                    print("nueva posicion aleatoria X "+str(self.randomX)+" Y "+str(self.randomY))
                    #posicion actual
                    print("posicion actual X "+str(self.rect.x)+" Y "+str(self.rect.y))

            #actualizamos el tiempo de la ultima actualizacion
            self.last_update = now
            if self.rect.x < self.randomX:
                self.rect.x += self.movAve
                self.image = self.aves[self.index]
                # movemos el sprite
                self.movX()
            else:
                if self.rect.x > self.randomX:
                    self.rect.x -= self.movAve
                    self.image = self.aves[self.index]
                    self.image = pygame.transform.flip(self.image, True, False)
                    #self.image = pygame.transform.rotate(self.image, 180)
                    #movemos el sprite
                    self.movX()
                else:
                    if self.rect.y < self.randomY:
                        self.rect.y += self.movAve
                        self.image = self.aves[self.index]
                        # rotar imagen
                        self.image = pygame.transform.rotate(self.image, 180)
                        self.movY()
                    else:
                        if self.rect.y > self.randomY:
                            self.rect.y -= self.movAve
                            self.image = self.aves[self.index]
                            self.movY()
                        else:
                            self.randomX = random.randint(0, self.screenWidth - self.rect.width)
                            self.randomY = random.randint(0, self.screenHeight - self.rect.height)
                            self.isEndPosition = True
                            self.index = 0
                            self.image = self.aves[self.index]




            #if self.rect.y < self.randonY:
            #    self.rect.y += 1
            #else:
            #    if self.rect.y > self.randonY:
            #        self.rect.y -= 1




            #self.index += 1
            #if self.index == len(self.aves):
            #    self.index = 0
            #self.image = self.aves[self.index]

        #get position of the rectangle





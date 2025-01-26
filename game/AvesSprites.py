import os.path
import random
import threading
import time

import numpy as np
import pygame


class AvesSprites(pygame.sprite.Sprite):

    def __init__(self, screenWidth, screenHeight):
        super(AvesSprites, self).__init__()
        # vector aves in folder .png
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

        # ancho ave
        self.anchoAve = 80
        self.altoAve = 80

        # resize image
        self.aves = [pygame.transform.scale(ave, (self.anchoAve, self.altoAve)) for ave in self.aves]

        # selecciòn de sprite
        self.index = 0
        # cantidad de movimiento de sprite
        self.movAve = 5
        # imagen de inicio
        self.image = self.aves[self.index]
        # rectangle object
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        # time init
        self.last_update = pygame.time.get_ticks()
        # is end position
        self.isEndPosition = False
        # generar numero aleatorio con ancho y alto
        self.randomX = random.randint(0, (screenWidth - self.rect.width) // 5) * 5
        self.randomY = random.randint(0, (
                    screenHeight - screenHeight * 0.35) // 5) * 5  # el 0.35 es para que no se vea en la parte de abajo
        # guardamos los valores de la pantalla
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        # distancia de movimiento
        self.distanciax = 0
        self.distanciay = 0
        # se murio el sprite
        self.isDeadAve = False
        # animacion de 2 segundo de frame disparo
        self.isDeadAveAnimation = False
        #contador de animacion
        self.contadoAnimaionMuerte = 0

    def movX(self):
        self.index += 1
        if self.index == 2:
            self.index = 0

    def movY(self):
        self.index += 1
        if self.index == 8:
            self.index = 5

    def reiniciamosMovimiento(self):
        self.randomX = random.randint(0, (self.screenWidth - self.rect.width) // 5) * 5
        self.randomY = random.randint(0, (
                self.screenHeight - self.screenHeight * 0.35) // 5) * 5  # el 0.35 es para que no se vea en la parte de abajo

        self.isEndPosition = True
        self.index = 0
        self.image = self.aves[self.index]

    # actuaización de sprites en pantalla
    def update(self):
        # current time
        now = pygame.time.get_ticks()
        # if current time is greater than 100ms
        if now - self.last_update > 33 and self.isDeadAve == False:
            # actualizamos el tiempo de la ultima actualizacion
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
                    # self.image = pygame.transform.rotate(self.image, 180)
                    # movemos el sprite
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
                            self.reiniciamosMovimiento()
        else:
            if self.isDeadAveAnimation:
                self.index = 8
                self.image = self.aves[self.index]
                if self.contadoAnimaionMuerte < 10:
                    self.contadoAnimaionMuerte += 1
                else:
                    self.isDeadAveAnimation = False
                    self.contadoAnimaionMuerte = 0

            if self.isDeadAve and self.isDeadAveAnimation == False:
                self.index = 9
                if self.rect.y < self.screenHeight - self.screenHeight * 0.35:
                    self.rect.y += self.movAve
                    self.image = self.aves[self.index]
                else:
                    self.rect.y = 0
                    self.rect.x = 0
                    self.reiniciamosMovimiento()
                    self.isDeadAve = False

    def colision(self, x, y):
        if self.rect.collidepoint(x, y):
            self.isDeadAve = True
            self.isDeadAveAnimation = True
            self.image = self.aves[8]
            return True

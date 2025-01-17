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
        self.movAve = 10
        #imagen de inicio
        self.image = self.aves[self.index]
        #rectangle object
        self.rect = pygame.Rect(0, 0, 50, 50)
        #time init
        self.last_update = pygame.time.get_ticks()
        #is end position
        self.isEndPosition = False
        #generar numero aleatorio con ancho y alto
        self.randonX = random.randint(0,screenWidth)
        self.randonY = random.randint(0,screenHeight)






    def movX(self):
        self.index += 1
        if self.index == 2:
            self.index = 0

    def movY(self):
        self.index += 1
        if self.index == 7:
            self.index = 5

    def update(self):
        #current time
        now = pygame.time.get_ticks()
        #if current time is greater than 100ms
        if now - self.last_update > 10:
            #actualizamos el tiempo de la ultima actualizacion
            self.last_update = now

            if self.rect.x < self.randonX:
                self.rect.x += self.movAve
                self.image = self.aves[self.index]
                self.movX()
            else:
                if self.rect.x > self.randonX:
                    self.rect.x -= self.movAve
                    self.image = self.aves[self.index]
                    self.image = pygame.transform.rotate(self.image, 180)
                    self.movX()
                else:
                    if self.rect.y < self.randonY:
                        self.rect.y += self.movAve
                        self.image = self.aves[self.index]
                        # rotar imagen
                        self.image = pygame.transform.rotate(self.image, 180)
                        self.movY()
                    else:
                        if self.rect.y > self.randonY:
                            self.rect.y -= self.movAve
                            self.image = self.aves[self.index]

                            self.movY()




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





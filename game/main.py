#1 pygame
import pygame
import os
#2 camara con cv2
import cv2 as cv  # Import the OpenCV library
import time  # Import the time library
#3 mediapipe
import cv2 as cv
import time
import mediapipe as mp
import numpy as np

#iniciamos pygame (1)
pygame.init()

#5) import avesSprites class
from AvesSprites import AvesSprites


#camara --------------------------------------------------------
# Create a VideoCapture object called cap (1)
cap = cv.VideoCapture(0)

# Start the timer (1)
start_time = time.time()

# Initialize the frame counter (1)
frame_counter = 0


#ancho imagen
screenWidth = 800
#alto imagen
screenHeight = 600
#tamaño de pantalla max display(1)
screen = pygame.display.set_mode((screenWidth, screenHeight))

#titulo de la ventana (1)
pygame.display.set_caption("Disparos")

#get image from file (1)
background = pygame.image.load(os.path.join("../img", "fondo.png"))
#scale image to screen size (1)
background = pygame.transform.scale(background, (800, 600))


#MediaPipe (3) --------------------------------------------------------
handsMp = mp.solutions.hands
hands = handsMp.Hands()
mpDraw = mp.solutions.drawing_utils

#sound 4 --------------------------------------------------------
#get sound from file
soundGun = pygame.mixer.Sound(os.path.join("../sound", "gun.mp3"))
isDisparo = False

#(5) ave sprintes
aves = AvesSprites(screenWidth,screenHeight)
groupAves = pygame.sprite.Group(aves)


with handsMp.Hands(static_image_mode=False,
                   max_num_hands=1,
                   min_detection_confidence=0.5) as hands:

    #Ciclo de ejecución de programa
    while True:
        #Pygame --------------------------------------------------------
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        #movemos una mira segun sea el movimiento de la mano

        #camara read --------------------------------------------------------
        # Increment the frame counter
        frame_counter += 1

        # Read a frame from the webcam
        ret, frame = cap.read()

        # If the frame was not successfully captured, break out of the loop
        if ret is False:
            break

        # Calculate the FPS
        fps = frame_counter / (time.time() - start_time)

        # Display the FPS on the frame
        cv.putText(frame, f"FPS: {fps:.3f}", (30, 30), cv.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 255), 2, cv.LINE_AA)

        #MediaPipe --------------------------------------------------------
        # Convert the BGR image to RGB
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        #procesamos la imagen con mediapipe
        results = hands.process(rgb_frame)
        #frame size
        frame_height,frame_width,c = frame.shape
        # si obtenemos puntos de referencia multiples
        if results.multi_hand_landmarks is not None:
            # recorremos esos puntos multiples de referencia
            for hand_landmarks in results.multi_hand_landmarks:
                # dibujamos los puntos de referencia (imagen,puntos referencia de la mano,describe las conexiones
                # de los puntos de referencia,
                mpDraw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    handsMp.HAND_CONNECTIONS)
                # *************************************
                # aqui todas las funciones para el movimiento de la mira
                # *************************************
                # obtenemos del punto 8 de la mano la posición en x y y
                x = hand_landmarks.landmark[8].x * frame_width
                y = hand_landmarks.landmark[8].y * frame_height
                #obtenemos del punto 7 de la mano la posición en x y y
                x2 = hand_landmarks.landmark[7].x * frame_width
                y2 = hand_landmarks.landmark[7].y * frame_height
                #calculamos el angulo que se forma entre estos dos puntos
                #angle = np.arctan2(y2 - y, x2 - x)
                #convertimos el angulo a grados
                #angle = np.degrees(angle)
                #print(angle)
                #camara 640 480
                #draw rectangle in frame con 200 de separación todo centrado
                cv.rectangle(frame, (int(frame_width/2)-100, int(frame_height/2)-100),
                             (int(frame_width/2)+100, int(frame_height/2)+100), (0, 255, 0), 2)
                #invertimos el valor de x
                x = frame_width - x
                #normalizar el valor de x y y
                x = np.interp(x, (int(frame_width/2)-100, int(frame_width/2)+100), (0, 800))
                y = np.interp(y, (int(frame_height/2)-100, int(frame_height/2)+100), (0, 600))

                #4 angle disparo
                #get position point 4
                x1p = hand_landmarks.landmark[4].x * frame_width
                y1p = hand_landmarks.landmark[4].y * frame_height

                #get position point 2
                x2p = hand_landmarks.landmark[2].x * frame_width
                y2p = hand_landmarks.landmark[2].y * frame_height

                #calculate angle
                angle = np.arctan2(y2p - y1p, x2p - x1p)
                angle = np.degrees(angle)

                if angle < 0:
                    print("disparo")
                    if not isDisparo:
                        soundGun.play()
                        isDisparo = True #para que no se repita el sonido
                else:
                    print("no disparo")
                    isDisparo = False


                groupAves.update()
                groupAves.draw(screen)
                #dibujamos la mira en la pantalla
                pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), 10)



        # Display the frame on the screen
        cv.imshow("frame", cv.flip(frame, 1))

        # Check if the user has pressed the `q` key, if yes then close the program.
        key = cv.waitKey(1)
        if key == ord("q"):
         break


        #PyGame Actualizamos la pantalla ------------------------------------
        pygame.display.update()

#release camera
cap.release()

# Close all the frames
cv.destroyAllWindows()
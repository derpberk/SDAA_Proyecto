#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
from time import sleep   

GPIO.setmode(GPIO.BOARD)
GPIO.setup(21,GPIO.OUT)    #Ponemos el pin 21 como salida
motor1 = GPIO.PWM(21,50)        #Ponemos el pin 21 en modo PWM y enviamos 50 pulsos por segundo
motor1.start(7.5)               #Enviamos un pulso del 7.5% para centrar el servo

GPIO.setup(26,GPIO.OUT)    #Ponemos el pin 26 como salida
motor2 = GPIO.PWM(26,50)        #Ponemos el pin 26 en modo PWM y enviamos 50 pulsos por segundo
motor2.start(7.5)               #Enviamos un pulso del 7.5% para centrar el servo


def SetAngleAA(angle):
	duty = angle / 18 + 2.5  #angulo entre 18(180*) y sumamos el valor mín posible (datasheet)
	GPIO.output(21, True) #encendemos el pin
	motor1.ChangeDutyCycle(duty) #mandamos la señal con el duty determinado
	sleep(1) #esperamos a que funcione
	GPIO.output(21, False) #se acabó
	motor1.ChangeDutyCycle(0) #lo dejamos así, no se vaya a volver loco


def SetAngleLL(angle):
	duty = angle / 18 + 2.5  #angulo entre 18(180*) y sumamos el valor mín posible (datasheet)
	GPIO.output(26, True) #encendemos el pin
	motor2.ChangeDutyCycle(duty) #mandamos la señal con el duty determinado
	sleep(1) #esperamos a que funcione
	GPIO.output(26, False) #se acabó
	motor2.ChangeDutyCycle(0) #lo dejamos así, no se vaya a volver loco


def nothing(x):
    pass

if __name__== "__main__":

    cv2.namedWindow('image')

    cv2.createTrackbar('Angulo acimutal','image',0,180,nothing)
    cv2.createTrackbar('Angulo longitudinal','image',0,180,nothing)

    while(1):

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

        # get current positions of four trackbars
        acimutal = cv2.getTrackbarPos('Angulo acimutal','image')
        longitudinal = cv2.getTrackbarPos('Angulo longitudinal','image')
        sleep(0.5)
        print("Angulo acimutal: " + str(acimutal) + " Angulo longitudinal: " + str(longitudinal))
        
        SetAngleAA(acimutal) #llamada de la fun ARRIBA ABAJO
        SetAngleLL(longitudinal) #llamada de la fun LADO LADO


    cv2.destroyAllWindows()
    exit(0)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from easygui import *
import subprocess # Importamos el subprocess para llamar al programa motion
import time
import sys
from statemachine import StateMachine

motion_enable = False
graficas_enable = False
servos_enable = False
proceso_motion = []
proceso_visor = []
proceso_graficas = []
proceso_servos = []

def start_window(txt):
    msg = """ Bienvenido a la interfaz de U-CARE!\n
    Este proyecto ha sido creado por Samuel Yanes y Cristina Guzmán."""

    title = "U-CARE GUI"

    choices = ["Continuar","Salir"]

    choice = buttonbox(msg, title = title, choices = choices, default_choice= "Aceptar", image = "harold_pls.png")
    print(choice)
    if choice == "Salir":
        sys.exit(0)
    else:
        return("STATE_Buttons",txt)

def buttons_window(txt):

    msg = "Escoja la opcion que quiera"
    reply = buttonbox(msg, choices = ["Salir"], image = ["camera.png","graphs.png","servo.png"], cancel_choice="Salir")

    if reply == "Salir":
        return("STATE_R_U_SURE",txt)
    elif reply == "camera.png":
        return("STATE_Camera",txt)
    elif reply == "graphs.png":
        return("STATE_Graficos",txt)
    elif reply == "servo.png":
        return("STATE_cameracontrol",txt)

def camera_handler(txt):

    global motion_enable
    global proceso_motion
    global proceso_visor

    if(motion_enable == False):
       
        proceso_motion = subprocess.Popen('motion')
        motion_enable = True
        time.sleep(3)
        proceso_visor = subprocess.Popen(['xdg-open','http://localhost:8080'])

    else:

        msgbox("La camara ya está funcionando. Abra el explorador con la url: http://localhost:8080", title="Atención")


    return("STATE_Buttons",txt)

def graficos_hanlder(txt):

    global proceso_graficas
    global graficas_enable

    if graficas_enable == False:
        # Aquí deberíamos hacer las cositas adecuadas como mostrar los graficos y llevarnos al NODE-RED GUI#
        graficas_enable = True
        proceso_graficas = subprocess.Popen(['python','main_code.py'])

    else:
        pass

    return("STATE_Buttons",txt)
    

def exit_function(txt):
    global motion_enable
    global proceso_motion
    global proceso_visor
    global proceso_servos   

    print("Apagando ...")
    time.sleep(3)
    if motion_enable == True:

        proceso_motion.terminate()
        proceso_motion.communicate()

        proceso_visor.terminate()
        proceso_visor.communicate()

    if graficas_enable == True:
        proceso_graficas.terminate()
        proceso_graficas.communicate()

    if servos_enable == True:
        proceso_servos.terminate()
        proceso_servos.communicate()
        
    return("Bye_state",txt)

def are_you_sure_function(txt):

    msg = "Voy a cerrar todo. Estas seguro?"
    choices = ["Si","No"]
    reply = buttonbox(msg, choices = choices, cancel_choice="No")

    if reply == "Si":
        return("STATE_Exit",txt)
    else:
        return("STATE_Buttons",txt)


def cameracontrol_function(txt):
    global servos_enable
    global proceso_servos

    # Ventana de control de los servomotores #
    if servos_enable == False:
        servos_enable = True
        proceso_servos = subprocess.Popen(['python','control_camera_position.py'])
    else:
        msgbox("El programa de control de la cámara ya está abierto.", title="Atención")

    return("STATE_Buttons",txt)
    

    
    

# Funcion MAIN 
if __name__== "__main__":

    # Creamos la FSM #
    m = StateMachine()
    m.add_state("STATE_Welcome", start_window)
    m.add_state("STATE_Buttons", buttons_window)
    m.add_state("STATE_Camera", camera_handler)
    m.add_state("STATE_Graficos", graficos_hanlder)
    m.add_state("STATE_Exit", exit_function)
    m.add_state("STATE_R_U_SURE", are_you_sure_function)
    m.add_state("STATE_cameracontrol", cameracontrol_function)
    m.add_state("Bye_state",None,end_state=1)
    m.set_start("STATE_Welcome")
    m.run("Exec")

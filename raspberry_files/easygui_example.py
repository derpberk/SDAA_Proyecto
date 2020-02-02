#!/usr/bin/env python
# -*- coding: utf-8 -*-

from easygui import *
import subprocess # Importamos el subprocess para llamar al programa motion
import time
import sys
from statemachine import StateMachine

motion_enable = False
graficas_enable = False
proceso_motion = []
proceso_visor = []
proceso_graficas = []

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
    choices = ["CARE-Cam","Monitorizacion","Desconectar"]
    reply = buttonbox(msg, choices = ["Salir"], image = ["camera.png","graphs.png"], cancel_choice="Salir")

    if reply == "Salir":
        return("STATE_R_U_SURE",txt)
    elif reply == "camera.png":
        return("STATE_Camera",txt)
    elif reply == "graphs.png":
        return("STATE_Graficos",txt)

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
        
    return("Bye_state",txt)

def are_you_sure_function(txt):

    msg = "Voy a cerrar todo. Estas seguro?"
    choices = ["Si","No"]
    reply = buttonbox(msg, choices = choices, cancel_choice="No")

    if reply == "Si":
        return("STATE_Exit",txt)
    else:
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
    m.add_state("Bye_state",None,end_state=1)
    m.set_start("STATE_Welcome")
    m.run("Exec")


"""
while 1:
    msgbox("Hello, world!")

    msg ="What is your favorite flavor?"
    title = "Ice Cream Survey"
    choices = ["Vanilla", "Chocolate", "Strawberry", "Rocky Road"]
    choice = choicebox(msg, title, choices)

    # note that we convert choice to string, in case
    # the user cancelled the choice, and we got None.
    msgbox("You chose: " + str(choice), "Survey Result")

    msg = "Do you want to continue?"
    title = "Please Confirm"
    if ccbox(msg, title):     # show a Continue/Cancel dialog
        pass  # user chose Continue
    else:
        sys.exit(0)           # user chose Cancel

"""
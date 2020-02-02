#!/usr/bin/env python

# Programa principal de comunicacion con el uCARE Glove #
import requests
import time
import paho.mqtt.client as mqtt
import numpy as np
from printlog import printlog as printlog # Funcion especial para imprimir logs creada para la ocasion #
import matplotlib.pyplot as plt

# Parametros de conexion #
CLIENT_ID = "Raspbi_ID"
BROKER_LOCALHOST_IP = "192.168.1.138"
DEVICE_IP = "192.168.1.138" 
ACC_SENSOR_TOPIC = "sensors/acc"
PULSE_SENSOR_TOPIC = "sensors/pulse"
OXI_SENSOR_TOPIC = "sensors/oxigen"
TM = 2
t_init = 0

# Ip del dispositivo del Glove #

ip_mqtt_broker = BROKER_LOCALHOST_IP
ip_dispositivo = DEVICE_IP
conf_route = "/r_u_here"
FLAG_new_data = False

acc_vct = np.array([])
pulse_vct = np.array([])
oxigen_vct = np.array([])

t_acc_vct = np.array([])
t_pulse_vct = np.array([])
t_oxigen_vct = np.array([])

data_windows = 100


# Funcion principal #

def data_handler(client, userdata, msg):
    global FLAG_new_data
    global t_init
    global t_acc_vct, t_oxigen_vct, t_pulse_vct
    global acc_vct, pulse_vct, oxigen_vct
    global data_windows

    #printlog(str(msg.payload.decode("utf-8")))

    """ESTABLECEMOS QUE EL FORMATO DEL MENSAJE ES UN STRING 
        COMO EL SIGUIENTE. PAYLOAD:

        dddddd

    """

    # Debemos hacer cosas rapiditas que estamos en un handler y no conviene
    # detener la ejecucion en este punto #

    dato = float(str(msg.payload.decode("utf-8")))

    if(msg.topic == ACC_SENSOR_TOPIC): # Dato de acelerometro recibido #

        if(len(acc_vct) < data_windows):
            acc_vct = np.append(acc_vct,dato)
            t_acc_vct = np.append(t_acc_vct, time.time()-t_init)
        else:
            acc_vct = np.roll(acc_vct,-1)
            acc_vct[data_windows-1] = dato
            t_acc_vct = np.roll(t_acc_vct,-1)
            t_acc_vct[data_windows-1] = time.time()-t_init

        
    elif(msg.topic == OXI_SENSOR_TOPIC): # Dato de oximetro recibido #

        if(len(oxigen_vct) < data_windows):
            oxigen_vct = np.append(oxigen_vct,dato)
            t_oxigen_vct = np.append(t_oxigen_vct, time.time()-t_init)
        else:
            oxigen_vct = np.roll(oxigen_vct,-1)
            oxigen_vct[data_windows-1] = dato
            t_oxigen_vct = np.roll(t_oxigen_vct,-1)
            t_oxigen_vct[data_windows-1] = time.time()-t_init
    
    elif(msg.topic == PULSE_SENSOR_TOPIC): # Dato del pulsimetro recibido #

        if(len(pulse_vct) < data_windows):
            pulse_vct = np.append(pulse_vct,dato)
            t_pulse_vct = np.append(t_pulse_vct, time.time()-t_init)
        else:
            pulse_vct = np.roll(pulse_vct,-1)
            pulse_vct[data_windows-1] = dato
            t_pulse_vct = np.roll(t_pulse_vct,-1)
            t_pulse_vct[data_windows-1] = time.time()-t_init

    FLAG_new_data = True





if __name__ == "__main__":

    t_init = time.time()
    
    try:
        printlog("Creando cliente MQTT ...","INFO")
        client = mqtt.Client(CLIENT_ID)
        printlog("Cliente MQTT creado!","OK")

        printlog("Conectando a Broker MQTT","INFO")
        client.connect(BROKER_LOCALHOST_IP)
        # Comenzamos el loop de escucha #
        client.loop_start() 
        printlog("Conectado a la red MQTT!","OK")

        printlog("Escuchando los topics de sensores...","INFO")
        client.subscribe(ACC_SENSOR_TOPIC)
        client.subscribe(PULSE_SENSOR_TOPIC)
        client.subscribe(OXI_SENSOR_TOPIC)
        printlog("CRASH","INFO")
        client.on_message = data_handler
        printlog("Conectado a los sensores","OK")
    
    except:
        # Fallo de red. Troubles handling ... #
        printlog("ERROR DE CONEXION. VERIFIQUE LA RED MQTT.","ERROR")

    
    # Emitimos mensaje de conexion # 
    printlog("Dispositivo uCARE conectado!","INFO")
    

    while(1):

        # Ponemos el flag a 0 #
        FLAG_new_data = False
        time.sleep(0.5)
        if(FLAG_new_data): # Si hay un nuevo dato #
            # printlog("ACTUALIZAMOS LOS DATOS","INFO")

            # Visualizacion de una variable #
            
            plt.clf()

            ax1 = plt.subplot(3,1,1)
            plt.plot(t_acc_vct,acc_vct,'r-')
            ax1.set(xlabel='t (s)', ylabel='Aceleracion (G)')

            ax2 = plt.subplot(3,1,2)
            plt.plot(t_pulse_vct,pulse_vct,'b-')
            ax2.set(xlabel='t (s)', ylabel='Pulso (Puls/min)')

            ax3 = plt.subplot(3,1,3)
            plt.plot(t_oxigen_vct,oxigen_vct,'g-')
            ax3.set(xlabel='t (s)', ylabel='Sat. Oxi (%)')

            plt.draw()

            plt.pause(0.001)

            #################################


        

    
    

    

    
    
    
    

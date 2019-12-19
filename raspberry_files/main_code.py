#!/usr/bin/env python

# Programa principal de comunicacion con el uCARE Glove #
import requests
import time
import paho.mqtt.client as mqtt
import printlog.printlog as printlog # Funcion especial para imprimir logs creada para la ocasion #
# Parametros de conexion #

CLIENT_ID = "Raspbi_ID"
BROKER_LOCALHOST_IP = "192.168.1.137"
DEVICE_IP = "192.168.1.255" 
ACC_SENSOR_TOPIC = "sensors/acc"
PULSE_SENSOR_TOPIC = "sensors/pulse"
OXI_SENSOR_TOPIC = "sensors/oxigen"
TM = 2

# Ip del dispositivo del Glove #

ip_mqtt_broker = LOCALHOST_IP
ip_dispositivo = DEVICE_IP
conf_route = "/r_u_here"
FLAG_new_data = False

# Funcion principal #
if __name__ == "__main__":
    
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
        printlog("Conectado a los sensores","OK")
    
    except:
        # Fallo de red. Troubles handling ... #
        printlog("ERROR DE CONEXION. VERIFIQUE LA RED MQTT.","ERROR")

    
    FLAG_new_data = False
    while(1){

        # Esperamos un tiempo de recepcion TM #
        time.sleep(TM)
        if(FLAG_new_data): # Si hay un nuevo dato #
            printlog("DATOS NUEVOS RECIBIDOS!!!","INFO")

    }
    
    # Emitimos mensaje de conexion # 
    printlog("Dispositivo uCARE conectado!","INFO")

    

    
    
    
    

#!/usr/bin/env python

import random
import time
import paho.mqtt.client as mqtt
from printlog import printlog as printlog 
import numpy as np

BROKER_LOCALHOST_IP = "192.168.1.138"
CLIENT_ID = "random_acc_generator"
ACC_SENSOR_TOPIC = "sensors/acc"

printlog("Creando cliente MQTT ...","INFO")

client = mqtt.Client(CLIENT_ID)
printlog("Cliente MQTT creado!","OK")

printlog("Conectando a Broker MQTT","INFO")
client.connect(BROKER_LOCALHOST_IP)
# Comenzamos el loop de escucha #
client.loop_start() 
printlog("Conectado a la red MQTT!","OK")

i = 0
d = np.linspace(0,2*np.pi,30)
y = np.sin(d)

while(True):

    n = random.randrange(-10,10)*0.05
    client.publish(ACC_SENSOR_TOPIC,y[i]+n)

    i += 1
    if(i == len(y)):
        i = 0

    time.sleep(0.1)



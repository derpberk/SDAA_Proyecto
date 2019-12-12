#!/usr/bin/env python

import requests
import time

ip_dispositivo = "192.168.1.200"
conf_route = "/r_u_here"


# Funcion principal #
if __name__ == "__main__":
    
    """ Así es cómo se captura un html 
        url = 'https://www.google.com/'
        r = requests.get(url)
        r.text
    """
    num_failed_conection = 0
    while(num_failed_conection < 10):
        time.sleep(5)
        try:
            resp = requests.get(ip_dispositivo+conf_route)
        except:
            num_failed_conection += 1
            print("Intento "+str(num_failed_conection)+"...")
    
    # Punto de salida si no se conecta a tiempo #
    if(num_failed_conection == 10):
        print("Dispositivo no encontrado. Asegurese de que tiene su dispositivo conectado.")
        exit()
    
    # Emitimos mensaje de conexion # 
    print("Dispositivo uCARE conectado!")

    
    
    
    

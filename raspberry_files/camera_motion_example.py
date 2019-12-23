#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Programa de testeo de la cámara

import subprocess # Importamos el subprocess para llamar al programa motion
import time

# Este modulo verifica que se puede usar la liberia subprocess para iniciar 
# procesos paralelos (threads) en el contexto de la GUI #

proceso = subprocess.Popen('motion')
print("COMIENZO A ESPERAR")
time.sleep(5)
print("ME HE CANSADO DE ESPERAR")
proceso.terminate() # Mandamos SIGTERM #
proceso.communicate() # Esperamos a que el proceso termine #

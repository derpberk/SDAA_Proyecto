for pushover import init, Client
import paho.mqtt.client as mqtt
from printlog import printlog as printlog # Funcion especial para imprimir logs creada para la ocasion #
import smtplib

# RECUERDA INSTALAR ESTO pip install python-pushover 

CLIENT_ID = "FreeFall_Observator"
BROKER_LOCALHOST_IP = "broker.hivemq.com"
ACC_SENSOR_TOPIC = "sensors/acc"
API_TOKEN_PUSHOVER = "acizppozqqjvim492e4vtus74htmfp" # Creada con mi cuenta de Pushover
USER_KEY_PUSHOVER = "u1kuav95hfck5x1c8fsozp8po8evru"
EMAIL_SOURCE = "sdaa.ucare@gmail.com"
EMAIL_PASSWD = "ucaresdaa"
EMAIL_PUSHOVER = "gikmri6cy1@pomail.net"
FLAG_new_data = False
msg_email = []

dato = 1

def data_handler(client, userdata, msg):
    global FLAG_new_data
    global dato

    # Capturamos el dato recibido #
    dato = float(str(msg.payload.decode("utf-8")))
    # Activamos el flag de recepcion de dato #
    FLAG_new_data = True


if __name__ == "__main__":
    # Inicializamos la API mediante su token #
    init(API_TOKEN_PUSHOVER)

    printlog("Creando cliente MQTT ...","INFO")
    clientMQTT = mqtt.Client(CLIENT_ID)
    printlog("Cliente MQTT creado!","OK")

    printlog("Conectando a Broker MQTT","INFO")
    clientMQTT.connect(BROKER_LOCALHOST_IP)

    # Comenzamos el loop de escucha del topic del acelerometro #
    clientMQTT.loop_start() 
    printlog("Conectado a la red MQTT!","OK")

    printlog("Escuchando el topic del acelerometro","INFO")
    clientMQTT.subscribe(ACC_SENSOR_TOPIC)
    printlog("Listo!","INFO")
    clientMQTT.on_message = data_handler
    printlog("Todo listo. Preparado para detectar caidas.","OK")

    # Creamos el cliente de pushover #
    pushover_client = Client("u1kuav95hfck5x1c8fsozp8po8evru", api_token=API_TOKEN_PUSHOVER)
    pushover_client.send_message("Se ha conectado U-CARE GLOVE", title="Todo va bien!")

    # Creamos el servidor smtp para norificaciones email #
    SMTPserver = smtplib.SMTP('smtp.gmail.com',587)
    SMTPserver.starttls()
    SMTPserver.login(EMAIL_SOURCE,EMAIL_PASSWD)

    # Creamos el mensaje predeterminado de aviso #
    msg = "Me he caido. Ayuda. Llama al 662238625"

    while True:

        if(FLAG_new_data == True):
            # Reseteamos el flag
            FLAG_new_data = False
            
            if(data < ACC_THRESHOLD): # Se ha detectado una caida #

                # Avisamos por email #
                printlog("TERRIBLES NOTICIAS. SE HA DETECTADO UNA CAIDA","ERROR")
                SMTPserver.sendmail(EMAIL_SOURCE,EMAIL_PUSHOVER,msg)

                # Avisamos por pushover #
                pushover_client.send_message(msg, title="Aviso de caida!")
                

            
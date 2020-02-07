#include <WiFiNINA.h>
#include <PubSubClient.h>

/** Sensor Libraries */
#include <MPU6050_tockn.h>
#include <Wire.h>


#define TM 200 /* Milisegundos entre transmision */

/* Definiciones de los nombres de los topics de comunicacion */

#define MQTT_TOPIC_IN "ucare_topic_in"
#define MQTT_TOPIC_OUT_ACC "sensors/acc"
#define MQTT_TOPIC_OUT_OXI "sensors/oxigen"
#define MQTT_TOPIC_OUT_PUL "sensors/pulse"

/* Lets introduce our password and ssid */
const char* ssid = "Redmi";        // your network SSID (name)
const char* pass = "123456789";    // your network password (use for WPA, or use as key for WEP)
const char* mqttServer = "broker.hivemq.com";
const char* mqttUsername = "mqttUSERNAME";
const char* mqttPassword = "mqttPASSWORD";

int status = WL_IDLE_STATUS;
long lastMsg = 0;
char msg[50];
int value = 0;

/* Variable sensores */
MPU6050 mpu6050(Wire);
float ax,ay,az;

WiFiClient wifiClient;
PubSubClient client(wifiClient);


void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}


void callback(char* topic, byte* payload, unsigned int length) 
{
    Serial.println("He recibido un dato!");
}

void setup() {

  /* Declaramos el LED como salida */
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  /* Inicializamos el puerto serie para depuracion */
  Serial.begin(9600);

  /* Verificamos si esta disponible el modulo WiFi */
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Modulo WiFi no disponible");
    /* Debug exit */
    while (true);
  }
  
  /* Comprobamos que el firmware esta actualizado*/
  String fv = WiFi.firmwareVersion();
  if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
    Serial.println("Actualice el software, por favor");
  }

  /* Nos conectamos al WiFi */

  while (status != WL_CONNECTED) {
    Serial.print("Tratando de conectar a la red: ");
    Serial.println(ssid);
    /* Nos conectamos al SSID */
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(10000);
  }

  /* Imprimimos los datos de la red */
  printWifiStatus();
  /* Activamos el LED para verificar que estamos conectados a la red*/
  digitalWrite(LED_BUILTIN, HIGH);
 
  /* Nos conectamos al cliente MQTT */
  client.setServer(mqttServer, 1883);
  client.setCallback(callback);

  /* Nos conectamos con los sensores */
  Wire.begin();
  mpu6050.begin();  
}

void reconnect() 
{
  /* Esperamos a conectarnos */
  while (!client.connected()) 
  {
    Serial.print("Attempting MQTT connection...");
    /* Creamos un ID aleatorio para evitar duplicidades */
    String clientId = "ArduinoClient-";
    clientId += String(random(0xffff), HEX);

    /* Intentamos la conexion */
    if (client.connect(clientId.c_str())) 
    {
      Serial.println("connected");
      // ... nos suscribimos a los topics
      /* Escribir aqui los topics */
      client.subscribe("topic_de_entrada");
    } else 
    {
      Serial.print("ERROR, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");

      /* Esperamos 5 segundos para volver a intentarlo */
      delay(5000);
    }
  }
}

void loop() 
{
  if (!client.connected()) 
  {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > TM) 
  {

    /* Actualizamos el valor de los acelerometros */
    mpu6050.update();

    /** Publicamos los datos de los sensores */

    // Sensor de Oxigeno en sangre - DEBUGGIN//
    lastMsg = now;
    snprintf(msg,5,"%.4f",99 + ((float)random(0,40) - 20)/100);
    client.publish(MQTT_TOPIC_OUT_OXI, msg);

    // Sensor de Pulso - DEBUGGIN//
    snprintf(msg,5,"%.4f",75 + ((float)random(0,10) - 5));
    client.publish(MQTT_TOPIC_OUT_PUL, msg);

    
    // Sensor de Acelerometro - DEBUGGIN//
    ax = mpu6050.getAccX();
    ay = mpu6050.getAccY();
    az = mpu6050.getAccZ();
    
    snprintf(msg,5,"%.4f",sqrt(ax*ax+ay*ay+az*az));
    client.publish(MQTT_TOPIC_OUT_ACC, msg);
  }
}

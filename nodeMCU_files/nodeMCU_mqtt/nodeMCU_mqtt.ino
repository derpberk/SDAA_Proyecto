
/** Programacion de uCARE mediante el protocolo MQTT */

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

/* Definiciones de los nombres de los topics de comunicacion */

#define MQTT_TOPIC_IN "ucare_topic_in"
#define MQTT_TOPIC_OUT "sensors/acc"
#define TM 200 // Tiempo de refresco para transmitir datos de los sensores //

/* Datos de la red. Configrurar antes */

const char* ssid = "MIWIFI_2G_69FZ";
const char* password = "VHqTa9kt";
const char* mqtt_server = "192.168.1.130";

/* Creamos el objeto de cliente WiFi */
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

void setup_wifi() {

  delay(10);
  
  /* Debug msgs para la conexion WiFi */
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  /* Imprimimos los datos de la conexion y la IP dinámica asignada */
  /** De momento sera dinamica, pero es preferiblemente estatica para
   * una facil identificacion */

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

}

/** Funcion de callback para cuando el sistema recibe un mensaje (cualquier msg)
 * por la red MQTT */

void callback(char* topic, byte* payload, unsigned int length) {

  // Cambiamos el LED de valor para asegurarnos que hemos recibido el msg //
  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW); 
  } else {
    digitalWrite(BUILTIN_LED, HIGH);  
  }

}

/** Funcion de reconexion. Sirve para mantener viva la conexion de MQTT */
void reconnect() {

  // Iteramos hasta estar conectados finalmente al MQTT-Broker //

  while (!client.connected()) {

    Serial.print("Attempting MQTT connection...");
    
    /* ID DEL CLIENTE - UCARE */
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);

    /* Intentamos la conexion */
    if (client.connect(clientId.c_str())) {

      Serial.println("connected");

      // Once connected, publish an announcement...
      client.publish(MQTT_TOPIC_OUT, "I'M ALIVE!!!");
      // ... and resubscribe
      client.subscribe(MQTT_TOPIC_IN);

    } else {

      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

int d[10] = {0,1,2,3,4,5,6,7,8,9};
int j = 0;

void loop() {
  float n;

  /* Verificacion de la conexion */
  if (!client.connected()) {
    reconnect();
  }

  client.loop();

  long now = millis();

  if (now - lastMsg > TM) {

    n = random(-10,10)*0.05;

    lastMsg = now;
    snprintf(msg,5,"%.4f",sin(d[j]/10*(2*3.141592))+n);
    client.publish(MQTT_TOPIC_OUT, msg);
    j++;
    if(j == 10) j = 0;

  }

}

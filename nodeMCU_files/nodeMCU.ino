/*! \brief Servidor del microcontrolador nodeMCU de la unidad guante
*
*   El servidor publica periódicamente el estado de los sensores
*   en un servidor propio con una IP fija preestablecida.
*   Cualquiera conectado a la misma red podrá observar los datos.
*
*/

#include <ESP8266WiFi.h>        /*< Librería del ESP8266 */
#include <WiFiClient.h>         /*< Librería para el acceso http */
#include <ESP8266WebServer.h>   /*< Librería para crear el servidor */
#include <ESP8266mDNS.h>        /*< Librería para la asignación de la IP*/
#include "web_html_files.h"     /*< Colección de literales HTML para las webs */

/* Asignamos el SSID y la contraseña de la red WiFi */
#ifndef STASSID
#define STASSID "your-ssid"
#define STAPSK  "your-password"
#endif

IPAddress ip(192,168,1,200);     
IPAddress gateway(192,168,1,1);   
IPAddress subnet(255,255,255,0);   

#define BUILTIN_LED 12

const char *ssid = STASSID;     /* SSID de la red a conectar - Pasarela residencial*/
const char *password = STAPSK; /* Contraseña de acceso a la pasarela residencial */

/**
 * Clase tipo WebServer en el puerto 80
 */
ESP8266WebServer server(80);

const int led = BUILTIN_LED; /*< Led de la placa para debuggin */

/**
 * Función handler para el directorio raíz de la página WEB - www.wherever.wv\ */
void handleRoot() {

  digitalWrite(led, 1);
  server.send(200, "text/html", root_web_str);
  digitalWrite(led, 0);

}

void handleNotFound() {

  digitalWrite(led, 1);
  String message = "ERROR 404: File Not Found\n\n";
  server.send(404, "text/plain", message);
  digitalWrite(led, 0);

}

void drawGraph() {
    
  /* Valores provisionales */
  int pulso = 60;
  int oxigeno = 99;
  int acel = 0;

  String out;
  out.reserve(2600);
  char temp[70];

  /* Componemos la medida de pulso */
  out += "<p><strong><em>Datos del servidor</em></strong></p>";
  snprintf(temp,"<p><em>Pulso medio: %d</em></p>",pulso);
  out += temp;

  /* Componemos la medida de pulso */
  snprintf(temp,"<p><em>Oxigeno: %d</em></p>",oxigeno);
  out += temp;

  /* Componemos la medida de pulso */
  snprintf(temp,"<p><em>Acel: %d</em></p>",acel);
  out += temp;

  server.send(200, "text/html", out);
}


void setup(void) {
  
    /* Pin de debuggin */
    pinMode(led, OUTPUT);
    digitalWrite(led, LOW);

    /* Inicializamos el puerto serie para depuración */
    Serial.begin(115200);
    WiFi.mode(WIFI_STA);
    WiFi.config(ip, gateway, subnet);
    WiFi.begin(ssid, password);
    Serial.println("");

    /* Esperamos a conectarnos */
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());

 /*   if (MDNS.begin("esp8266")) {
  *      Serial.println("MDNS responder started");
  *  }
  */

    server.on("/", handleRoot);
    server.on("/getSensors", drawGraph);
    server.onNotFound(handleNotFound);
    server.begin();
    Serial.println("HTTP server started");
}

void loop(void) {

  server.handleClient();
  
}

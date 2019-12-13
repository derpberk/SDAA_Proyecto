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
#define STASSID "MIWIFI_2G_69FZ"
#define STAPSK  "VHqTa9kt"
#endif

#define led 12

const char *ssid = STASSID;     /* SSID de la red a conectar - Pasarela residencial*/
const char *password = STAPSK; /* Contraseña de acceso a la pasarela residencial */

/**
 * Función handler para el directorio raíz de la página WEB - www.wherever.wv\ 
 */
ESP8266WebServer server(80);

void handleRoot() {

  digitalWrite(led, 1);
  server.send(200, "text/html", root_web_str);
  digitalWrite(led, 0);

}

void sensorsHandler() {
    
  /* Valores provisionales */
  int pulso = 60;
  int oxigeno = 99;
  int acel = 0;

  String out;
  out.reserve(2600);
  char temp[70];

  /* Componemos la medida de pulso */
  out += "<p><strong><em>Datos del servidor</em></strong></p>";
  sprintf(temp,"<p><em>Pulso medio: %d</em></p>",pulso);
  out += temp;

  /* Componemos la medida de pulso */
  sprintf(temp,"<p><em>Oxigeno: %d</em></p>",oxigeno);
  out += temp;

  /* Componemos la medida de pulso */
  sprintf(temp,"<p><em>Acel: %d</em></p>",acel);
  out += temp;

  server.send(200, "text/html", out);
}

void handleNotFound() {

  digitalWrite(led, 1);
  String message = "ERROR 404: File Not Found\n\n";
  server.send(404, "text/plain", message);
  digitalWrite(led, 0);

}

void r_u_here_handler() {
  server.send(200, "text/plain", r_u_here_web_str);

}


void setup() {

    /* Pin de debuggin */
    pinMode(led, OUTPUT);
    digitalWrite(led, LOW);

    /* Inicializamos el puerto serie para depuración */
    Serial.begin(115200);
    WiFi.mode(WIFI_STA);
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

    server.on("/", handleRoot);
    server.on("/getSensors", sensorsHandler);
    server.on("/r_u_here", r_u_here_handler);
    server.onNotFound(handleNotFound);
    server.begin();
    Serial.println("HTTP server started");
}


void loop() {

  server.handleClient();
  
}

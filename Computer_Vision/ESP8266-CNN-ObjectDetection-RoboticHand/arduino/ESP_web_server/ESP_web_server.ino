#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WiFiMulti.h> 
#include <ESP8266mDNS.h>
#include <ESP8266WebServer.h>
#include <Servo.h>
#include <ArduinoJson.h>


ESP8266WebServer server(80);    // Create a webserver object that listens for HTTP request on port 80

Servo servoMotor;

void setup(void){
  Serial.begin(115200);         // Start the Serial communication to send messages to the computer
  delay(10);
  Serial.println('\n');
  WiFi.begin("vodafone4491", "DERIAUXYRPAPQU");  //Connect to the WiFi network
    while (WiFi.status() != WL_CONNECTED) {  //Wait for connection
        delay(500);
        Serial.println("Waiting to connect...");
     }

  //Printing connection info
  Serial.println('\n');
  Serial.print("Connected to ");
  Serial.println(WiFi.SSID());               // Tell us what network we're connected to
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());            // Send the IP address of the ESP8266 to the computer

  initServer();

}
void initServer()
{

  server.on("/", handleRoot);
  server.on("/moveServo", handleMoveServo);
  server.onNotFound(handleNotFound);           // When a client requests an unknown URI (i.e. something other than "/"), call function "handleNotFound"
  server.begin();                            // Actually start the server
  Serial.println("HTTP server started");
  servoMotor.attach(5); //connected to pin D1
  servoMotor.write(0);
}

void loop(void){
  server.handleClient();                     // Listen for HTTP requests from clients
}

// Funcion que se ejecutara en la URI '/'
void handleRoot()
{
   server.send(200, "text/plain", "Hello World!");
}

void handleMoveServo() {                         

  if (server.hasArg("plain")== false){ //Check if body received
      server.send(200, "text/plain", "Body not received");
      return;
  }

  DynamicJsonDocument doc(1024);
  // Parse JSON object
  DeserializationError error = deserializeJson(doc, server.arg("plain"));
  if (error) {
    Serial.println("Parsing failed!");
    return;
  }
  
  // Decode JSON/Extract values
  int degree1 = doc["degree1"];
  //int degree2 = doc["degree2"];
  Serial.println(degree1);
  //Serial.println(degree2);
  servoMotor.write(degree1);
  delay(1000);
  //servoMotor.write(degree2);
  //delay(1000); 
  Serial.println("OK, servo moved");
  server.send(200,"OK, servo moved");

 }




void handleNotFound(){
  server.send(404, "text/plain", "404: Not found"); // Send HTTP status 404 (Not Found) when there's no handler for the URI in the request
}

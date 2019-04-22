
/*
  File: RestClient.ino
  This example makes an HTTP request after 10 seconds and shows the result both in
  serial monitor and in the wifi console of the Arduino Uno WiFi.

  Note: works only with Arduino Uno WiFi Developer Edition.

  http://www.arduino.org/learning/tutorials/boards-tutorials/restserver-and-restclient
*/

#include <Wire.h>
#include <UnoWiFiDevEd.h>

const char* connector = "rest";
const char* server = "192.168.5.13";
const char* method = "GET";
const char* resource = "/device?test=1";

void setup() {


  Serial.begin(9600);
  Ciao.begin();

  log(F("\nWelcome to smart window controller"));
}

void loop() {

  doRequest(connector, server, resource, method);
  delay(1000);
}

void doRequest(const char* conn, const char* server, const char* command, const char* method) {
  log("Sending request to: " + String(server));
      CiaoData data = Ciao.read(conn, server, command, method);
  if (!data.isEmpty()) {
  Ciao.println( "State: " + String (data.get(1)) );
    Ciao.println( "Response: " + String (data.get(2)) );
    Serial.println( "State: " + String (data.get(1)) );
    Serial.println( "Response: " + String (data.get(2)) );
  }
  else {
    Ciao.println ("Write Error");
    Serial.println ("Write Error");
  }
}


void log(String message) {
  Ciao.println(message);
  Serial.println(message);
}

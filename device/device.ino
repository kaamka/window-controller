/*
  File: device.ino
  Main code for smart window controler.

  This example code is part of the public domain

  Note: works only with Arduino Uno WiFi Developer Edition.

  Requires:
  - UnoWiDiDevEd.h
  - Adafruit unified sensor
  - DHT by adafruit
*/

#include <Wire.h>
#include <UnoWiFiDevEd.h>
#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT11   // DHT 11

#define SMOKEPIN A0
#define MICPIN A1

#define LED_RED 13
#define LED_GREEN 12
#define LED_BLUE 11


bool open = false;
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Wifi.begin();
  Wifi.println("REST Server is up");

  // set up led indicator
  pinMode(LED_RED, OUTPUT);

  // set up sensors
   dht.begin();

   // set up serial for debugging
   Serial.begin(57600);
}

void loop() {

  while (Wifi.available()) {
    process(Wifi);
  }
  delay(50);

}

void process(WifiData client) {
  // read the command
  String command = client.readStringUntil('/');

  // is "digital" command?
  if (command == "digital") {
    String command2 = client.readStringUntil('/');
    if (command2 == "status") {
      statusCommand(client);
    } else if (command2 == "setting") {
      settingCommand(client);
    } else if (command2 == "data") {
      dataCommand(client);
    } else if (command2 == "open") {
      openCommand(client);
    } else if (command2 == "close") {
      closeCommand(client);
    } else {
      client.println("HTTP/1.1 404 Not found\n");
      client.print(EOL);
    }
  }
}

void statusCommand(WifiData client) {

  // Send feedback to client
  headers(client);
  if (open) {
    client.print("open");
  } else {
    client.print("closed");
  }
  client.print(EOL);
}

void openCommand(WifiData client) {
  headers(client);
  if (!open) {
    client.print("ok");
    client.print(EOL);
    open = true;
    moveActuator(LED_BLUE);
  } else {
    client.print("was_open");
    client.print(EOL);
  }
}

void closeCommand(WifiData client) {
  headers(client);
  if (open) {
    client.print("ok");
    client.print(EOL);
    open = false;
    moveActuator(LED_RED);
  } else {
    client.print("was_closed");
    client.print(EOL);
  }
}



void moveActuator(int led) {
  for (int i = 0; i < 10; i++) {
    digitalWrite(led, HIGH);
    delay(200);
    digitalWrite(led, LOW);
    delay(200);
  }
}


void settingCommand(WifiData client) {

  // Send feedback to client
  headers(client);
  client.print("setting");
  client.print(EOL);    //char terminator
}


void dataCommand(WifiData client) {

  float humidity =  dht.readHumidity();
  float temp = dht.readTemperature();
  int gas = analogRead(SMOKEPIN);
  int sound = getSound();
  
  if ( isnan(humidity) || isnan(temp) ){
    client.println("HTTP/1.1 500\n");
    client.println("Error reading humidity or temperature");
    client.print(EOL); 
    return;
    Wifi.println("DHT error");
  }
  
  // Send feedback to client
  headers(client);
  client.print(gas);
  client.print(","); client.print(sound);
  client.print(","); client.print((int)humidity);
  client.print(","); client.print(temp);
  client.print(EOL);

}


void headers(WifiData client) {
  client.print("HTTP/1.1 200 -\n");
  client.print("Access-Control-Allow-Origin:*\n");
  client.print("Connection:close\n");
  client.print('\n');
}


int getSound() {
  int sum = 0;
  for (byte  i = 0; i < 50; i++)
  {
    sum += analogRead(MICPIN);
    delay(1);
  }
  return - (sum/50 - 1000);
}

/**
 * Get int from a url
 * client.parseInt();
 * Read just one char
 * client.read() == '/'
 * Read string until the end
 */

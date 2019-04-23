/*
  File: device.ino
  Main code for smart window controler.

  This example code is part of the public domain

  Note: works only with Arduino Uno WiFi Developer Edition.
*/

#include <Wire.h>
#include <UnoWiFiDevEd.h>

#define LED_RED 13
#define LED_GREEN 12


bool open = false;

void setup() {
  Wifi.begin();
  Wifi.println("REST Server is up");

  // set up led indicator
  pinMode(LED_RED, OUTPUT);
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
    }
  }
}

void statusCommand(WifiData client) {

  // Send feedback to client
  client.println("HTTP/1.1 200 OK\n");
  if (open) {
    client.println("open");
  } else {
    client.println("closed");
  }

}

void openCommand(WifiData client) {
  client.println("HTTP/1.1 200 OK\n");
  if (!open) {
    client.print("ok");
    client.print(EOL);
    moveActuator(LED_RED);
    open = true;
  } else {
    client.print("was_open");
    client.print(EOL);
  }
}

void closeCommand(WifiData client) {
  client.println("HTTP/1.1 200 OK\n");
  if (open) {
    client.print("ok");
    client.print(EOL);
    moveActuator(LED_GREEN);
    open = false;
  } else {
    client.print("was_closed");
    client.print(EOL);
  }
}



void moveActuator(int led) {
  for (int i = 0; i < 10; i++) {
    digitalWrite(led, HIGH);
    delay(500);
    digitalWrite(led, LOW);
    delay(500);
  }
}


void settingCommand(WifiData client) {

  // Send feedback to client
  client.println("HTTP/1.1 200 OK\n");
  client.print("setting");
  client.print(EOL);    //char terminator

}


void dataCommand(WifiData client) {

  // Send feedback to client
  client.println("HTTP/1.1 200 OK\n");
  client.print("{");
  client.print("\n\tgas: "); client.print(getSound());
  client.print("\n\tsound: "); client.print(getSound());
  client.print("\n\thumidity: "); client.print(getHumidity());
  client.print("\n\ttemp: "); client.print(getTemp());
  client.print("\n}");
  client.print(EOL);    //char terminator

}

int getGas() {
  return 0;
}


int getHumidity() {
  return 0;
}


int getTemp() {
  return 0;
}


int getSound() {
  return 0;
}

/**
 * Get int from a url
 * client.parseInt();
 * Read just one char
 * client.read() == '/'
 * Read string until the end
 */

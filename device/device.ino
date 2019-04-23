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
    client.print("open");
  } else {
    client.print("closed");
  }
  client.print(EOL);    //char terminator

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
  client.print("data");
  client.print(EOL);    //char terminator

}




void digitalCommand(WifiData client) {
  int pin, value;

  // Read pin number
  pin = client.parseInt();

  // If the next character is a '/' it means we have an URL
  // with a value like: "/digital/13/1"
  if (client.read() == '/') {
    value = client.parseInt();
    digitalWrite(pin, value);
  }
  else {
    value = digitalRead(pin);
  }

  // Send feedback to client
  client.println("HTTP/1.1 200 OK\n");
  client.print("Pin D");
  client.print(pin);
  client.print(F(" set to "));
  client.println(value);
  client.print(EOL);    //char terminator

}

void analogCommand(WifiData client) {
  int pin, value;

  // Read pin number
  pin = client.parseInt();

  // If the next character is a '/' it means we have an URL
  // with a value like: "/analog/5/120"
  if (client.read() == '/') {
    // Read value and execute command
    value = client.parseInt();
    analogWrite(pin, value);

    // Send feedback to client
    client.println("HTTP/1.1 200 OK\n");
    client.print(F("Pin D"));
    client.print(pin);
    client.print(F(" set to analog "));
    client.println(value);
    client.print(EOL);    //char terminator

  }
  else {
    // Read analog pin
    value = analogRead(pin);

    // Send feedback to client
    client.println("HTTP/1.1 200 OK\n");
    client.print(F("Pin A"));
    client.print(pin);
    client.print(F(" reads analog "));
    client.println(value);
    client.print(EOL);    //char terminator

  }
}

void modeCommand(WifiData client) {
  int pin;

  // Read pin number
  pin = client.parseInt();

  // If the next character is not a '/' we have a malformed URL
  if (client.read() != '/') {
    client.println(F("error"));
    client.print(EOL);    //char terminator
    return;
  }

  String mode = client.readStringUntil('\r');

  if (mode == "input") {
    pinMode(pin, INPUT);
    // Send feedback to client
    client.println("HTTP/1.1 200 OK\n");
    client.print(F("Pin D"));
    client.print(pin);
    client.println(F(" configured as INPUT!"));
    client.print(EOL);    //char terminator
    return;
  }

  if (mode == "output") {
    pinMode(pin, OUTPUT);
    // Send feedback to client
    client.println("HTTP/1.1 200 OK\n");
    client.print(F("Pin D"));
    client.print(pin);
    client.println(F(" configured as OUTPUT!"));
    client.print(EOL);    //char terminator
    return;
  }

  client.print(F("error: invalid mode "));
  client.println(mode);
  client.print(EOL);    //char terminator
}

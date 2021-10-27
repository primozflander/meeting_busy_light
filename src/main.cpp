#include <Arduino.h>
#include "BluetoothSerial.h"

#define LED_BUILTIN 2

BluetoothSerial SerialBT;


void ledHandler(String command)
{
  if (command.equals("busy"))
  {
    digitalWrite(LED_BUILTIN, HIGH); 
  }
  else if (command.equals("ready"))
  {
    for (int i=0; i<5; i++)
    {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(100);
      digitalWrite(LED_BUILTIN, LOW);
      delay(100);
    }
  }
  else
  {
    digitalWrite(LED_BUILTIN, LOW);
  }
}


void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  SerialBT.begin("ESP32_busy_light");
  Serial.println("Setup complete");
}


void loop() {
  if (Serial.available()) {
    SerialBT.write(Serial.read());
  }
  if (SerialBT.available()) {
    String receivedCommand = SerialBT.readString();
    Serial.println(receivedCommand);
    ledHandler(receivedCommand);
  }
  delay(10);
}
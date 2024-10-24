/*
This is the example of getting ANT BMS data from Bluetooth serial communication

Author: Avtar Chodankar
Email: avtar9823@gmail.com
Github: AVTAR0901
*/


#include "BluetoothSerial.h"

//#define USE_NAME // Comment this to use MAC address instead of a slaveName
const char *pin = "1234"; // Change this to reflect the pin expected by the real slave BT device

#if !defined(CONFIG_BT_SPP_ENABLED)
#error Serial Bluetooth not available or not enabled. It is only available for the ESP32 chip.
#endif

BluetoothSerial SerialBT;

#ifdef USE_NAME
  String slaveName = "BMS-ANT24C-000"; // Change this to reflect the real name of your slave BT device
#else
  String MACadd = "AA:BB:CC:90:10:00"; // This only for printing
  uint8_t address[6]  = {0xAA, 0xBB, 0xCC, 0x90, 0x10, 0x00}; // Change this to reflect real MAC address of your slave BT device
#endif

String myName = "ESP32-BT-Master";
byte initiateByte[]  = {0xDB, 0xDB, 0x00, 0x00, 0x00, 0x00};
char s[200];

void setup() {
  bool connected;
  Serial.begin(115200, SERIAL_8N1);

  SerialBT.begin(myName, true);
  Serial.printf("The device \"%s\" started in master mode, make sure slave BT device is on!\n", myName.c_str());

  #ifndef USE_NAME
    SerialBT.setPin(pin);
    Serial.println("Using PIN");
  #endif

  #ifdef USE_NAME
    connected = SerialBT.connect(slaveName);
    Serial.printf("Connecting to slave BT device named \"%s\"\n", slaveName.c_str());
  #else
    connected = SerialBT.connect(address);
    Serial.print("Connecting to slave BT device with MAC "); Serial.println(MACadd);
  #endif

  if(connected) {
    Serial.println("Connected Successfully!");
  } else {
    while(!SerialBT.connected(10000)) {
      Serial.println("Failed to connect. Make sure remote device is available and in range, then restart app.");
    }
  }

  SerialBT.write(initiateByte, sizeof(initiateByte)); //Sending HEX byte to BMS to receive data
  
}

void loop() {
  if (SerialBT.available()) {
  sprintf(s, "%02X", SerialBT.read());
  Serial.print(s);
  Serial.print(" ");
  }
}

/*
 This is client side code for sequesntial connection of ESP32 devices using BLE network
 Author: Avtar Chodankar
 Email: avtar9823@gmail.com
 github: AVTAR0901
 
 */

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

#define temperatureCelsius

BLEClient* pClient;
BLEScan* pBLEScan;
BLEAdvertisedDevice* foundDevice1 = nullptr;
BLEAdvertisedDevice* foundDevice2 = nullptr;
BLEAdvertisedDevice* foundDevice3 = nullptr;
BLEAdvertisedDevice* foundDevice4 = nullptr;
BLEAdvertisedDevice* foundDevice5 = nullptr;
BLEAdvertisedDevice* foundDevice6 = nullptr;

// UUIDs for the services on all six servers
static BLEUUID serviceUUID1("91bad492-b950-4226-aa2b-4ede9fa42f59"); // UUID for Server 1
static BLEUUID serviceUUID2("3f02e7f1-71d4-4ed9-9afe-f51001884393"); // UUID for Server 2
static BLEUUID serviceUUID3("f2f8db16-2745-463b-8bad-9fafbb892d96"); // UUID for Server 3
static BLEUUID serviceUUID4("7f9c2830-53c9-4788-abaf-5ec94cdd73b3"); // UUID for Server 4
static BLEUUID serviceUUID5("840bbcef-764b-43d3-8497-0e5efa7a141e"); // UUID for Server 5
static BLEUUID serviceUUID6("4d92048f-ee10-409b-ab33-314caf43586a"); // UUID for Server 6

// UUIDs for the characteristics on each server
// Server 1
static BLEUUID charUUID_Temp1("cba1d466-344c-4be3-ab3f-189f80dd7518");
static BLEUUID charUUID_Hum1("ffecfd19-25ed-4e8c-820f-89277636a9c1");
// Server 2
static BLEUUID charUUID_Temp2("f78ebbff-c8b7-4107-93de-889a6a06d408");
static BLEUUID charUUID_Hum2("ca73b3ba-39f6-4ab3-91ae-186dc9577d99");
// Server 3
static BLEUUID charUUID_Temp3("1e498b88-caa5-4cc0-9768-a16aac17ecb8");
static BLEUUID charUUID_Hum3("a8b6b50d-b2c6-4b7f-a731-02031455a41e");
// Server 4
static BLEUUID charUUID_Temp4("20349082-3d70-477e-809b-070ef504e806");
static BLEUUID charUUID_Hum4("78dcf577-1fb6-4091-a703-bbf96e359ed1");
// Server 5
static BLEUUID charUUID_Temp5("fc0af3d1-f62a-44bd-abaa-c02825f965ae");
static BLEUUID charUUID_Hum5("3a0dd56f-df8b-4894-bd9d-331832c1b78c");
// Server 6
static BLEUUID charUUID_Temp6("c1161a37-12f8-48c0-a43f-b114be0c6bc5");
static BLEUUID charUUID_Hum6("4de53c9c-cde3-4cdc-948f-3ba104cc4791");

// Function to connect to a server and read the characteristics
bool connectToServer(BLEAdvertisedDevice* myDevice, BLEUUID serviceUUID, BLEUUID charUUID_Temp, BLEUUID charUUID_Hum) {
  pClient = BLEDevice::createClient();
  Serial.print("Connecting to ");
  Serial.println(myDevice->getName().c_str());

  if (pClient->connect(myDevice)) {
    Serial.println("Connected to server");

    // Obtain the service for the connected server
    BLERemoteService* pRemoteService = pClient->getService(serviceUUID);
    if (pRemoteService == nullptr) {
      Serial.print("Failed to find service UUID: ");
      Serial.println(serviceUUID.toString().c_str());
      pClient->disconnect();
      return false;
    }

    // Get the temperature characteristic
    BLERemoteCharacteristic* pTempCharacteristic = pRemoteService->getCharacteristic(charUUID_Temp);
    if (pTempCharacteristic == nullptr) {
      Serial.println("Failed to find temperature characteristic");
      pClient->disconnect();
      return false;
    }

    // Get the humidity characteristic
    BLERemoteCharacteristic* pHumCharacteristic = pRemoteService->getCharacteristic(charUUID_Hum);
    if (pHumCharacteristic == nullptr) {
      Serial.println("Failed to find humidity characteristic");
      pClient->disconnect();
      return false;
    }

    // Read and print the temperature
    if (pTempCharacteristic->canRead()) {
      std::string value = pTempCharacteristic->readValue();
      Serial.print("Temperature: ");
      Serial.println(value.c_str());
    }

    // Read and print the humidity
    if (pHumCharacteristic->canRead()) {
      std::string value = pHumCharacteristic->readValue();
      Serial.print("Humidity: ");
      Serial.println(value.c_str());
    }

    pClient->disconnect(); // Disconnect after reading data
    Serial.println("Disconnected from the server");
    delay(200);
    delete pClient;
    pClient = nullptr;

    return true;
  } else {
    Serial.println("Failed to connect to the server");
    return false;
  }
}

// Callback to scan and find the devices
class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
  void onResult(BLEAdvertisedDevice advertisedDevice) {
    Serial.print("Found Device: ");
    Serial.println(advertisedDevice.getName().c_str());

    // Match by UUID and connect as soon as the device is found
    if (advertisedDevice.isAdvertisingService(serviceUUID1) && foundDevice1 == nullptr) {
      foundDevice1 = new BLEAdvertisedDevice(advertisedDevice); // Store the first server
      Serial.println("Found Server 1");
    } else if (advertisedDevice.isAdvertisingService(serviceUUID2) && foundDevice2 == nullptr) {
      foundDevice2 = new BLEAdvertisedDevice(advertisedDevice); // Store the second server
      Serial.println("Found Server 2");
    } else if (advertisedDevice.isAdvertisingService(serviceUUID3) && foundDevice3 == nullptr) {
      foundDevice3 = new BLEAdvertisedDevice(advertisedDevice); // Store the third server
      Serial.println("Found Server 3");
    } else if (advertisedDevice.isAdvertisingService(serviceUUID4) && foundDevice4 == nullptr) {
      foundDevice4 = new BLEAdvertisedDevice(advertisedDevice); // Store the fourth server
      Serial.println("Found Server 4");
    } else if (advertisedDevice.isAdvertisingService(serviceUUID5) && foundDevice5 == nullptr) {
      foundDevice5 = new BLEAdvertisedDevice(advertisedDevice); // Store the fifth server
      Serial.println("Found Server 5");
    } else if (advertisedDevice.isAdvertisingService(serviceUUID6) && foundDevice6 == nullptr) {
      foundDevice6 = new BLEAdvertisedDevice(advertisedDevice); // Store the sixth server
      Serial.println("Found Server 6");
    }
  }
};

void setup() {
  Serial.begin(115200);
  BLEDevice::init("");

  pBLEScan = BLEDevice::getScan(); // Initialize scan
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setInterval(1349);
  pBLEScan->setWindow(449);
  pBLEScan->setActiveScan(true);

  Serial.println("Starting scan for BLE devices...");
}

void loop() {
  // Start scan if any device is still missing
  if (!foundDevice1 || !foundDevice2 || !foundDevice3 || !foundDevice4 || !foundDevice5 || !foundDevice6) {
    pBLEScan->start(5, false); // Scan for 5 seconds to discover devices
  }

  // Connect to available devices and read their data
  if (foundDevice1) {
    Serial.println("Connecting to Server 1...");
    connectToServer(foundDevice1, serviceUUID1, charUUID_Temp1, charUUID_Hum1);
    delete foundDevice1;
    foundDevice1 = nullptr;
  }

  if (foundDevice2) {
    Serial.println("Connecting to Server 2...");
    connectToServer(foundDevice2, serviceUUID2, charUUID_Temp2, charUUID_Hum2);
    delete foundDevice2;
    foundDevice2 = nullptr;
  }

  if (foundDevice3) {
    Serial.println("Connecting to Server 3...");
    connectToServer(foundDevice3, serviceUUID3, charUUID_Temp3, charUUID_Hum3);
    delete foundDevice3;
    foundDevice3 = nullptr;
  }

  if (foundDevice4) {
    Serial.println("Connecting to Server 4...");
    connectToServer(foundDevice4, serviceUUID4, charUUID_Temp4, charUUID_Hum4);
    delete foundDevice4;
    foundDevice4 = nullptr;
  }

  if (foundDevice5) {
    Serial.println("Connecting to Server 5...");
    connectToServer(foundDevice5, serviceUUID5, charUUID_Temp5, charUUID_Hum5);
    delete foundDevice5;
    foundDevice5 = nullptr;
  }

  if (foundDevice6) {
    Serial.println("Connecting to Server 6...");
    connectToServer(foundDevice6, serviceUUID6, charUUID_Temp6, charUUID_Hum6);
    delete foundDevice6;
    foundDevice6 = nullptr;
  }
}

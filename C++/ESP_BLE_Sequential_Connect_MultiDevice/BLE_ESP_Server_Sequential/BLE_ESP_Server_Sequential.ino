 /*
This is server side implementation of sequential connection between ESP32 devices using BLE network
 
 Author: Avtar Chodankar
 Email: avtar9823@gmail.com
 github: AVTAR0901
 
*/
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <Wire.h>

#define temperatureCelsius

// BLE server name (Uncomment for each server individually)
//#define bleServerName "ESP_1" // For 1st Server
//#define bleServerName "ESP_2" // For 2nd Server
//#define bleServerName "ESP_3" // For 3rd Server
//#define bleServerName "ESP_4" // For 4th Server
//#define bleServerName "ESP_5" // For 5th Server
#define bleServerName "ESP_6" // For 6th Server

float temp;
float tempF;
float hum;

// Timer variables
unsigned long lastTime = 0;
unsigned long timerDelay = 10000;

bool deviceConnected = false;

// Replace with your service UUIDs
//#define SERVICE_UUID "91bad492-b950-4226-aa2b-4ede9fa42f59" // For 1st Server
//#define SERVICE_UUID "3f02e7f1-71d4-4ed9-9afe-f51001884393" // For 2nd server
//#define SERVICE_UUID "f2f8db16-2745-463b-8bad-9fafbb892d96" // For 3rd server
//#define SERVICE_UUID "7f9c2830-53c9-4788-abaf-5ec94cdd73b3" // For 4th server
//#define SERVICE_UUID "840bbcef-764b-43d3-8497-0e5efa7a141e" // For 5th server
#define SERVICE_UUID "4d92048f-ee10-409b-ab33-314caf43586a" // For 6th server
/*
//-------------------------SERVER 1 DATA START----------------------------------
// Temperature Characteristic and Descriptor for SERVER 1
#ifdef temperatureCelsius
  BLECharacteristic bmeTemperatureCelsiusCharacteristics(
    "cba1d466-344c-4be3-ab3f-189f80dd7518", 
    BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);  // Added PROPERTY_READ
  BLEDescriptor bmeTemperatureCelsiusDescriptor(BLEUUID((uint16_t)0x2902));
#else
  BLECharacteristic bmeTemperatureFahrenheitCharacteristics(
    "f78ebbff-c8b7-4107-93de-889a6a06d409", 
    BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);  // Added PROPERTY_READ
  BLEDescriptor bmeTemperatureFahrenheitDescriptor(BLEUUID((uint16_t)0x2902));
#endif

// Server-specific Humidity Data (Uncomment for the respective server)
BLECharacteristic bmeHumidityCharacteristics(
  "ffecfd19-25ed-4e8c-820f-89277636a9c1", 
  BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);  // Added PROPERTY_READ
BLEDescriptor bmeHumidityDescriptor(BLEUUID((uint16_t)0x2903));
//-------------------------SERVER 1 DATA END----------------------------------
*/
/*
//-------------------------SERVER 2 DATA START----------------------------------
// Temperature Characteristic and Descriptor
#ifdef temperatureCelsius
  BLECharacteristic bmeTemperatureCelsiusCharacteristics(
    "f78ebbff-c8b7-4107-93de-889a6a06d408", 
    BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);  // Added PROPERTY_READ
  BLEDescriptor bmeTemperatureCelsiusDescriptor(BLEUUID((uint16_t)0x2902));
#else
  BLECharacteristic bmeTemperatureFahrenheitCharacteristics(
    "f78ebbff-c8b7-4107-93de-889a6a06d449", 
    BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);  // Added PROPERTY_READ
  BLEDescriptor bmeTemperatureFahrenheitDescriptor(BLEUUID((uint16_t)0x2902));
#endif

// Server-specific Humidity Data (Uncomment for the respective server)
BLECharacteristic bmeHumidityCharacteristics(
  "ca73b3ba-39f6-4ab3-91ae-186dc9577d99", 
  BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);  // Added PROPERTY_READ
BLEDescriptor bmeHumidityDescriptor(BLEUUID((uint16_t)0x2903));
//-------------------------SERVER 2 DATA END----------------------------------
*/
/*
//-------------------------SERVER 3 DATA START----------------------------------
// Temperature Characteristic and Descriptor
#ifdef temperatureCelsius
  BLECharacteristic bmeTemperatureCelsiusCharacteristics(
    "1e498b88-caa5-4cc0-9768-a16aac17ecb8", 
    BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);  // Added PROPERTY_READ
  BLEDescriptor bmeTemperatureCelsiusDescriptor(BLEUUID((uint16_t)0x2902));
#else
  BLECharacteristic bmeTemperatureFahrenheitCharacteristics(
    "c7deea65-229f-4360-9985-d5cd4e2a3270", 
    BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);  // Added PROPERTY_READ
  BLEDescriptor bmeTemperatureFahrenheitDescriptor(BLEUUID((uint16_t)0x2902));
#endif

// Server-specific Humidity Data (Uncomment for the respective server)
BLECharacteristic bmeHumidityCharacteristics(
  "a8b6b50d-b2c6-4b7f-a731-02031455a41e", 
  BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);  // Added PROPERTY_READ
BLEDescriptor bmeHumidityDescriptor(BLEUUID((uint16_t)0x2903));
//-------------------------SERVER 3 DATA END----------------------------------
*/
/*
//-------------------------SERVER 4 DATA START----------------------------------
// Temperature Characteristic and Descriptor
#ifdef temperatureCelsius
  BLECharacteristic bmeTemperatureCelsiusCharacteristics(
    "20349082-3d70-477e-809b-070ef504e806", 
    BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);  // Added PROPERTY_READ
  BLEDescriptor bmeTemperatureCelsiusDescriptor(BLEUUID((uint16_t)0x2902));
#else
  BLECharacteristic bmeTemperatureFahrenheitCharacteristics(
    "fe79ae9d-8fd5-4ed0-86b6-3f6e50c3b378", 
    BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);  // Added PROPERTY_READ
  BLEDescriptor bmeTemperatureFahrenheitDescriptor(BLEUUID((uint16_t)0x2902));
#endif

// Server-specific Humidity Data (Uncomment for the respective server)
BLECharacteristic bmeHumidityCharacteristics(
  "78dcf577-1fb6-4091-a703-bbf96e359ed1", 
  BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);  // Added PROPERTY_READ
BLEDescriptor bmeHumidityDescriptor(BLEUUID((uint16_t)0x2903));
//-------------------------SERVER 4 DATA END----------------------------------
*/
/*
//-------------------------SERVER 5 DATA START----------------------------------
// Temperature Characteristic and Descriptor
#ifdef temperatureCelsius
  BLECharacteristic bmeTemperatureCelsiusCharacteristics(
    "fc0af3d1-f62a-44bd-abaa-c02825f965ae", 
    BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);  // Added PROPERTY_READ
  BLEDescriptor bmeTemperatureCelsiusDescriptor(BLEUUID((uint16_t)0x2902));
#else
  BLECharacteristic bmeTemperatureFahrenheitCharacteristics(
    "8aafad6f-22ad-4215-a2e4-a5bfbbbdca53", 
    BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);  // Added PROPERTY_READ
  BLEDescriptor bmeTemperatureFahrenheitDescriptor(BLEUUID((uint16_t)0x2902));
#endif

// Server-specific Humidity Data (Uncomment for the respective server)
BLECharacteristic bmeHumidityCharacteristics(
  "3a0dd56f-df8b-4894-bd9d-331832c1b78c", 
  BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);  // Added PROPERTY_READ
BLEDescriptor bmeHumidityDescriptor(BLEUUID((uint16_t)0x2903));
//-------------------------SERVER 5 DATA END----------------------------------
*/
//-------------------------SERVER 6 DATA START----------------------------------
// Temperature Characteristic and Descriptor
#ifdef temperatureCelsius
  BLECharacteristic bmeTemperatureCelsiusCharacteristics(
    "c1161a37-12f8-48c0-a43f-b114be0c6bc5", 
    BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);  // Added PROPERTY_READ
  BLEDescriptor bmeTemperatureCelsiusDescriptor(BLEUUID((uint16_t)0x2902));
#else
  BLECharacteristic bmeTemperatureFahrenheitCharacteristics(
    "60d5c8c3-d1b3-4ee7-bf38-3940a15dbeaa", 
    BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);  // Added PROPERTY_READ
  BLEDescriptor bmeTemperatureFahrenheitDescriptor(BLEUUID((uint16_t)0x2902));
#endif

// Server-specific Humidity Data (Uncomment for the respective server)
BLECharacteristic bmeHumidityCharacteristics(
  "4de53c9c-cde3-4cdc-948f-3ba104cc4791", 
  BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);  // Added PROPERTY_READ
BLEDescriptor bmeHumidityDescriptor(BLEUUID((uint16_t)0x2903));
//-------------------------SERVER 6 DATA END----------------------------------




// Callbacks for connect and disconnect
class MyServerCallbacks: public BLEServerCallbacks {
  void onConnect(BLEServer* pServer) {
    deviceConnected = true;
  };
  void onDisconnect(BLEServer* pServer) {
    deviceConnected = false;
    pServer->getAdvertising()->start();
    Serial.println("Advertising again");
  }
};

void setup() {
  // Start serial communication
  Serial.begin(115200);

  //// CHANGE THIS VALUE FOR EACH SERVER TO DIFFERENTIATE
  temp = 60.00;
  tempF = 60.00;
  hum = 60.00;  

  // Initialize the BLE device
  BLEDevice::init(bleServerName);

  // Create the BLE Server
  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  // Create the BLE Service
  BLEService *bmeService = pServer->createService(SERVICE_UUID);

  // Add characteristics for temperature and humidity
  #ifdef temperatureCelsius
    bmeService->addCharacteristic(&bmeTemperatureCelsiusCharacteristics);
    bmeTemperatureCelsiusDescriptor.setValue("BME temperature Celsius");
    bmeTemperatureCelsiusCharacteristics.addDescriptor(&bmeTemperatureCelsiusDescriptor);
  #else
    bmeService->addCharacteristic(&bmeTemperatureFahrenheitCharacteristics);
    bmeTemperatureFahrenheitDescriptor.setValue("BME temperature Fahrenheit");
    bmeTemperatureFahrenheitCharacteristics.addDescriptor(&bmeTemperatureFahrenheitDescriptor);
  #endif

  // Add characteristic for humidity
  bmeService->addCharacteristic(&bmeHumidityCharacteristics);
  bmeHumidityDescriptor.setValue("BME humidity");
  bmeHumidityCharacteristics.addDescriptor(new BLE2902());

  // Start the service
  bmeService->start();

  // Start advertising
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pServer->getAdvertising()->start();
  Serial.println("Waiting for a client to connect...");
}

void loop() {
  if (deviceConnected) {
    if ((millis() - lastTime) > timerDelay) {
      // Update temperature and humidity for notification
      temp += 0.1;
      tempF += 0.1;
      hum += 0.1;

      // Notify temperature reading
      #ifdef temperatureCelsius
        static char temperatureCTemp[6];
        dtostrf(temp, 6, 2, temperatureCTemp);
        bmeTemperatureCelsiusCharacteristics.setValue(temperatureCTemp);
        bmeTemperatureCelsiusCharacteristics.notify();
        Serial.print("Temperature Celsius: ");
        Serial.print(temp);
        Serial.println(" ºC");
      #else
        static char temperatureFTemp[6];
        dtostrf(tempF, 6, 2, temperatureFTemp);
        bmeTemperatureFahrenheitCharacteristics.setValue(temperatureFTemp);
        bmeTemperatureFahrenheitCharacteristics.notify();
        Serial.print("Temperature Fahrenheit: ");
        Serial.print(tempF);
        Serial.println(" ºF");
      #endif

      // Notify humidity reading
      static char humidityTemp[6];
      dtostrf(hum, 6, 2, humidityTemp);
      bmeHumidityCharacteristics.setValue(humidityTemp);
      bmeHumidityCharacteristics.notify();
      Serial.print("Humidity: ");
      Serial.print(hum);
      Serial.println(" %");

      lastTime = millis();
    }
  }
}

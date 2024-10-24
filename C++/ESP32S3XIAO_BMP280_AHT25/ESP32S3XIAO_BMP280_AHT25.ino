/*
This is example code of connecting BMP280 & AHT25 sensorsv to XIAO-ESP32-S3 using software I2C pins as hardware I2C dosent work
Author: Avtar Chodankar
Email: avtar9823@gmail.com
Github: AVTAR0901
 */

#include <Wire.h>              // Library to handle I2C communication
#include <Adafruit_Sensor.h>   // Adafruit sensor library
#include <Adafruit_BMP280.h>   // Library for BMP280 sensor
#include <Adafruit_AHTX0.h>    // Library for AHTX0 sesnor

// Create an instance of the BMP280 object
Adafruit_BMP280 bmp; // Use I2C interface
Adafruit_AHTX0 aht;  // Use I2c interface


void setup() {
  Serial.begin(115200);
  
  // Initialize I2C communication
  Wire.begin(3, 2);  // Using pins 3 (SDA) and 2 (SCL)
  //Wire.setClock(300000);

  // Start the BMP280 sensor
  if (!bmp.begin(0x76)) {  // Check for the BMP280 sensor at I2C address 0x76
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring!"));
    while (1);
  }

  // Start the AHT25 sensor
  if (! aht.begin()) {
    Serial.println("Could not find AHT? Check wiring");
    while (1) delay(10);
  }

  // Set the BMP280 settings for accuracy
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     // Operating Mode
                  Adafruit_BMP280::SAMPLING_X2,     // Temperature oversampling
                  Adafruit_BMP280::SAMPLING_X16,    // Pressure oversampling
                  Adafruit_BMP280::FILTER_X16,      // Filtering
                  Adafruit_BMP280::STANDBY_MS_500); // Standby time
}

void loop() {
  // Read temperature and pressure from the sensor
  float temperature = bmp.readTemperature();  // Get temperature in Celsius
  float pressure = bmp.readPressure();        // Get pressure in Pascals

  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);// populate temp and humidity objects with fresh data
  
  // Convert pressure from Pascals to hPa (hectopascals)
  pressure /= 100.0;

  Serial.println("|-------BMP280 & AHT25 Readings-------|");
  Serial.println(" ");

  // Display the results
  Serial.print(F("Temperature(BMP280) = "));
  Serial.print(temperature);
  Serial.println(" *C");

  Serial.print(F("Pressure(BMP280) = "));
  Serial.print(pressure);
  Serial.println(" hPa");

   Serial.println(" ");

// Data from AHT25 sensor
  Serial.print("Temperature(AHT25): "); Serial.print(temp.temperature); Serial.println(" *C");
  Serial.print("Humidity(AHT25): "); Serial.print(humidity.relative_humidity); Serial.println("% rH");
  Serial.println(" ");
  Serial.println(" ");

  // Delay before the next reading
  delay(5000);
}

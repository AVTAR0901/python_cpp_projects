"""
Description: This Script is example code to get status, signal strength,
             uptime, GPS coordinates from sim868 modules

Author: Avtar Chodankar
Github: AVTAR0901
email: avtar9823@gmail.com
"""

import RPi.GPIO as GPIO
import os
import time
import sys
import serial
from PIL import Image, ImageDraw, ImageFont, ImageOps
import adafruit_focaltouch
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import json
import PiDisplay

piDisplay = PiDisplay.PiDisplay 
class PiSimModemCallback:
    def loactionCordinates(self, x, y, z):
        pass

class PiSimModem:
    
    _callback : PiSimModemCallback
    
    def __init__(self, callback : PiSimModemCallback):
        self._callback=callback
    
    def initializeSimModem(self, image, disp, draw, i2c):
        self.image = image
        self.disp  = disp
        self.draw  = draw
        self.i2c   = i2c
        self.simOnOff()
        self.gpsModem(image, disp, draw)

    def simOnOff(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12, GPIO.OUT)
        
        GPIO.output(12, GPIO.LOW)
        time.sleep(1.2)
        GPIO.output(12, GPIO.HIGH)
        time.sleep(4)
    
    def gpsModem(self, image, disp, draw):
        piDisplay.drawRectangle(draw, 0, 0, 239, 239, "black", "black")
        disp.image(image)
        port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
        port.flush()
        #while True:
        
        piDisplay.drawRectangle(draw, 0, 0, 239, 239, "black", "black")
        port.write(str.encode('AT'+'\r'))
        rcv = port.read(20)
        print (rcv)
        time.sleep(1)
        
        
        port.write(str.encode('AT+IPR=9600'+'\r'))
        rcv = port.read(20)
        print (rcv)
        time.sleep(2)
        
        port.write(str.encode('AT+CSQ'+'\r'))
        rcj = port.read(20)
        rcjl = rcj.decode().split(",")
        rcjls = rcjl[0].split(" ")
        signalStrength = int(rcjls[1])
        print (signalStrength)
        time.sleep(1)
        
        port.write(str.encode('AT+CGPSPWR=1'+'\r'))
        rcv = port.read(20)
        print (rcv)
        time.sleep(1)
        
        port.write(str.encode('AT+CGPSSTATUS?'+'\r'))
        rcv = port.read(100)
        print (rcv)                                        # dis
        time.sleep(1)
        
        port.write(str.encode('AT+CGPSINF=0'+'\r'))
        rcg = port.read(100)
        print (rcg)
        rcgl = rcg.decode().split(",")
        gpsx = rcgl[1]
        gpsy = rcgl[2]
        gpsz = rcgl[3]
        print (gpsx)
        print (gpsy)
        print (gpsz)
        time.sleep(1)
        
        
        text = rcgl[4]
        piDisplay.drawText(draw, 5, 5, text, "white", 20, "mplus-1m-light")
        text = rcgl[1]
        piDisplay.drawText(draw, 5, 45, text, "white", 20, "mplus-1m-light")
        text = rcgl[2]
        piDisplay.drawText(draw, 5, 75, text, "white", 20, "mplus-1m-light")
        text = rcgl[3]
        piDisplay.drawText(draw, 5, 125, text, "white", 20, "mplus-1m-light")
        
        t = time.localtime()
        currentTime = time.strftime("%H:%M", t)
        print(currentTime)
        
        disp.image(image)
        
        fileObject = {
        
            "signalStrength": signalStrength,
            "Time": currentTime,
            "GpsX": gpsx,
            "GpsY": gpsy,
            "GpsZ": gpsz
            }
        
        with open("dataFile.json", "w") as dataFile:
            json.dump(fileObject, dataFile)
            print("file has been written")
    
        self.simOnOff()
        self._callback.loactionCordinates(gpsx, gpsy, gpsz)

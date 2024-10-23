import RPi.GPIO as GPIO
import time
import serial

class PiGpsModemCallback:
    def loactionCordinates(self, x, y, z):
        pass

class PiGpsModem:
    _callback: PiGpsModemCallback

    def __init__(self, callback: PiGpsModemCallback):
        self._callback = callback

    def initializeSimModem(self):
        self.simOnOff()
        self.gpsModem()

    def simOnOff(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12, GPIO.OUT)

        GPIO.output(12, GPIO.LOW)
        time.sleep(1.2)
        GPIO.output(12, GPIO.HIGH)
        time.sleep(4)

    def gpsModem(self):
        port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
        port.flush()

        port.write(str.encode('AT+CGPSPWR=1' + '\r'))
        rcv = port.read(20)
        print(rcv)
        time.sleep(1)

        port.write(str.encode('AT+CGPSINF=0' + '\r'))
        rcg = port.read(100)
        print(rcg)
        rcgl = rcg.decode().split(",")
        gpsx = rcgl[1]
        gpsy = rcgl[2]
        gpsz = rcgl[3]
        print(gpsx)
        print(gpsy)
        print(gpsz)
        time.sleep(1)

        self.simOnOff()
        self._callback.loactionCordinates(gpsx, gpsy, gpsz)
import Screen
import threading
from PIL import Image, ImageDraw, ImageFont, ImageOps
import adafruit_focaltouch
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import time

class PiTouch:
    _instance = None
    _name = "none"
    _screen : Screen
    _thread : threading.Thread
    _i2c = None

    def __init__(self):
        self._thread = threading.Thread(target=self._touchDetect, args=())
        print("Thread Created")
        self._thread.start()
        print("Thread Started")

    @staticmethod
    def addListener(name,threadCallback : Screen, i2c):
        PiTouch._name = name
        PiTouch._screen = threadCallback
        PiTouch._i2c = i2c
        if(PiTouch._instance == None):
            PiTouch._instance = PiTouch()

    def _touchDetect(self):
        ft = adafruit_focaltouch.Adafruit_FocalTouch(PiTouch._i2c, debug=False)
        while True:
            if ft.touched:
                ts = ft.touches
                point = ts[0]
                y = point["y"]
                x = point["x"]
                if(PiTouch._name != "none"):
                    #PiTouch._instance = None
                    PiTouch._name="none"
                    PiTouch._screen.handleTouch(x,y)
                    #PiTouch._screen = None
            else:
                time.sleep(.1)

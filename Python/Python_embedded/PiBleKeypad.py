import time
from evdev import InputDevice, categorize, ecodes
import threading

class PiBleKeypadCallback:
    def handleBleKeypad(self, key):
        pass

class PiBleKeypad:

    keyDict = {'A': ['a', 'A'],
               'B': ['b', 'B'],
               'C': ['c', 'C'],
               'D': ['d', 'D'],
               'E': ['e', 'E'],
               'F': ['f', 'F'],
               'G': ['g', 'G'],
               'H': ['h', 'H'],
               'I': ['i', 'I'],
               'J': ['j', 'J'],
               'K': ['k', 'K'],
               'L': ['l', 'L'],
               'M': ['m', 'M'],
               'N': ['n', 'N'],
               'O': ['o', 'O'],
               'P': ['p', 'P'],
               'Q': ['q', 'Q'],
               'R': ['r', 'R'],
               'S': ['s', 'S'],
               'T': ['t', 'T'],
               'U': ['u', 'U'],
               'V': ['v', 'V'],
               'W': ['w', 'W'],
               'X': ['x', 'X'],
               'Y': ['y', 'Y'],
               'Z': ['z', 'Z'],
               '1': ['1', '!'],
               '2': ['2', '@'],
               '3': ['3', '#'],
               '4': ['4', '$'],
               '5': ['5', '%'],
               '6': ['6', '^'],
               '7': ['7', '&'],
               '8': ['8', '*'],
               '9': ['9', '('],
               '0': ['0', ')'],
               'MINUS': ['-', '_'],
               'EQUAL': ['=', '+'],
               'BACKSLASH': ['\\', '|'],
               'LEFTBRACE': ['[', '{'],
               'RIGHTBRACE': [']', '}'],
               'APOSTROPHE': ['\'', '"'],
               'SEMICOLON': [';', ':'],
               'SLASH': ['/', '?'],
               'DOT': ['.', '>'],
               'COMMA': [',', '<'],
               'SPACE': [' ', ' '],
               'GRAVE': ['`', '~'],
               'KP0': ['0', '0'],
               'KP1': ['1', '1'],
               'KP2': ['2', '2'],
               'KP3': ['3', '3'],
               'KP4': ['4', '4'],
               'KP5': ['5', '5'],
               'KP6': ['6', '6'],
               'KP7': ['7', '7'],
               'KP8': ['8', '8'],
               'KP9': ['9', '9'],
               'KPDOT': ['.', '.'],
               'KPPLUS': ['+', '+'],
               'KPMINUS': ['-', '-'],
               'KPASTERISK': ['*', '*'],
               'KPSLASH': ['/', '/']}

    alphabetList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    digitsList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    punctuationList = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
    alphaNumericList = alphabetList + digitsList + punctuationList
    specialKeysList = ["ENTER", "TAB", "DELETE", "BACKSPACE"]

    remainingKeysList = ["TAB", "LEFTCTRL", "CAPSLOCK", "LEFTALT", "RIGHTALT", "RIGHTCTRL", "ESC", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F8", "F9", "F10", "F11", "F12", "SYSRQ", "SCROLLLOCK", "PAUSE", "HOME", "END", "INSERT", "PAGEUP", "PAGEDOWN", "DELETE", "UP", "DOWN", "LEFT", "RIGHT", "NUMLOCK"]

    allkeyList = alphabetList + digitsList + punctuationList + remainingKeysList

    keyGroupDict = {'alphabet':alphabetList,
                    'digits':digitsList,
                    'punctuation':punctuationList,
                    'alphaNumeric':alphaNumericList,
                    'specialKeys':specialKeysList,
                    'allKey':allkeyList}

    _instance = None
    _name = "none"
    _callback = None
    _isShift = False
    _isCapsLock = False
    _keyGroup = None
    _callback: PiBleKeypadCallback
    _thread: threading.Thread

    def __init__(self):
        self.dev = InputDevice('/dev/input/event0')
        print(self.dev)
        self.dev.capabilities(verbose=True)
        self._thread = threading.Thread(target=self._bleKeyDetect, args=())
        print("BlueTooth keypad Thread Created")
        self._thread.start()
        print("BlueTooth keypad Thread Started")

    @staticmethod
    def addBleKeyListener(name, keyGroup, threadCallback: PiBleKeypadCallback):
        PiBleKeypad._name = name
        PiBleKeypad._callback = threadCallback
        PiBleKeypad._keyGroup = keyGroup
        if (PiBleKeypad._instance == None):
            PiBleKeypad._instance = PiBleKeypad()

    def _bleKeyDetect(self):
        for event in self.dev.read_loop():
            if event.type == ecodes.EV_KEY:
                if(PiBleKeypad._name != "none"):
                    keyStrokStr = str((categorize(event)))
                    keyStrokStr = keyStrokStr.split(",")
                    key = keyStrokStr[1].split(" (")
                    key = key[1].split(")")
                    key = key[0].split("_")
                    key = key[1]
                    # print(key)
                    keyStatus = keyStrokStr[2].split(" ")
                    keyStatus = keyStatus[1]
                    # print(keyStatus)
                    if ("SHIFT" in key):
                        if (keyStatus == "down"):
                            print("is Shift key TRUE")
                            PiBleKeypad._isShift = True
                        elif (keyStatus == "up"):
                            print("is Shift key False")
                            PiBleKeypad._isShift = False
                    elif (key == "CAPSLOCK"):
                        if (keyStatus == "down"):
                            print("is CapsLock key Change")
                            PiBleKeypad._isCapsLock = not PiBleKeypad._isCapsLock
                    elif (keyStatus == "down"):
                        if (PiBleKeypad._isCapsLock == False and PiBleKeypad._isShift == True):
                            # Upper Case
                            print("Upper Case latter with shift")
                            if (key in self.keyDict.keys()):
                                key = self.keyDict[key][1]
                            if(key in self.keyGroupDict[self._keyGroup]):
                                PiBleKeypad._name = "none"
                                PiBleKeypad._callback.handleBleKeypad(key)
                            else:
                                print("out of group")
                        elif (PiBleKeypad._isCapsLock == True and PiBleKeypad._isShift == False):
                            # Upper Case
                            print("Upper Case latter with capslock")
                            if (key in self.keyDict.keys()):
                                key = self.keyDict[key][1]
                            if (key in self.keyGroupDict[self._keyGroup]):
                                PiBleKeypad._name = "none"
                                PiBleKeypad._callback.handleBleKeypad(key)
                            else:
                                print("out of group")
                            # PiBleKeypad._name = "none"
                            # PiBleKeypad._callback.handleBleKeypad(key)
                        else:
                            # Lowe Case
                            print("Lower Case latter")
                            if (key in self.keyDict.keys()):
                                key = self.keyDict[key][0]
                            if (key in self.keyGroupDict[self._keyGroup]):
                                PiBleKeypad._name = "none"
                                PiBleKeypad._callback.handleBleKeypad(key)
                            else:
                                print("out of group")
                            # PiBleKeypad._name = "none"
                            # PiBleKeypad._callback.handleBleKeypad(key)
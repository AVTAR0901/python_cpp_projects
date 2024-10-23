"""
Description: This script using bluetooth allows user to connect, disconnect, pair, unpair, trust, get list of available devices

Author: Avtar Chodankar
Github: AVTAR0901
email: avtar9823@gmail.com
"""


import os
import bluetooth
import time
import subprocess



class PiBluetooth:
    deviceNames = []
    deviceMacAddr = []

    def checkBTStatus(self):
        out = subprocess.Popen(['sudo', 'service', 'bluetooth', 'status'], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        out = subprocess.run(['grep', 'Active'], stdin=out.stdout, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = out.stdout.decode('utf-8')
        print(out)
        if ("inactive" in out):
            print("BlueTooth Status On")
            return "OFF"
        else:
            print("BlueTooth Status Off")
            return "ON"

    def turnONBT(self):
        os.system("sudo systemctl start bluetooth")

    def turnOFFBT(self):
        os.system("sudo systemctl stop bluetooth")

    def pairBT(self, macAddress):
        os.system('timeout 15s bluetoothctl scan on')
        pair_str = "sudo bluetoothctl pair " + str(macAddress)
        os.system(pair_str)
        time.sleep(5)

    def connectBT(self, macAddress):
        connect_str = "sudo bluetoothctl connect " + str(macAddress)
        os.system(connect_str)
        time.sleep(2)

    def trustBT(self, macAddress):
        trust_str = "sudo bluetoothctl trust " + str(macAddress)
        os.system(trust_str)
        time.sleep(2)

    def removeBT(self, macAddress):
        remove_str = "sudo bluetoothctl remove " + str(macAddress)
        os.system(remove_str)
        time.sleep(2)

    def getNearByBTList(self):
        self.deviceNames.clear()
        self.deviceMacAddr.clear()
        print("Scanning for bluetooth devices:")
        devices = bluetooth.discover_devices(lookup_names=True, lookup_class=True)
        number_of_devices = len(devices)
        print(number_of_devices, "devices found")
        for addr, name, device_class in devices:
            self.deviceNames.append(name)
            self.deviceMacAddr.append(addr)
        return self.deviceNames, self.deviceMacAddr

    def pairedDeviceList(self):
        self.deviceNames.clear()
        self.deviceMacAddr.clear()
        out = os.popen('sudo bluetoothctl paired-devices').read()
        out = out.encode("utf-8")
        out = out.decode().split("\n")
        out.pop()
        for i in out:
            x = i[:24]
            x = x.split(" ")
            self.deviceMacAddr.append(x[1])
            self.deviceNames.append(i[25:])
        return self.deviceNames, self.deviceMacAddr

"""
Description: This script allows to connect, pair, get status, get list of availbe wifi, etc

Author: Avtar Chodankar
Github: AVTAR0901
email: avtar9823@gmail.com
"""

import os
import subprocess
import time


class PiWifi:
    def getNearByWifiList(self):
        ESSIDList = []
        os.system("wifi off")
        time.sleep(1)
        os.system("wifi on")
        time.sleep(2)
        a = os.popen('iwlist wlan0 scan | grep ESSID').read()
        b = str.encode(str(a))
        b = b.decode("utf-8")
        c = b.split("\n")
        for name in c:
            if (len(name) != 0):
                x = name.split("\"")
                ESSIDList.append(x[1])
        return ESSIDList

    def connectWlan(self, wifiID, password):
        config_lines = [
            '\n',
            'network={',
            '\tssid="{}"'.format(wifiID),
            '\tpsk="{}"'.format(password),
            '\tkey_mgmt=WPA-PSK',
            '}'
        ]
        config = '\n'.join(config_lines)
        print(config)

        os.system("sudo chmod -R 777 /etc/wpa_supplicant/wpa_supplicant.conf")
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a+") as wifi:
            wifi.write(config)
            wifi.close()

        time.sleep(5)
        # os.system('sudo systemctl daemon-reload')
        # time.sleep(5)
        # os.system('sudo systemctl restart dhcpcd')
        os.system("sudo wpa_cli -i wlan0 reconfigure")
        time.sleep(10)

    def getConnectedWifiName(self):
        out = subprocess.Popen(['iwgetid'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        out = stdout.decode('utf-8')
        out = out.split("\"")
        if(len(out)>1):
            out = out[1]
            return out
        else:
            return "Not Connected"

    @staticmethod
    def configuredList():
        ESSIDConfigList = []
        out = subprocess.Popen(['cat', '/etc/wpa_supplicant/wpa_supplicant.conf'], stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        out = subprocess.run(['grep', 'ssid'], stdin=out.stdout, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = out.stdout.decode('utf-8')
        out = out.split("\n")
        for name in out:
            if (len(name) != 0):
                x = name.split("\"")
                ESSIDConfigList.append(x[1])
        return ESSIDConfigList

    def checkWifiStatus(self):
        out = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        out = stdout.decode('utf-8')
        if "wlan0" in out:
            return "ON"
        else:
            return "OFF"

    def checkSIMStatus(self):
        out = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        out = stdout.decode('utf-8')
        if "ppp0" in out:
            return "ON"
        else:
            return "OFF"

    def getIpAddress(self):
        out = subprocess.Popen(['ifconfig', 'wlan0'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        out = stdout.decode('utf-8')
        out = out.split("\n")
        if("inet" in out[1]):
            out = out[1].split("inet ")
            out = out[1].split(" ")
            return out[0]
        else:
            return "Not Connected"

    def getWifiMacAddr(self):
        p = subprocess.Popen(['cat', '/sys/class/net/wlan0/address'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        out = out.decode('utf-8')
        return out[:-1]

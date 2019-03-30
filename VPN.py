import os
import re
import random
import time
import subprocess
import sys
from requests import get

class VPN:
    def __init__(self, log):
        with open(os.devnull, 'w') as fp:
            subprocess.Popen("taskkill /f /im openvpn.exe", stdout=fp, stderr=fp, stdin=fp)
            time.sleep(1)
        self.log = log
        self.source = get('https://api.ipify.org').text
        self.remote = self.source
        self.country = ""
        self.log.info("Starting with source ip %s", self.source)

        self.vpn = ["AU Melbourne.ovpn",
        "AU Sydney.ovpn",
        "Austria.ovpn",
        "Belgium.ovpn",
        "Brazil.ovpn",
        "CA Montreal.ovpn",
        "CA Toronto.ovpn",
        "CA Vancouver.ovpn",
        "Czech Republic.ovpn",
        "DE Berlin.ovpn",
        "DE Frankfurt.ovpn",
        "Denmark.ovpn",
        "Finland.ovpn",
        "France.ovpn",
        "Hong Kong.ovpn",
        "Hungary.ovpn",
        "India.ovpn",
        "Ireland.ovpn",       
        "Israel.ovpn",
        "Italy.ovpn",
        "Japan.ovpn",
        "Luxembourg.ovpn",
        "Mexico.ovpn",  
        "Netherlands.ovpn",       
        "New Zealand.ovpn",
        "Norway.ovpn",
        "Poland.ovpn",
        "Romania.ovpn",
        "South Africa.ovpn",
        "Spain.ovpn",
        "Sweden.ovpn",
        "Switzerland.ovpn",
        "Turkey.ovpn",
        "UAE.ovpn",
        "UK London.ovpn",
        "UK Manchester.ovpn",
        "UK Southampton.ovpn"
        ]
        
        sleep_init = 2
        while self.source == self.remote:
            with open(os.devnull, 'w') as fp:
                self.log.info("Trying to connect to VPN")
                subprocess.Popen("taskkill /f /im openvpn.exe", stdout=fp, stderr=fp, stdin=fp)
                time.sleep(sleep_init)
                self.country = self.vpn[random.randint(0, len(self.vpn) - 1)]
                subprocess.Popen('openvpn --config "C:\\Program Files\\OpenVPN\\config' + '\\' + self.country, stdout=fp, stderr=fp, stdin=fp)
                time.sleep(sleep_init)
                sleep_init = sleep_init + 1
                attempts = 0
                max_attempts = 10
                while attempts < max_attempts and self.source == self.remote:
                    try:
                        self.remote = get('https://ident.me/').text
                        break
                    except Exception:
                        attempts = attempts + 1
                        time.sleep(1)
                        pass
        self.log.info("Connection to %s located in %s", self.remote, self.country)

    def disconnect(self):
        with open(os.devnull, 'w') as fp:
            self.log.info("Disconnecting from VPN")
            subprocess.Popen("taskkill /f /im openvpn.exe", stdout=fp, stderr=fp, stdin=fp)
            time.sleep(1)
        self.remote = self.source

    def reconnect(self):
        sleep_init = 2
        while self.source == self.remote:
            with open(os.devnull, 'w') as fp:
                self.log.info("Trying to connect to VPN")
                subprocess.Popen("taskkill /f /im openvpn.exe", stdout=fp, stderr=fp, stdin=fp)
                time.sleep(sleep_init)
                self.country = self.vpn[random.randint(0, len(self.vpn) - 1)]
                subprocess.Popen('openvpn --config "C:\\Program Files\\OpenVPN\\config' + '\\' + self.country, stdout=fp, stderr=fp, stdin=fp)
                time.sleep(sleep_init)
                sleep_init = sleep_init + 1
                attempts = 0
                max_attempts = 10
                while attempts < max_attempts and self.source == self.remote:
                    try:
                        self.remote = get('https://ident.me/').text
                        break
                    except Exception:
                        attempts = attempts + 1
                        time.sleep(1)
                        pass
        self.log.info("Connection to %s located in %s", self.remote, self.country)
        
    

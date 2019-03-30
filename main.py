import datetime
import json
import os
import random
import socket
import threading
import time
from datetime import datetime, timedelta
from os import popen
from pprint import pprint
from subprocess import call
from selenium import webdriver
import logging
import Bot
import God
import re
import VPN
import asyncio
import random
import time
import passgen
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.common.exceptions import (ElementNotVisibleException,
                                        NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException,
                                        UnexpectedAlertPresentException,
                                        WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

formatter = logging.Formatter("[%(asctime)s.%(msecs)03d][%(thread)d][%(levelname)s]: [%(funcName)s] %(message)s", "%Y-%m-%d %H:%M:%S")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.addLevelName(logging.DEBUG, 'debug')
logging.addLevelName(logging.INFO, 'info')
logging.addLevelName(logging.WARNING, 'warning')
logging.addLevelName(logging.WARN, 'warn')
logging.addLevelName(logging.ERROR, 'error')
logging.addLevelName(logging.CRITICAL, 'critical')
logging.addLevelName(logging.FATAL, 'fatal')
log = logging.getLogger(__name__)
log.addHandler(handler)
log.setLevel(logging.DEBUG)

command_queue = asyncio.Queue()
connection = None
vpn = VPN.VPN(log)

bots = []
if os.stat("bots.json").st_size != 0:
    with open("bots.json", "r") as data:
        [bots.append(Bot.Bot(bot['email'], bot['password'], bot['date'], bot['currency'], bot['gold'], bot['country'], bot['state'], bot['last_vpn'], vpn, log)) for bot in json.load(data)['bots']]

if len(bots) != 0:
    with open("bots.json", "w") as data:
        root = {'bots' : []}
        [root['bots'].append({ "email":bot.email, "password":bot.password, "date":bot.date, "currency":bot.currency, "gold":bot.gold, "country":bot.country,"state":bot.state,"last_vpn":bot.last_vpn }) for bot in bots]
        data.write(json.dumps(root, indent=4, sort_keys=True))

def CommandHandler(ip, port):
    log.info("Listening on %s:%s", ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)
    s.bind(server_address)
    s.listen(1)
    connection, address = s.accept()
    with connection:
        log.info("Connection of %s", address)
        while True:
            data = connection.recv(1024)
            tokenize = data.split()
            if len(tokenize) == 1:
                if tokenize[0] == b"exit":
                    command_queue.put_nowait(data)
                    break
            if len(tokenize) == 3:
                if tokenize[0] == b"bot" and tokenize[1] == b"create":
                    command_queue.put_nowait(data)
                    connection.send(b"OK")

def MainThread():
    log.info("Starting")

    deleted = True
    changed = False

    while True:

        if command_queue.empty():
            pass
        else:
            data = command_queue.get_nowait()

            tokenize = data.split()
            if len(tokenize) == 1:
                if tokenize[0] == b"exit":
                    command_queue.put_nowait(data)
                    break
            if len(tokenize) == 2:
                if tokenize[0] == b"bot" and tokenize[1] == b"start":
                    for bot in bots:
                        bot.state = "daily"

                    if deleted == True:
                        browser = webdriver.Chrome()
                        browser.get('https://www.startmail.com/signup/trial')
                        deleted = False

            if len(tokenize) == 3:
                if tokenize[0] == b"bot" and tokenize[1] == b"create":
                    if deleted == True:
                        browser = webdriver.Chrome()
                        browser.get('https://www.startmail.com/signup/trial')
                        deleted = False
  
                    god = God.God(tokenize[2].decode("utf-8"), passgen.passgen(32), bots, vpn, log)

                    if not god.create_startmail(browser):
                        log.error("Creation of startmail failed")
                        browser.delete_all_cookies() 
                        browser.quit()
                        del browser
                        deleted = True
                        continue

                    if not god.create_vivaldi(browser):
                        log.error("Creation of vivaldi failed")
                        browser.delete_all_cookies() 
                        browser.quit()
                        del browser
                        deleted = True
                        continue

                    if not god.validate_vivaldi(browser):
                        log.error("Validation for vivaldi failed")
                        browser.delete_all_cookies() 
                        browser.quit()
                        del browser
                        deleted = True
                        continue

                    if not god.create_erepublik(browser):
                        log.error("Creation of erepublik failed")
                        browser.delete_all_cookies() 
                        browser.quit()
                        del browser
                        deleted = True
                        continue

                    if not god.validate_erepublik(browser):
                        log.error("Validation for erepublik failed")
                        browser.delete_all_cookies() 
                        browser.quit()
                        del browser
                        deleted = True
                        continue

                    if not god.initialize(browser):
                        log.error("Initialization failed")
                        browser.delete_all_cookies() 
                        browser.quit()
                        del browser
                        deleted = True
                        continue

                    if not god.finalize(browser):
                        connection.send(b"Finalization failed")
                        browser.delete_all_cookies() 
                        browser.quit()
                        del browser
                        deleted = True
                        continue
                    
                    deleted = True

        for bot in bots:
            if bot.date != "":
                now_time = datetime.now()
                bot_time = datetime.strptime(bot.date, "%Y-%m-%d %H:%M:%S")
                diff = now_time - bot_time
                if diff.days >= 1:
                    bot.change_state("daily")

            if bot.state != "idle" and bot.state != "invalid":
                log.info("Doing %s", bot.email)

                vpn.disconnect()
                vpn.reconnect()

                bot.last_vpn = vpn.remote

                if deleted == True:
                    browser = webdriver.Chrome()
                    browser.get('https://www.erepublik.com/en')
                    deleted = False
                
                if not bot.connect(browser):
                    browser.quit()
                    del browser
                    deleted = True
                    bot.change_state("invalid")
                    bot.update_time()
                    continue

                bot.home(browser)
                bot.buy(browser)
                bot.work(browser)
                bot.produce(browser)
                bot.train(browser)
                bot.fight(browser)
                bot.change_currency(browser)
                bot.home(browser)         
                bot.get_status(browser)
                bot.change_state("idle")
                bot.update_time()
                
                with open("bots.json", "w") as data:
                    root = {'bots' : []}
                    [root['bots'].append({ "email":bot.email, "password":bot.password, "date":bot.date, "currency":bot.currency, "gold":bot.gold, "country":bot.country, "state":bot.state,"last_vpn":bot.last_vpn }) for bot in bots]
                    data.write(json.dumps(root, indent=4, sort_keys=True))

            if deleted != True:
                browser.delete_all_cookies()
                browser.quit()
                del browser
                deleted = True
            


thread1 = threading.Thread(target=CommandHandler, args=('127.0.0.1', 10000))
thread2 = threading.Thread(target=MainThread)
thread1.start()
thread2.start()
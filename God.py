import random
import time
from io import BytesIO
from random import randint
import Bot
import requests
import urllib3
from PIL import Image
from python_anticaptcha import (AnticaptchaClient, ImageToTextTask,
                                NoCaptchaTaskProxylessTask)
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

class God:
    def __init__(self, username, password, bots, vpn, log):
        self.username = username
        self.password = password
        self.startmail_mail = ''
        self.vivaldi_mail = ''
        self.startmail_window = ''
        self.vivaldi_window = ''
        self.erepublik_window = ''

        i = (randint(0, 4))

        self.country = ["Serbia", "Romania", "Egypt", "Indonesia", "Brazil"][i]
        self.country_id = ["65", "1", "165", "49", "9"][i]
        self.api = "" #recaptcha
        self.site = 'https://www.erepublik.com/en'
        self.key = "6Lf490AUAAAAAIqP0H7DFfXF5tva00u93wxAQ--h"

        self.bots = bots
        self.vpn = vpn
        self.log = log
        print("God has created a bot with " + self.username + " and " + self.password)

    def create_startmail(self, browser):
        self.log.info("Creating startmail account")
        browser.get('https://www.startmail.com/signup/trial')

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="field-email"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="field-email"]'))) 
            textbox = browser.find_element_by_xpath('//input[@id="field-email"]')
            textbox.send_keys(self.username)
        except TimeoutException:
            self.log.error("Failed to create startmail account")
            return False

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="field-password"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="field-password"]'))) 
            textbox = browser.find_element_by_xpath('//input[@id="field-password"]')
            textbox.send_keys(self.password)
        except TimeoutException:
            self.log.error("Failed to create startmail account")
            return False

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="field-confirm-password"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="field-confirm-password"]'))) 
            textbox = browser.find_element_by_xpath('//input[@id="field-confirm-password"]')
            textbox.send_keys(self.password)
        except TimeoutException:
            self.log.error("Failed to create startmail account")
            return False

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="field-terms-agree"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="field-terms-agree"]'))) 
            checkbox = browser.find_element_by_xpath('//input[@id="field-terms-agree"]')
            checkbox.click()
        except TimeoutException:
            self.log.error("Failed to create startmail account")
            return False

        retry = True

        while retry:
            try:
                WebDriverWait(browser, 3).until(
                    expected_conditions.presence_of_element_located((By.XPATH, '//img[@id="captcha"]')))
                WebDriverWait(browser, 3).until(
                    expected_conditions.visibility_of_element_located((By.XPATH, '//img[@id="captcha"]'))) 
                element = browser.find_element_by_xpath('//img[@id="captcha"]')
            except TimeoutException:
                self.log.error("Failed to create startmail account")
                return False

            location = element.location
            size = element.size
            png = browser.get_screenshot_as_png()

            im = Image.open(BytesIO(png))

            left = location['x'] - 120
            top = location['y'] - 120
            right = location['x'] + size['width'] + 120
            bottom = location['y'] + size['height'] + 120

            im = im.crop((left, top, right, bottom))
            im.save('captcha.png')

            captcha_fp = open("captcha.png", 'rb')
            client = AnticaptchaClient(self.api)
            task = ImageToTextTask(captcha_fp)
            job = client.createTask(task)
            job.join()

            try:
                WebDriverWait(browser, 3).until(
                    expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="field-captcha"]')))
                WebDriverWait(browser, 3).until(
                    expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="field-captcha"]'))) 
                textbox = browser.find_element_by_xpath('//input[@id="field-captcha"]')
                textbox.send_keys(job.get_captcha_text())
            except TimeoutException:
                self.log.error("Failed to create startmail account")
                return False

            try:
                WebDriverWait(browser, 3).until(
                    expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="btn-register"]')))
                WebDriverWait(browser, 3).until(
                    expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="btn-register"]'))) 
                button = browser.find_element_by_xpath('//input[@id="btn-register"]')
                button.click()
            except TimeoutException:
                self.log.error("Failed to create startmail account")  
                return False

            try:
                WebDriverWait(browser, 15).until(
                    expected_conditions.presence_of_element_located((By.XPATH, '//p[@class="trial-username"]/span/strong')))
                WebDriverWait(browser, 15).until(
                    expected_conditions.visibility_of_element_located((By.XPATH, '//p[@class="trial-username"]/span/strong'))) 
                text = browser.find_element_by_xpath('//p[@class="trial-username"]/span/strong')
                self.startmail_mail = text.text
                retry = False
            except TimeoutException:
                job.report_incorrect()
                self.log.error("Failed to process captcha. Retrying...")    

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//button[@id="upgrade-complete-btn"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//button[@id="upgrade-complete-btn"]'))) 
            button = browser.find_element_by_xpath('//button[@id="upgrade-complete-btn"]')
            button.click()
        except TimeoutException:
            self.log.error("Failed to create startmail account")
            return False

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@class="button green btn btn-success"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//input[@class="button green btn btn-success"]'))) 
            button = browser.find_element_by_xpath('//input[@class="button green btn btn-success"]')
            button.click()
        except TimeoutException:
            self.log.error("Failed to create startmail account")
            return False

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="field-password"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="field-password"]'))) 
            textbox = browser.find_element_by_xpath('//input[@id="field-password"]')
            textbox.send_keys(self.password)
        except TimeoutException:
            self.log.error("Failed to create startmail account")
            return False

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@class="button green btn btn-success"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//input[@class="button green btn btn-success"]'))) 
            button = browser.find_element_by_xpath('//input[@class="button green btn btn-success"]')
            button.click()
        except TimeoutException:
            self.log.error("Failed to create startmail account")
            return False

        browser.get('https://www.startmail.com/mailbox')

        self.startmail = browser.current_window_handle
        browser.execute_script("window.open('about:blank','_blank');")
        WebDriverWait(browser, 10).until(expected_conditions.number_of_windows_to_be(2))
        windows = browser.window_handles
        self.vivaldi = [x for x in windows if x != self.startmail][0]
        browser.switch_to_window(self.vivaldi)
        browser.get("https://vivaldi.net/")
        browser.get("https://login.vivaldi.net/profile/id/signup")

        return True

    def create_vivaldi(self, browser):
        self.log.info("Creating vivaldi account")
        try:
            WebDriverWait(browser, 5).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="username"]')))
            WebDriverWait(browser, 5).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="username"]'))) 
            textbox = browser.find_element_by_xpath('//input[@id="username"]')
            textbox.send_keys(self.username)
        except TimeoutException:
            self.log.error("Failed to create vivaldi account")
            return False

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="password"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="password"]'))) 
            textbox = browser.find_element_by_xpath('//input[@id="password"]')
            textbox.send_keys(self.password)
        except TimeoutException:
            self.log.error("Failed to create vivaldi account")
            return False

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="email"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="email"]'))) 
            textbox = browser.find_element_by_xpath('//input[@id="email"]')
            textbox.send_keys(self.startmail_mail)
        except TimeoutException:
            self.log.error("Failed to create vivaldi account")
            return False

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="name"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="name"]'))) 
            textbox = browser.find_element_by_xpath('//input[@id="name"]')
            textbox.send_keys(self.username)
        except TimeoutException:
            self.log.error("Failed to create vivaldi account")
            return False

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//select[@id="day"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//select[@id="day"]'))) 
            selectbox = browser.find_element_by_xpath('//select[@id="day"]')
            selectbox.click()
            selectbox.send_keys(Keys.DOWN)
            selectbox.send_keys(Keys.ENTER)
        except TimeoutException:
            self.log.error("Failed to create vivaldi account")
            return False

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//select[@id="month"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//select[@id="month"]'))) 
            selectbox = browser.find_element_by_xpath('//select[@id="month"]')
            selectbox.click()
            selectbox.send_keys(Keys.DOWN)
            selectbox.send_keys(Keys.ENTER)
        except TimeoutException:
            self.log.error("Failed to create vivaldi account")
            return False

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//select[@id="year"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//select[@id="year"]'))) 
            selectbox = browser.find_element_by_xpath('//select[@id="year"]')
            selectbox.click()
            selectbox.send_keys("1")
            selectbox.send_keys(Keys.ENTER)
        except TimeoutException:
            self.log.error("Failed to create vivaldi account")
            return False

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//span[@id="captcha1"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//span[@id="captcha1"]'))) 
            text = browser.find_element_by_xpath('//span[@id="captcha1"]')
            captcha1 = int(text.text)
        except TimeoutException:
            self.log.error("Failed to create vivaldi account")
            return False

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//span[@id="captcha2"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//span[@id="captcha2"]'))) 
            text = browser.find_element_by_xpath('//span[@id="captcha2"]')
            captcha2 = int(text.text)
        except TimeoutException:
            self.log.error("Failed to create vivaldi account")
            return False

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="captchaAnswer"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="captchaAnswer"]')))
            textbox = browser.find_element_by_xpath('//input[@id="captchaAnswer"]')
            textbox.send_keys(captcha1 + captcha2)
        except TimeoutException:
            self.log.error("Failed to create vivaldi account")
            return False

        ActionChains(browser).send_keys(Keys.TAB).perform()
        ActionChains(browser).send_keys(Keys.SPACE).perform()
        ActionChains(browser).send_keys(Keys.TAB).perform()
        ActionChains(browser).send_keys(Keys.TAB).perform()
        ActionChains(browser).send_keys(Keys.SPACE).perform()
        ActionChains(browser).send_keys(Keys.TAB).perform()
        ActionChains(browser).send_keys(Keys.TAB).perform()
        ActionChains(browser).send_keys(Keys.TAB).perform()
        ActionChains(browser).send_keys(Keys.ENTER).perform()

        browser.close()
        browser.switch_to.window(self.startmail_window)

        self.vivaldi_mail = self.username + "@vivaldi.net"

        return True

    def validate_vivaldi(self, browser):
        self.log.info("Validating vivaldi account")
        waiting = True
        while waiting:
            try:
                WebDriverWait(browser, 5).until(
                    expected_conditions.presence_of_element_located((By.XPATH, '//span[@title="no-reply@vivaldi.com"]')))
                WebDriverWait(browser, 5).until(
                    expected_conditions.visibility_of_element_located((By.XPATH, '//span[@title="no-reply@vivaldi.com"]')))
                button = browser.find_element_by_xpath('//span[@title="no-reply@vivaldi.com"]')
                button.click()
                waiting = False
            except TimeoutException:
                browser.refresh()
                time.sleep(5)
                self.log.info("Refreshing to get vivaldi validation email...")

        try:
            WebDriverWait(browser, 5).until(
                expected_conditions.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'https://login.vivaldi.net/profile')))
            WebDriverWait(browser, 5).until(
                expected_conditions.visibility_of_element_located((By.PARTIAL_LINK_TEXT, 'https://login.vivaldi.net/profile')))
            button = browser.find_element_by_partial_link_text('https://login.vivaldi.net/profile')
            button.click()
        except TimeoutException:
            self.log.error("Failed to validate vivaldi account")
            return False

        try:
            WebDriverWait(browser, 5).until(
                expected_conditions.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'https://login.vivaldi.net/profile/confirmReg?confirmation')))
            WebDriverWait(browser, 5).until(
                expected_conditions.visibility_of_element_located((By.PARTIAL_LINK_TEXT, 'https://login.vivaldi.net/profile/confirmReg?confirmation')))
            element = browser.find_element_by_partial_link_text('https://login.vivaldi.net/profile/confirmReg?confirmation')
            self.vpn.disconnect()
            browser.get(element.text)
            self.vpn.reconnect()
        except TimeoutException:
            self.log.error("Failed to validate vivaldi account")
            return False

        browser.get("https://imap.vivaldi.net/webmail/")
        attempts = 0
        max_attempts = 10
        while attempts < max_attempts:
            try:
                browser.refresh()
                WebDriverWait(browser, 3).until(
                    expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="rcmloginuser"]')))
                WebDriverWait(browser, 3).until(
                    expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="rcmloginuser"]')))
                textbox = browser.find_element_by_xpath('//input[@id="rcmloginuser"]')
                textbox.send_keys(self.username)
                break
            except TimeoutException:
                self.log.info("Failed to validate vivaldi account. Retrying...")
                browser.refresh()
                attempts = attempts + 1
                pass

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="rcmloginpwd"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="rcmloginpwd"]')))
            textbox = browser.find_element_by_xpath('//input[@id="rcmloginpwd"]')
            textbox.send_keys(self.password)
        except TimeoutException:
            self.log.error("Failed to validate vivaldi account")
            return False
        
        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="rcmloginsubmit"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="rcmloginsubmit"]')))
            button = browser.find_element_by_xpath('//input[@id="rcmloginsubmit"]')
            button.click()
        except TimeoutException:
            self.log.error("Failed to validate vivaldi account")
            return False

        return True

    def create_erepublik(self, browser):
        self.log.info("Creating erepublik account")
        self.vivaldi = browser.current_window_handle
        browser.execute_script("window.open('about:blank','_blank');")
        WebDriverWait(browser, 10).until(expected_conditions.number_of_windows_to_be(2))
        windows = browser.window_handles
        self.erepublik_window = [x for x in windows if x != self.vivaldi][0]
        browser.switch_to_window(self.erepublik_window)
        browser.get("https://www.erepublik.com/en")

        attempts = 0
        max_attempts = 10
        while attempts < max_attempts:
            try:
                WebDriverWait(browser, 5).until(
                    expected_conditions.presence_of_element_located((By.XPATH, '//a[@class="sign_up register_button"]')))
                WebDriverWait(browser, 5).until(
                    expected_conditions.visibility_of_element_located((By.XPATH, '//a[@class="sign_up register_button"]')))
                button = browser.find_element_by_xpath('//a[@class="sign_up register_button"]')
                button.click()
                break
            except TimeoutException:
                self.log.info("Failed to validate vivaldi account. Retrying...")
                browser.refresh()
                attempts = attempts + 1
                pass
        
        try:
            WebDriverWait(browser, 5).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="register_name"]')))
            WebDriverWait(browser, 5).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="register_name"]')))
            textbox = browser.find_element_by_xpath('//input[@id="register_name"]')
            textbox.send_keys(self.username)
        except TimeoutException:
            self.log.error("Failed to create erepublik account")
            return False

        ActionChains(browser).send_keys(Keys.TAB).perform()
        ActionChains(browser).send_keys(self.country).perform()
        ActionChains(browser).send_keys(Keys.ENTER).perform()

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="register_email"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="register_email"]')))
            textbox = browser.find_element_by_xpath('//input[@id="register_email"]')
            textbox.send_keys(self.vivaldi_mail)
        except TimeoutException:
            self.log.error("Failed to create erepublik account")
            return False

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="register_password"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="register_password"]')))
            textbox = browser.find_element_by_xpath('//input[@id="register_password"]')
            textbox.send_keys(self.password)
        except TimeoutException:
            self.log.error("Failed to create erepublik account")
            return False
        
        ActionChains(browser).send_keys(Keys.TAB).perform()
        ActionChains(browser).send_keys(Keys.TAB).perform()
        ActionChains(browser).send_keys(Keys.TAB).perform()
        ActionChains(browser).send_keys(Keys.TAB).perform()
        ActionChains(browser).send_keys(Keys.SPACE).perform()

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//button[@class="next btn btn-info pull-right dirty_green"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//button[@class="next btn btn-info pull-right dirty_green"]')))
            button = browser.find_element_by_xpath('//button[@class="next btn btn-info pull-right dirty_green"]')
            button.click()
        except TimeoutException:
            self.log.error("Failed to create erepublik account")
            return False

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="_token"]')))
            text = browser.find_element_by_xpath('//input[@id="_token"]')
            token = text.get_attribute('value')
        except TimeoutException:
            self.log.error("Failed to create erepublik account")
            return False

        response1 = ""
        response2 = ""

        while True:
            try:
                self.log.info("Starting recaptcha process")

                client = AnticaptchaClient(self.api)
                task = NoCaptchaTaskProxylessTask(self.site, self.key)
                job = client.createTask(task)
                job.join()
                captcha_token = job.get_solution_response()

                with requests.Session() as session:

                    headers = {
                    'authority': 'www.erepublik.com',
                    'method': 'GET',
                    'path': '/en/main/register-validate/captcha/?registerCaptchaToken=' + captcha_token,
                    'scheme': 'https',
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
                    'cookie': '__cfduid=db61e737f8762e6becd3c698aa65688aa1542547999; erpk_plang=en; erpk_auth=1; erpk_mid=109d3e691d173a8a73a13280fa6f0d4e; l_chatroom=Njk6ZDQxZDhjZDk4ZjAwYjIwNGU5ODAwOTk4ZWNmODQyN2U6Um5WbGNucGhjeUJCY20xaFpHRnpJRVp2Y205amIyTm9aWEpoY3c9PQ%3D%3D; invite_friends_pop_counter=0; erpk=72uhg06jv0qf62dp62r76j70j4; _b711c7ff820789c20ca210c4f04d34b8=YjcxMWM3ZmY4MjA3ODljMjBjYTIxMGM0ZjA0ZDM0Yjg%3D',
                    'dnt': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 OPR/56.0.3051.104',
                    'x-requested-with': 'XMLHttpRequest',
                    }

                    response1 = session.get('https://www.erepublik.com/en/main/register-validate/captcha/?registerCaptchaToken=' + captcha_token, headers=headers)

                    self.log.info("First response is: %s", response1.text)

                    headers = {
                        'authority': 'www.erepublik.com',
                        'method': 'POST',
                        'path': '/en/main/register-new-email',
                        'accept': 'application/json, text/javascript, */*; q=0.01',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
                        'content-length': '441',
                        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'cookie': '__cfduid=db61e737f8762e6becd3c698aa65688aa1542547999; erpk_plang=en; erpk_auth=1; erpk_mid=109d3e691d173a8a73a13280fa6f0d4e; l_chatroom=Njk6ZDQxZDhjZDk4ZjAwYjIwNGU5ODAwOTk4ZWNmODQyN2U6Um5WbGNucGhjeUJCY20xaFpHRnpJRVp2Y205amIyTm9aWEpoY3c9PQ%3D%3D; invite_friends_pop_counter=0; erpk=72uhg06jv0qf62dp62r76j70j4; _b711c7ff820789c20ca210c4f04d34b8=YjcxMWM3ZmY4MjA3ODljMjBjYTIxMGM0ZjA0ZDM0Yjg%3D',
                        'dnt': '1',
                        'origin':'https://www.erepublik.com',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 OPR/56.0.3051.104',
                        'x-requested-with': 'XMLHttpRequest',
                        'scheme': 'https',
                    }

                    payload = {
                        'name': self.username,
                        'countryId': str(self.country_id),
                        'email': self.vivaldi_mail,
                        'password': self.password,
                        'referrer':'',
                        '_token': token,
                        'registerCaptchaToken':captcha_token,
                    }

                    response2 = session.post('https://www.erepublik.com/en/main/register-new-email', headers=headers, data=payload)

                    self.log.info("Second response is: %s", response2.text)
                    
                    if response1.text == '{"error":true,"message":"Incorrect captcha"}' or response2.text == '{"has_error":true,"error":"captcha"}':
                        job.report_incorrect()
                        self.log.info("Failed to process captcha. Retrying...")
                    else:
                        break
            except Exception:
                self.log.info("Exception happened... Restarting...")
                pass

        browser.close()
        browser.switch_to_window(self.vivaldi_window)

        return True

    def validate_erepublik(self, browser):
        self.log.info("Validating erepublik account")

        attempts = 0
        max_attempts = 10
        while attempts < max_attempts:
            try:
                WebDriverWait(browser, 3).until(
                    expected_conditions.presence_of_element_located((By.LINK_TEXT, 'eRepublik registration email')))
                WebDriverWait(browser, 3).until(
                    expected_conditions.visibility_of_element_located((By.LINK_TEXT, 'eRepublik registration email')))
                button = browser.find_element_by_link_text('eRepublik registration email')
                button.click()
                break
            except TimeoutException:
                self.log.info("Refreshing to get erepublik validation email...")
                browser.refresh()
                attempts = attempts + 1
                pass
                
            
        iframe = browser.find_elements_by_tag_name('iframe')[0]
        browser.switch_to_frame(iframe)

        try:
            WebDriverWait(browser, 5).until(
                expected_conditions.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'www.erepublik.com/en/register-validate')))
            WebDriverWait(browser, 5).until(
                expected_conditions.visibility_of_element_located((By.PARTIAL_LINK_TEXT, 'www.erepublik.com/en/register-validate')))
            text = browser.find_element_by_partial_link_text('www.erepublik.com/en/register-validate')
            url = text.text[text.text.find("www"):]
        except TimeoutException:
            self.log.error("Could not click erepublik validation email...")
            return False

        self.vivaldi = browser.current_window_handle
        browser.execute_script("window.open('about:blank','_blank');")
        WebDriverWait(browser, 10).until(expected_conditions.number_of_windows_to_be(2))
        windows = browser.window_handles
        self.erepublik_window = [x for x in windows if x != self.vivaldi][0]
        browser.switch_to_window(self.erepublik_window)
        browser.get("https://" + url)

        return True

    def initialize(self, browser):
        self.log.info("Initializing bot")

        browser.refresh()

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//img[@class="avatar"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//img[@class="avatar"]')))
            buttons = browser.find_elements_by_xpath('//img[@class="avatar"]')
            random.shuffle(buttons)
            buttons.pop().click()
        except TimeoutException:
            self.log.error("Failed to join military rank")
            return False

        try:
            WebDriverWait(browser, 3).until(expected_conditions.presence_of_element_located(
            (By.PARTIAL_LINK_TEXT, 'Join and Continue')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.PARTIAL_LINK_TEXT, 'Join and Continue')))
            button = browser.find_element_by_partial_link_text('Join and Continue')
            button.click()
        except TimeoutException:
            self.log.error("Failed to join military rank")
            return False
        
        browser.get('https://www.erepublik.com/en/main/messages-inbox')

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="select_all"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="select_all"]')))
            button = browser.find_element_by_xpath('//input[@id="select_all"]')
            button.click()
        except TimeoutException:
            self.log.error("Failed to delete messages")
            return False

        try:
            WebDriverWait(browser, 3).until(expected_conditions.presence_of_element_located(
            (By.LINK_TEXT, 'Delete')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.LINK_TEXT, 'Delete')))
            button = browser.find_element_by_link_text('Delete')
            button.click()
        except TimeoutException:
            self.log.error("Failed to delete messages")
            return False

        try:
            WebDriverWait(browser, 3).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//a[@id="confirmAlert"]')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//a[@id="confirmAlert"]')))
            button = browser.find_element_by_xpath('//a[@id="confirmAlert"]')
            button.click()
        except TimeoutException:
            self.log.error("Failed to delete messages")
            return False

        browser.get('https://www.erepublik.com/en/main/citizen-edit/edit_account_settings')

        try:
            WebDriverWait(browser, 3).until(expected_conditions.presence_of_element_located(
            (By.LINK_TEXT, 'Edit')))
            WebDriverWait(browser, 3).until(
                expected_conditions.visibility_of_element_located((By.LINK_TEXT, 'Edit')))
            buttons = browser.find_elements_by_link_text('Edit')
            buttons.pop().click()
            browser.switch_to_active_element().send_keys(Keys.CONTROL + "a")
            browser.switch_to_active_element().send_keys(Keys.DELETE)
            browser.switch_to_active_element().send_keys(self.username + "@gmail.com")
            browser.switch_to_active_element().send_keys(Keys.ENTER)
            time.sleep(2)
        except TimeoutException:
            self.log.error("Failed to change email account")
            return False

        try:
            WebDriverWait(browser, 5).until(
                expected_conditions.presence_of_element_located(
            (By.PARTIAL_LINK_TEXT, 'Change email')))
            WebDriverWait(browser, 5).until(
                expected_conditions.visibility_of_element_located((By.PARTIAL_LINK_TEXT, 'Change email')))
            button = browser.find_element_by_partial_link_text('Change email')
            button.click()
            time.sleep(2)
        except TimeoutException:
            self.log.error("Failed to change email account")
            return False

        browser.close()
        browser.switch_to_window(self.vivaldi_window)

        waiting = True
        while waiting:
            try:
                WebDriverWait(browser, 3).until(
                    expected_conditions.presence_of_element_located((By.LINK_TEXT, 'Change your email request')))
                WebDriverWait(browser, 3).until(
                    expected_conditions.visibility_of_element_located((By.LINK_TEXT, 'Change your email request')))
                button = browser.find_element_by_link_text('Change your email request')
                button.click()
                waiting = False
            except TimeoutException:
                browser.refresh()
                time.sleep(5)
                self.log.info("Refreshing to get erepublik change email validation email...")

        iframe = browser.find_elements_by_tag_name('iframe')[0]
        browser.switch_to_frame(iframe)

        try:
            WebDriverWait(browser, 5).until(
                expected_conditions.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'www.erepublik.com/en/citizen/email-validate')))
            WebDriverWait(browser, 5).until(
                expected_conditions.visibility_of_element_located((By.PARTIAL_LINK_TEXT, 'www.erepublik.com/en/citizen/email-validate')))
            text = browser.find_element_by_partial_link_text('www.erepublik.com/en/citizen/email-validate')
            url = text.text[text.text.find("www"):]
        except TimeoutException:
            self.log.error("Failed to get erepublik change email validation email")
            return False

        self.vivaldi = browser.current_window_handle
        browser.execute_script("window.open('about:blank','_blank');")
        WebDriverWait(browser, 10).until(expected_conditions.number_of_windows_to_be(2))
        windows = browser.window_handles
        self.erepublik_window = [x for x in windows if x != self.vivaldi][0]
        browser.switch_to_window(self.erepublik_window)
        browser.get("https://" + url)

        return True
    
    def finalize(self, browser):
        self.log.info("Finalizing bot")
        browser.quit()
        self.bots.append(Bot.Bot(self.username + "@gmail.com", self.password, "", "", "", self.country, "daily", self.vpn.remote, self.vpn, self.log))

        return True

import datetime
import os
import random
import time
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.common.exceptions import (ElementNotVisibleException,
                                        NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException,
                                        UnexpectedAlertPresentException,
                                        WebDriverException)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import VPN

class Bot:
    def __init__(self, email, password, date, currency, gold, country, state, last_vpn, vpn, log):
        self.email = email
        self.password = password
        self.date = date
        self.currency = currency
        self.gold = gold
        self.country = country
        self.state = state
        self.last_vpn = vpn.remote
        self.vpn = vpn

        self.log = log

        self.worked = False
        self.trained = False
        self.produced = False
        self.fought = False

    def connect(self, browser):
        self.log.info("Connecting of %s", self.email)
        max_attempts = 5
        attempts = 0
        while attempts < max_attempts:
            browser.get('https://www.erepublik.com/en')

            try:
                WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                    (By.NAME, 'citizen_email')))
                WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                    (By.NAME, 'citizen_email')))
                textbox = browser.find_element_by_name('citizen_email')
                textbox.send_keys(self.email)
            except TimeoutException:
                self.log.info("Failed to load page for %s", self.email)
                attempts = attempts + 1
                continue

            try:
                WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                    (By.NAME, 'citizen_password')))
                WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                    (By.NAME, 'citizen_password')))
                textbox = browser.find_element_by_name('citizen_password')
                textbox.send_keys(self.password)
            except TimeoutException:
                self.log.info("Failed to connect for %s", self.email)
                return False

            try:
                WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                    (By.XPATH, "//button[@type='submit']")))
                WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                    (By.XPATH, "//button[@type='submit']")))  
                button = browser.find_element_by_xpath("//button[@type='submit']")
                button.send_keys(Keys.RETURN)
            except TimeoutException:
                self.log.info("Failed to connect for %s", self.email)
                return False

            try:
                WebDriverWait(browser, 2).until(EC.presence_of_element_located(
                    (By.PARTIAL_LINK_TEXT, 'Buy now!')))
                break
            except TimeoutException:
                try:
                    WebDriverWait(browser, 2).until(EC.presence_of_element_located(
                        (By.PARTIAL_LINK_TEXT, 'Recover Energy')))
                    break
                except TimeoutException:
                    try:
                        WebDriverWait(browser, 2).until(EC.presence_of_element_located(
                            (By.PARTIAL_LINK_TEXT, 'Energy Bar')))
                        break
                    except TimeoutException:
                        try:
                            WebDriverWait(browser, 2).until(EC.presence_of_element_located(
                                (By.PARTIAL_LINK_TEXT, 'Buy food')))
                            break
                        except TimeoutException:
                            browser.delete_all_cookies()

                            self.vpn.reconnect()

                            self.last_vpn = self.vpn.remote

                            attempts = attempts + 1
                            continue

        if attempts == max_attempts:
            return False
        
        try:
            WebDriverWait(browser, 2).until(EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Get all rewards")]')))
            WebDriverWait(browser, 2).until(EC.visibility_of_element_located(
                (By.XPATH, '//span[contains(text(), "Get all rewards")]')))
            button = browser.find_element_by_xpath('//span[contains(text(), "Get all rewards")]')
            button.click()
            time.sleep(1)
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "mission_link")))
            buttons = browser.find_elements_by_class_name("mission_link")
            for button in buttons:
                button.click()
                try:
                    WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                        (By.XPATH, '//span[contains(text(), "Ok")]')))
                    WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                        (By.XPATH, '//span[contains(text(), "Ok")]')))    
                    button = browser.find_element_by_xpath('//span[contains(text(), "Ok")]')
                    button.click()
                    time.sleep(3)
                except TimeoutException:
                    try:
                        WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                            (By.LINK_TEXT, "X")))
                        WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                            (By.LINK_TEXT, "X")))     
                        button = browser.find_element_by_link_text("X")
                        button.click()
                        time.sleep(3)
                    except TimeoutException:
                        pass
        except TimeoutException:
            pass    

        return True

    def change_state(self, state):
        self.state = state

    def home(self, browser):
        self.log.info("Going to residence for %s", self.email)
        browser.get('https://www.erepublik.com/en/main/myResidence')

        try:
            WebDriverWait(browser, 5).until(EC.presence_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Buy now!')))
            WebDriverWait(browser, 5).until(EC.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Buy now!')))
            browser.get('https://www.erepublik.com/en/economy/myResidence')
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.XPATH, '//a[@class="std_global_btn blueColor smallSize cta nextBtn"]')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.XPATH, '//a[@class="std_global_btn blueColor smallSize cta nextBtn"]')))

            button = browser.find_element_by_xpath('//a[@class="std_global_btn blueColor smallSize cta nextBtn"]')
            button.send_keys(Keys.RETURN)
            button.send_keys(Keys.RETURN)
            button.send_keys(Keys.RETURN)
            button.send_keys(Keys.RETURN)
            button.send_keys(Keys.RETURN)
            button.send_keys(Keys.RETURN)
            button.send_keys(Keys.RETURN)
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.XPATH, '//a[@class="std_global_btn greenColor smallSize cta endBtn"]')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.XPATH, '//a[@class="std_global_btn greenColor smallSize cta endBtn"]')))
            button = browser.find_element_by_xpath('//a[@class="std_global_btn greenColor smallSize cta endBtn"]')
            button.send_keys(Keys.RETURN)
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.LINK_TEXT, 'Become a resident')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, 'Become a resident')))
            button = browser.find_element_by_link_text('Become a resident')
            button.send_keys(Keys.RETURN)
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.LINK_TEXT, 'Yes')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, 'Yes')))
            button = browser.find_element_by_link_text('Yes')
            button.send_keys(Keys.RETURN)
        except TimeoutException:
            pass
        
        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Travel to city')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Travel to city')))
            button = browser.find_element_by_partial_link_text('Travel to city')
            button.click()
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Move to location')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Move to location')))
            button = browser.find_element_by_partial_link_text('Move to location')
            button.click()
        except TimeoutException:
            pass
        return True

    def buy(self, browser):
        self.log.info("Buying food for %s", self.email)
        browser.get('https://www.erepublik.com/en/economy/inventory')

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Buy now!')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Buy now!')))
            browser.get('https://www.erepublik.com/en/economy/inventory')
        except TimeoutException:
            pass

        exists = False
        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.ID, 'stock_1_1')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.ID, 'stock_1_1')))
            stock_1_1 = browser.find_element_by_id('stock_1_1')
            exists = True
        except TimeoutException:
            pass
        
        if not exists or float(stock_1_1.text.replace(',', '')) < 400:
            browser.get('https://www.erepublik.com/en/economy/marketplace#15/1/1')

            try:
                WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="country-select"]')))
                WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                    (By.XPATH, '//div[@class="country-select"]')))
                dropdown = browser.find_element_by_xpath('//div[@class="country-select"]')
                dropdown.click()

                ActionChains(browser).send_keys(self.country).perform()
                ActionChains(browser).send_keys(Keys.ENTER).perform()
            except TimeoutException:
                self.log.info("Failed to buy for %s", self.email)
                return False

            try:
                WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                    (By.XPATH, '//td[@class="m_stock ng-binding"]')))
                WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                    (By.XPATH, '//td[@class="m_stock ng-binding"]')))
                stocks = browser.find_elements_by_xpath('//td[@class="m_stock ng-binding"]')
            except TimeoutException:
                self.log.info("Failed to buy for %s", self.email)
                return False

            for stock in stocks:
                if float(stock.text) > 1000:
                    try:
                        one_level_up = stock.find_element_by_xpath('..')
                        quantity = one_level_up.find_element_by_xpath(
                            './/td[@class="m_quantity ng-scope"]/div/input')
                        quantity.clear()
                        quantity.send_keys("500")
                        buy = one_level_up.find_element_by_xpath(
                            './/td[@class="m_buy ng-scope"]/a')
                        buy.send_keys(Keys.ENTER)
                    except NoSuchElementException:
                        return False
                    break
        return True

    def work(self, browser):
        self.log.info("Working for %s", self.email)
        browser.get('https://www.erepublik.com/en/economy/myCompanies')

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Buy now!')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Buy now!')))
            browser.get('https://www.erepublik.com/en/economy/myCompanies')
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.LINK_TEXT, 'Get Reward')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, 'Get Reward')))        
            get_reward = browser.find_element_by_link_text('Get Reward')
            get_reward.click()
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 5).until(EC.presence_of_element_located(
                (By.XPATH, '//img[@class="employee_worked ng-scope"]')))
            WebDriverWait(browser, 5).until(EC.visibility_of_element_located(
                (By.XPATH, '//img[@class="employee_worked ng-scope"]'))) 
            self.worked = True
            return False
        except TimeoutException:
            pass

        self.log.info("Getting a job if needed for %s", self.email)

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Get a job')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Get a job')))
            button = browser.find_element_by_link_text('Get a job')
            button.send_keys(Keys.RETURN)

            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Apply')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Apply')))
            buttons = browser.find_elements_by_link_text('Apply')
            while len(buttons) > 1:
                buttons.pop()

            button = buttons.pop()

            actions = ActionChains(browser)
            actions.move_to_element(button)
            actions.click(button)
            actions.perform()

            browser.get('https://www.erepublik.com/en/economy/myCompanies')

        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.XPATH, '//a[@id="DailyConsumtionTrigger"]')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.XPATH, '//a[@id="DailyConsumtionTrigger"]'))) 
            button = browser.find_element_by_xpath('//a[@id="DailyConsumtionTrigger"]')
            button.click()
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.LINK_TEXT, 'Energy Bar')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, 'Energy Bar'))) 
            button = browser.find_element_by_link_text('Energy Bar')
            button.click()
        except TimeoutException:
            pass
        
        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.XPATH, '//a[@id="close_limit_health"]')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.XPATH, '//a[@id="close_limit_health"]'))) 
            button = browser.find_element_by_xpath('//a[@id="close_limit_health"]')
            button.click()
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.LINK_TEXT, 'Work')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, 'Work')))  
            buttons = browser.find_elements_by_link_text('Work')
            buttons.pop().click()
            self.worked = True
        except TimeoutException:
            pass
            
        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.LINK_TEXT, 'OK')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, 'OK')))   
            button = browser.find_element_by_link_text('OK')
            button.click()
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.LINK_TEXT, 'Cancel')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, 'Cancel')))    
            button = browser.find_element_by_link_text('Cancel')
            button.click()
        except TimeoutException:
            pass

        return True

    def produce(self, browser):
        self.log.info("Producing for %s", self.email)
        browser.get('https://www.erepublik.com/en/economy/myCompanies')

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Buy now!')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Buy now!')))
            browser.get('https://www.erepublik.com/en/economy/myCompanies')
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.LINK_TEXT, 'Get Reward')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, 'Get Reward')))        
            get_reward = browser.find_element_by_link_text('Get Reward')
            get_reward.click()
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.XPATH, '//a[@id="DailyConsumtionTrigger"]')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.XPATH, '//a[@id="DailyConsumtionTrigger"]'))) 
            button = browser.find_element_by_xpath('//a[@id="DailyConsumtionTrigger"]')
            button.click()
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.LINK_TEXT, 'Energy Bar')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, 'Energy Bar'))) 
            button = browser.find_element_by_link_text('Energy Bar')
            button.click()
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.XPATH, '//a[@id="close_limit_health"]')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.XPATH, '//a[@id="close_limit_health"]'))) 
            button = browser.find_element_by_xpath('//a[@id="close_limit_health"]')
            button.click()
        except TimeoutException:
            pass

        self.log.info("Creating holding if needed")

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.XPATH, '//a[@class="std_global_btn smallSize greenColor createHolding floatLeft new_company"]')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.XPATH, '//a[@class="std_global_btn smallSize greenColor createHolding floatLeft new_company"]'))) 
            button = browser.find_element_by_xpath('//a[@class="std_global_btn smallSize greenColor createHolding floatLeft new_company"]')
            time.sleep(2)
            button.click()
            try:
                WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                    (By.XPATH, '//a[@class="std_global_btn mediumSize averageWidth blueColor create_holding_btn"]')))
                WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                    (By.XPATH, '//a[@class="std_global_btn mediumSize averageWidth blueColor create_holding_btn"]')))
                button = browser.find_element_by_xpath('//a[@class="std_global_btn mediumSize averageWidth blueColor create_holding_btn"]')
                button.click()
                try:
                    WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                        (By.XPATH, '//input[@id="holdingCompanyName"]')))
                    WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                        (By.XPATH, '//input[@id="holdingCompanyName"]')))
                    textbox = browser.find_element_by_xpath('//input[@id="holdingCompanyName"]')

                    rest = self.email.split("@", 1)[0]
                    textbox.send_keys(rest.upper())
                    try:
                        WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                            (By.XPATH, '//a[@class="std_global_btn mediumSize blueColor ctaBtn"]')))
                        WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                            (By.XPATH, '//a[@class="std_global_btn mediumSize blueColor ctaBtn"]')))
                        button = browser.find_element_by_xpath('//a[@class="std_global_btn mediumSize blueColor ctaBtn"]')
                        button.click()
                    except TimeoutException:
                        pass
                except TimeoutException:
                    pass
            except TimeoutException:
                pass
        except TimeoutException:
            pass

        time.sleep(1)
        browser.get('https://www.erepublik.com/en/economy/myCompanies')
        self.log.info("Allocating companies if needed")

        try:
            max_attempts = 5
            attempts = 0
            while attempts < max_attempts:
                try:
                    time.sleep(1)

                    WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                        (By.XPATH, '//div[@id="holding_0"]')))
                    WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                        (By.XPATH, '//div[@id="holding_0"]')))
                    WebDriverWait(browser, 3).until(EC.element_to_be_clickable(
                        (By.XPATH, '//div[@id="holding_0"]')))
                   
                    element = browser.find_element_by_xpath('//div[@id="holding_0"]')
                    button = element.find_element_by_xpath('.//span[@class="toggle isClosed"]')
                    button.click()
                    
                    break
                except WebDriverException:
                    attempts = attempts + 1
                    continue

            time.sleep(1)
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.XPATH, '//a[@class="std_global_btn smallSize assignBtn"]')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.XPATH, '//a[@class="std_global_btn smallSize assignBtn"]')))
            buttons = browser.find_elements_by_xpath('//a[@class="std_global_btn smallSize assignBtn"]')
            for button in buttons:
                button.click()
                try:
                    WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                        (By.XPATH, '//a[@class="std_global_btn mediumSize averageWidth blueColor create_holding_btn"]')))
                    button = browser.find_element_by_xpath('//a[@class="std_global_btn mediumSize averageWidth blueColor create_holding_btn"]')
                    time.sleep(1)
                    button.click()
                    time.sleep(3)
                except TimeoutException:
                    pass
            browser.refresh()
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.XPATH, '//a[@id="check_trigger"]')))
            button = browser.find_element_by_xpath('//a[@id="check_trigger"]')
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.XPATH, '//a[@id="check_trigger"]')))
            button.click()
            try:
                WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                    (By.XPATH, '//a[@id="check_all_companies"]')))
                WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                    (By.XPATH, '//a[@id="check_all_companies"]')))
                button = browser.find_element_by_xpath('//a[@id="check_all_companies"]')
                button.click()
            except TimeoutException:
                pass
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.LINK_TEXT, 'Start production')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, 'Start production')))     
            button = browser.find_element_by_link_text('Start production')
            button.send_keys(Keys.RETURN)
            self.produced = True
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.LINK_TEXT, 'OK')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, 'OK')))    
            button = browser.find_element_by_link_text('OK')
            button.click()          
        except TimeoutException:
            pass
        
        return True

    def train(self, browser):
        self.log.info("Training for %s", self.email)
        browser.get('https://www.erepublik.com/en/economy/training-grounds')

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Buy now!')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Buy now!')))
            browser.get('https://www.erepublik.com/en/economy/training-grounds')
        except TimeoutException:
            pass
        
        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.LINK_TEXT, 'Get Reward')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, 'Get Reward')))        
            get_reward = browser.find_element_by_link_text('Get Reward')
            get_reward.click()
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.XPATH, '//a[@class="green_enlarged ng-scope gored"]')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.XPATH, '//a[@class="green_enlarged ng-scope gored"]')))  
            self.trained = True
            return False
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.LINK_TEXT, 'Train')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, 'Train')))     
            buttons = browser.find_elements_by_link_text('Train')
            buttons.pop().send_keys(Keys.RETURN)
            self.trained = True
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.LINK_TEXT, 'OK')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, 'OK')))     
            button = browser.find_element_by_link_text('OK')
            button.click()
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.LINK_TEXT, 'Cancel')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, 'Cancel')))        
            button = browser.find_element_by_link_text('Cancel')
            button.click()
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.LINK_TEXT, 'Get Reward')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, 'Get Reward')))        
            get_reward = browser.find_element_by_link_text('Get Reward')
            get_reward.click()
            time.sleep(1)
        except TimeoutException:
            pass

        return True

    def change_currency(self, browser):
        self.log.info("Changing currency for %s", self.email)
        browser.get('https://www.erepublik.com/en/economy/exchange-market/')
        
        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Buy now!')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Buy now!')))
            browser.get('https://www.erepublik.com/en/economy/exchange-market/')
        except TimeoutException:
            pass
        
        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.LINK_TEXT, 'Get Reward')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, 'Get Reward')))        
            get_reward = browser.find_element_by_link_text('Get Reward')
            get_reward.click()
        except TimeoutException:
            pass

        try:
            max_attempts = 5
            attempts = 0
            while attempts < max_attempts:
                try:
                    WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                        (By.ID, 'change_currency')))
                    WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                        (By.ID, 'change_currency')))
                    button = browser.find_element_by_id("change_currency")
                    button.click()
                    break
                except WebDriverException:
                    attempts = attempts + 1
                    continue

            try:
                max_attempts = 5
                attempts = 0
                while attempts < max_attempts:
                    try:
                        WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                            (By.XPATH, '//td[@class="ex_amount"]/strong/span')))
                        WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                            (By.XPATH, '//td[@class="ex_amount"]/strong/span')))
                        elements = browser.find_elements_by_xpath('//td[@class="ex_amount"]/strong/span')
                    
                        value = browser.find_element_by_id('side_bar_gold_account_value').text

                        done = False
                        for element in elements:
                            if(float(element.text) > int(value) * 500):
                                element = element.find_element_by_xpath('.//ancestor::tr/td[@class="ex_buy"]')
                                textbox = element.find_element_by_class_name("buy_field")
                                textbox.send_keys(int(value) * 500)

                                actions = ActionChains(browser) 
                                actions.send_keys(Keys.TAB)
                                actions.send_keys(Keys.ENTER)
                                actions.perform()

                                WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                                    (By.ID, 'confirmAlert')))
                                WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                                    (By.ID, 'confirmAlert')))
                                button = browser.find_element_by_id("confirmAlert")
                                button.send_keys(Keys.RETURN)
                                done = True
                                break
                        if done:
                            value = browser.find_element_by_id('side_bar_gold_account_value').text
                            if value == '0':
                                break
                    except StaleElementReferenceException:
                        attempts = attempts + 1
                        continue          
            except TimeoutException:
                pass
        except TimeoutException:
            pass

        return True

    def update_time(self):
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def donate(self, browser):
        self.log.info("Donating for %s", self.email)
        browser.get('https://www.erepublik.com/en/economy/marketplace#15/17/1')
        
        try:
            WebDriverWait(browser, 5).until(EC.presence_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Buy now!')))
            WebDriverWait(browser, 5).until(EC.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Buy now!')))
            browser.get('https://www.erepublik.com/en/economy/marketplace#15/17/1')
        except TimeoutException:
            pass
        
        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.LINK_TEXT, 'Get Reward')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, 'Get Reward')))        
            get_reward = browser.find_element_by_link_text('Get Reward')
            get_reward.click()
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.XPATH, '//td[@class="m_provider"]/a[contains(text(), "Xeorin")]')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.XPATH, '//td[@class="m_provider"]/a[contains(text(), "Xeorin")]')))  

            element = browser.find_element_by_xpath('//td[@class="m_provider"]/a[contains(text(), "Xeorin")]')
            parent1 = element.find_element_by_xpath('..')
            parent2 = parent1.find_element_by_xpath('..')
            button = parent2.find_element_by_xpath('.//a[@class="std_global_btn smallSize blueColor buyOffer"]')
            button.send_keys(Keys.RETURN)
        except TimeoutException:
            self.log.info("Failed to donate")
            return False

        return True

    def fight(self, browser):
        self.log.info("Fighting for %s", self.email)
        browser.get('https://www.erepublik.com/en/military/campaigns')
        
        try:
            WebDriverWait(browser, 5).until(EC.presence_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Buy now!')))
            WebDriverWait(browser, 5).until(EC.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Buy now!')))
            browser.get('https://www.erepublik.com/en/military/campaigns')
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.LINK_TEXT, 'Get Reward')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, 'Get Reward')))        
            get_reward = browser.find_element_by_link_text('Get Reward')
            get_reward.click()
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.XPATH, '//div[@id="campaignsListContainer"]')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.XPATH, '//div[@id="campaignsListContainer"]')))
            elements = browser.find_elements_by_xpath('//li[@class="type_aircraft"]')
            random.shuffle(elements)
            button = elements.pop().find_element_by_xpath(
                './/a[@class="std_global_btn smallSize blueColor ng-scope"]')
            button.send_keys(Keys.RETURN)
            self.fought = True
        except TimeoutException:
            self.log.info("Failed to find a campaign")
            return False

        iterations = 0

        while True:
            try:
                button = browser.find_element_by_xpath('//a[@class="std_global_btn mediumSize greenColor averageWidth close"]')
                button.click()
            except UnexpectedAlertPresentException:
                browser.switch_to_alert().accept()
            except WebDriverException:
                pass

            try:
                button = browser.find_element_by_xpath(
                    '//span[contains(text(), "Fight for")]')
                button.click()
            except UnexpectedAlertPresentException:
                browser.switch_to_alert().accept()
            except WebDriverException:
                pass

            try:
                button = browser.find_element_by_xpath(
                    '//a[@class="fight_btn disabled"]')
                if button:
                    button = browser.find_element_by_id("heal_btn")
                    button.send_keys(Keys.RETURN)
            except UnexpectedAlertPresentException:
                browser.switch_to_alert().accept()
            except WebDriverException:
                pass

            try:
                button = browser.find_element_by_id("fight_btn")
                button.send_keys(Keys.RETURN)
            except UnexpectedAlertPresentException:
                browser.switch_to_alert().accept()
            except WebDriverException:
                pass

            try:
                button = browser.find_element_by_xpath('//a[@class="get_reward fullWidth mediumSize blueColor"]')
                button.send_keys(Keys.RETURN)
            except UnexpectedAlertPresentException:
                browser.switch_to_alert().accept()
            except WebDriverException:
                pass

            try:
                button = browser.find_element_by_id("popDecide")
                button.click()
            except UnexpectedAlertPresentException:
                browser.switch_to_alert().accept()
            except WebDriverException:
                pass

            try:
                button = browser.find_element_by_id("add_damage_btn")
                button.send_keys(Keys.RETURN)
            except UnexpectedAlertPresentException:
                browser.switch_to_alert().accept()
            except WebDriverException:
                pass

            try:
                button = browser.find_element_by_class_name("join")
                button.send_keys(Keys.RETURN)
            except UnexpectedAlertPresentException:
                browser.switch_to_alert().accept()
            except WebDriverException:
                pass

            try:
                button = browser.find_element_by_id("add_rank_btn")
                button.send_keys(Keys.RETURN)
            except UnexpectedAlertPresentException:
                browser.switch_to_alert().accept()
            except WebDriverException:
                pass

            try:
                button = browser.find_element_by_partial_link_text("Next battle")
                button.send_keys(Keys.RETURN)
            except UnexpectedAlertPresentException:
                browser.switch_to_alert().accept()
            except WebDriverException:
                pass

            try:
                browser.find_element_by_id("globalShop")
                break
            except UnexpectedAlertPresentException:
                browser.switch_to_alert().accept()
            except WebDriverException:
                pass
            iterations = iterations + 1

        self.log.info("Finished fighting for %s after %s", self.email, str(iterations))

        return True

    def get_status(self, browser):
        self.log.info("Get status for %s", self.email)
        browser.get('https://www.erepublik.com/en')

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Buy now!')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Buy now!')))
            browser.get('https://www.erepublik.com/en')
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.ID, 'side_bar_gold_account_value')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.ID, 'side_bar_gold_account_value')))
            element = browser.find_element_by_id('side_bar_gold_account_value')
            self.gold = str(element.text)
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.ID, 'side_bar_currency_account_value')))
            WebDriverWait(browser, 3).until(EC.visibility_of_element_located(
                (By.ID, 'side_bar_currency_account_value')))
            element = browser.find_element_by_id('side_bar_currency_account_value')
            self.currency = str(element.text)
        except TimeoutException:
            pass

        try:
            WebDriverWait(browser, 2).until(EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Get all rewards")]')))
            WebDriverWait(browser, 2).until(EC.visibility_of_element_located(
                (By.XPATH, '//span[contains(text(), "Get all rewards")]')))
            button = browser.find_element_by_xpath('//span[contains(text(), "Get all rewards")]')
            button.click()
            time.sleep(1)
        except TimeoutException:
            pass

        return True
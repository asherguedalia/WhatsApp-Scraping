"""
Importing the libraries that we are going to use
for loading the settings file and scraping the website
"""
import os
import time
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ride_adder import ride_adder


class WhatsappScrapper():
    def __init__(self, page, browser, browser_path):
        self.page = page
        self.browser = browser
        self.browser_path = browser_path
        self.driver = self.load_driver()

        # Open the web page with the given browser
        self.driver.get(self.page)

    def load_driver(self):
        """
        Load the Selenium driver depending on the browser
        (Edge and Safari are not running yet)
        """
        driver = None
        if self.browser == 'firefox':
            firefox_profile = webdriver.FirefoxProfile(
                self.browser_path)
            driver = webdriver.Firefox(firefox_profile)
        elif self.browser == 'chrome':
            chrome_options = webdriver.ChromeOptions()
            if self.browser_path:
                print('here!!!', self.browser_path)
                files = os.listdir(self.browser_path)
                for f in files:
                    if 'chrome' in f:
                        print(f)
                chrome_options.add_argument('user-data-dir=' +
                                            self.browser_path)
            # driver = webdriver.Chrome(options=chrome_options)
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        elif self.browser == 'safari':
            pass
        elif self.browser == 'edge':
            pass

        return driver

    def open_conversation(self, names):
        """
        Function that search the specified user by the 'name' and opens the conversation.
        """
        print('scraping messages with groups who contain', names)
        while True:
            try:
                for chatter in self.driver.find_elements_by_xpath("//div[@id='pane-side']/div/div/div/div"):
                    #print('in for loop', chatter.text)

                    for name in names:

                        if name in chatter.text:
                            lines = chatter.text.split('\n')
                            if len(lines) > 3:

                                group_name = lines[0]
                                time_stamp = lines[1]
                                sender_number = lines[2]
                                msg = ''.join(lines[3:])

                                ride_adder(group_name, time_stamp, sender_number, msg)

                            else:
                                print('lines', lines)
                            print('------------')
                            time.sleep(random.randint(15, 20))

            except StaleElementReferenceException:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//span[contains(@title,'{}')]".format(
                            name)))
                )



                # #### todo - probably will need to teach it to scroll to find more contacts if they dont appear ### actually not cuz if its a new chat it will show up
                # if name not in chatter.text:
                #     continue
                # # chatter_path = ".//span[@title='{}']".format(name)
                # chatter_path = "//span[contains(@title,'{}')]".format(name)
                #
                # # Wait until the chatter box is loaded in DOM
                # try:
                #     WebDriverWait(self.driver, 10).until(
                #         EC.presence_of_element_located(
                #             (By.XPATH, "//span[contains(@title,'{}')]".format(
                #                 name)))
                #     )
                # except StaleElementReferenceException:
                #     WebDriverWait(self.driver, 10).until(
                #         EC.presence_of_element_located(
                #             (By.XPATH, "//span[contains(@title,'{}')]".format(
                #                 name)))
                #     )
                #
                # try:
                #     print('trying this!', chatter.text)
                #     chatter_name = chatter.find_element_by_xpath(
                #         chatter_path).text
                #     if chatter_name == name:
                #         print('here in chatter 1')
                #         print(chatter_name, name)
                #         chatter.find_element_by_xpath(
                #             ".//div/div").click()
                #         return True
                #     else:
                #         print('here in chatter 2')
                #         print(chatter_name, name)
                #
                # except Exception as e:
                #     print('found error', e)
                #     return False

    def read_last_in_message(self):
        """
        Reading the last message that you got in from the chatter
        """
        text_list = self.driver.find_elements_by_class_name('copyable-text')

        # try:
        #     for tex in text_list:
        #         print('text', tex.text)
        # except Exception:
        #     print('coudlnt')
        if len(text_list) > 1:
            return text_list[-2].text
        return ''
        # for messages in self.driver.find_elements_by_xpath(
        #         "//div[contains(@class,'message-in')]"):
        #     print('in for loop')
        #     try:
        #         message = ""
        #         emojis = []
        #
        #         message_container = messages.find_element_by_xpath(
        #             ".//div[@class='copyable-text']")
        #
        #         message = message_container.find_element_by_xpath(
        #             ".//span[contains(@class,'selectable-text invisible-space copyable-text')]"
        #         ).text
        #
        #         for emoji in message_container.find_elements_by_xpath(
        #                 ".//img[contains(@class,'selectable-text invisible-space copyable-text')]"
        #         ):
        #             emojis.append(emoji.get_attribute("data-plain-text"))
        #
        #     except NoSuchElementException:  # In case there are only emojis in the message
        #         print('maybe only emojis')
        #         try:
        #             message = ""
        #             emojis = []
        #             message_container = messages.find_element_by_xpath(
        #                 ".//div[contains(@class,'copyable-text')]")
        #
        #             for emoji in message_container.find_elements_by_xpath(
        #                     ".//img[contains(@class,'selectable-text invisible-space copyable-text')]"
        #             ):
        #                 emojis.append(emoji.get_attribute("data-plain-text"))
        #         except NoSuchElementException:
        #             print('nope no element')
        #             pass

        # return message, emojis

    def send_message(self, text):
        """
        Send a message to the chatter.
        You need to open a conversation with open_conversation()
        before you can use this function.
        """

        input_text = self.driver.find_element_by_xpath(
            "//div[@id='main']/footer/div/div[2]/div/div[@contenteditable='true']")

        input_text.click()
        input_text.send_keys(text)

        send_button = self.driver.find_element_by_xpath(
            "//div[@id='main']/footer/div/div[3]/button")
        send_button.click()

        return True

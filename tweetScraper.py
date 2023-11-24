import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

from dotenv import load_dotenv
import os

class TwitterScrape:

    def __init__(self):
        f_options = Options()
        f_options.add_argument('--headless')
        f_options.add_argument('--disable-gpu')
        self.ctx = webdriver.Firefox(options=f_options)
        load_dotenv()        


    def login(self):
        email_id = os.getenv("EMAIL_ID")
        user_name = os.getenv("USER_NAME")
        password = os.getenv("PASSWORD")
        self.ctx.get("https://twitter.com/i/flow/login")
        time.sleep(3)
    

        #input email
        self.ctx.find_element(By.TAG_NAME, "input").send_keys(email_id)
        self.ctx.find_elements(By.XPATH, "//div[@role = 'button']")[3].click()
        time.sleep(3)

        #input username
        self.ctx.find_element(By.XPATH, "//input[@type= 'text']").send_keys(user_name)
        self.ctx.find_elements(By.XPATH, "//div[@role = 'button']")[1].click()
        time.sleep(3)

        #input password
        self.ctx.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
        self.ctx.find_elements(By.XPATH, "//div[@role = 'button']")[2].click()
        time.sleep(3)

    def get_tweets_from_list(self, list_url):
        self.ctx.get(list_url)
        time.sleep(5)
        tweets = self.ctx.find_elements(By.XPATH, "//article[@data-testid = 'tweet']")
        twts = []
        links = []
        for tweet in tweets:
            link =  tweet.find_element(By.TAG_NAME,"time").find_element(By.XPATH, "..").get_attribute("href")
            links.append(link)
            
        self.ctx.get("https://publish.twitter.com/")
        for lnk in links:
            self.ctx.find_element(By.XPATH, ".//input").clear()
            self.ctx.find_element(By.XPATH, ".//input").send_keys(lnk)
            self.ctx.find_element(By.XPATH, ".//button[@type = 'submit']").click()
            time.sleep(.5)
            code = self.ctx.find_element(By.XPATH, ".//code").text
            twts.append(code)

        return twts;
    def __del__(self):
        self.ctx.quit()

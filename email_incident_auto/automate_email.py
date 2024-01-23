from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from random import seed
import requests

import pandas as pd
import numpy as np

# to find links
from bs4 import BeautifulSoup
import json
import urllib.request
from urllib.request import Request, urlopen
import re

import os

import time # to sleep

import configparser

PREFERENCES = {
    'title': 'sent Adobe Audit email for '
}

def login(driver):
    driver.get('https://disneystreaming.service-now.com/nav_to.do?uri=%2Fincident.do%3Fsys_id%3D-1%26sysparm_query%3Dactive%3Dtrue%26sysparm_stack%3Dincident_list.do%3Fsysparm_query%3Dactive%3Dtrue')

    try: 
        WebDriverWait(driver,50).until(EC.url_contains('nav_to.do?'))
    except Exception as e:
        print(e)
        return False
        
    time.sleep(2)
    return True

def array_create():

    emails_file_path = '/Users/kyler.rynear.-nd/adobe_automation/emails.xlsx'
    df = pd.read_excel(emails_file_path)
    names = 'Username'
    names_array = np.array(df[names])

    names = np.empty_like(names_array, dtype='U200')  # Assuming a maximum length of 50 for names
    
    for i, email in enumerate(names_array):
        match = re.match(r'([a-zA-Z]+)\.([a-zA-Z]+)@hulu\.com', email, re.IGNORECASE)
        
        if match:
            firstname = match.group(1)
            lastname = match.group(2)
            full_name = f'{firstname} {lastname}'
            names[i] = full_name
        else:
            print(f"Warning: Unable to parse email format for {email}")
            names[i] = ''  # You can assign a default value or handle it differently
    
    return names

def incident(driver, name):
    try:

        actions = ActionChains(driver)
        iframe = driver.find_element(By.XPATH, "//iframe[@id='gsft_main']")
        driver.switch_to.frame(iframe)

        template_button = driver.find_element(By.XPATH, "//*[@data-ref='51db5e2087dbb910568dfea8cebb3528']").click()

        test = driver.find_element(By.XPATH, "//input[@id='incident.short_description']")
        time.sleep(0.7)

        new_title = PREFERENCES['title'] + name
        test.send_keys(new_title)
        time.sleep(0.7)


        res_tab = driver.find_element(By.XPATH, f"//*[@class='tabs2_strip']")
        res_tab.click()
        time.sleep(0.7)

        res_tab = driver.find_element(By.XPATH, r"//*[@id='tabs2_section']/span[3]/span[1]")
        res_tab.click()
        time.sleep(0.7)

        res_notes = driver.find_element(By.XPATH, "//textarea[@id='incident.close_notes']")
        res_notes.clear()
        res_notes.send_keys(new_title)
        time.sleep(0.7)

        res_tab = driver.find_element(By.XPATH, f"//*[@class='tabs2_strip']")
        res_tab.click()
        time.sleep(0.7)

        submit = driver.find_element(By.XPATH, f"//*[@id='sysverb_insert']")
        submit.click()
        time.sleep(3.7)

    except Exception as e: 
        print(e)
        return False

    

    return True

def check_start(name, names):
    for i, check in enumerate(names):
        if check == name:
            return i

    return False

def automate():
    custom_profile_path = "/Users/kyler.rynear.-nd/Library/Application Support/Google/Chrome/User Data"
    service = Service(executable_path='/opt/homebrew/Caskroom/chromedriver/120.0.6099.71/chromedriver-mac-arm64/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={custom_profile_path}")
    options.add_argument(f"--profile-directory=Profile 2")
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    driver = webdriver.Chrome(options=options, service=service)

    names = array_create()
    with open('/Users/kyler.rynear.-nd/email_incident_auto/ending_name.txt', 'r') as file:
        current_name = file.read()

    start = check_start(current_name, names)
    if not start:
        driver.quit()
        return False

    count = int(input("how many tickets to do: "))

    for name in names[start+1:start+count+1]: #BRIAN ANDERSON
        success = login(driver)
        if not success:
            driver.quit()
            return False

        success = incident(driver,name)
        if not success:
            driver.quit()
            return False

        end = name
    
    with open('/Users/kyler.rynear.-nd/email_incident_auto/ending_name.txt', 'w') as file:
        file.write(end)



    # print(names)



    driver.quit()
    return True

automate()
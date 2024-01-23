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
    "myid_email": "rynek004",
    "myid_pw": "Mezmerize8989DISNEY1!"
}

def login(driver):
    driver.get('https://disneystreaming.service-now.com/nav_to.do?uri=%2Ftask_list.do%3Fsysparm_view%3D%26sysparm_first_row%3D1%26sysparm_query%3Dstate%3D1%5Esys_class_name%3Dsc_task%5Eassignment_group%3D64c72e421b4b3010729d2068b04bcb7f%5Esys_class_name%3Dsc_task%5Eassigned_toISEMPTY%5ENQassignment_group%3D64c72e421b4b3010729d2068b04bcb7f%5Esys_class_name%3Dincident%5Eref_incident.incident_state!%3D6%5Eactive%3Dtrue%5Esys_class_name%3Dsc_task%26sysparm_clear_stack%3Dtrue')
    try: 
        WebDriverWait(driver,50).until(EC.url_contains('nav_to.do?'))
    except Exception as e:
        print(e)
        return False
        
    time.sleep(2)
    return True

def myid_login(driver):
    try:
        input = driver.find_element(By.XPATH, "//*[@id='login-username']")
        input.send_keys(PREFERENCES['myid_email'])

        next = driver.find_element(By.XPATH, "//*[@id='login-next']").click()

        time.sleep(2)

        password = driver.find_element(By.XPATH, "//*[@id='login-password']")
        password.send_keys(PREFERENCES["myid_pw"])

        submit = driver.find_element(By.XPATH, "//*[@id='login-submit']").click()

        if ("mfa" in driver.current_url):
            push = driver.find_element(By.XPATH, "//*[@id='mfa-sendpush']").click()
            time.sleep(4)

        try:
            ttb = driver.find_element(By.XPATH, "//*[@id='mfa-trustedbrowsers-trust']").click()
            time.sleep(4)
        except:
            pass

    except Exception as e:
        print(e)
        return False

def get_task(driver):
    try:
        time.sleep(0.8)


        total_rows = int(driver.find_element(By.XPATH, f"//*[contains(@id, '_total_rows')]").text)
        last_row = int(driver.find_element(By.XPATH, f"//*[contains(@id, '_last_row')]").text)

        while (last_row != total_rows):
            time.sleep(0.8)
            table = driver.find_element(By.XPATH, "//*[@id='task_table']")
            rows = table.find_elements(By.TAG_NAME, "tr")
            total_rows = int(driver.find_element(By.XPATH, f"//*[contains(@id, '_total_rows')]").text)
            last_row = int(driver.find_element(By.XPATH, f"//*[contains(@id, '_last_row')]").text)

            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")

                for column in columns:
                    if "SCTASK" in column.text:
                        element_to_return = column

                    if (column.text == "Manage Accounts - Vault Access Request"):
                        return element_to_return

                    elif (column.text == "Manage Accounts - Charles Proxy Access Request"):
                        return element_to_return
                    
                    # elif ("HARPS" in column.text):
                    #     return element_to_return
                    
                    # elif ("Mission Control" in column.text):
                    #     return element_to_return

            print("got here")
            next_page = driver.find_element(By.XPATH, "//*[contains(@name, 'vcr_next')]").click()
        return False    
            


    except Exception as e:
        print(e)
        return False

    return True 

def vault_task(driver):
    try:
        time.sleep(1.8)
        template_button = driver.find_element(By.XPATH, "//*[@data-ref='e203ebaf87a7f1103e11fea8cebb35aa']").click()
        time.sleep(1.8)
        update = driver.find_element(By.XPATH, "//*[@id='sysverb_update']").click()
    except Exception as e:
        print(e)
        return False

    return True

def CP_task(driver):
    try:
        time.sleep(1.8)
        template_button = driver.find_element(By.XPATH, "//*[@data-ref='e7c2e8d1877f3110dad2653e0ebb3501']").click()
        time.sleep(1.8)
        update = driver.find_element(By.XPATH, "//*[@id='sysverb_update']").click()
    except Exception as e:
        print(e)
        return False

    return True

def MC_task(driver):
    try:
        time.sleep(1)
        action = ActionChains(driver)
        info = driver.find_element(By.XPATH, "/html/body/div[2]/form/span[2]/span/div/div/div/div/table/tbody/tr[2]/td/div[2]/div/table/tbody/tr[2]/td/span/div/div[1]/table/tbody/tr/td/div/div/div/div[2]/div/span/span/span/a[2]")
        new_info = info.click()
        time.sleep(0.5)
        email = driver.find_element(By.XPATH, "//*[@id='sys_readonly.sys_user.email']").get_attribute('value')
        info.click()
        category = driver.find_element(By.XPATH, "/html/body/div[2]/form/span[2]/span/div/div/div/div/table/tbody/tr[2]/td/div[2]/div/table/tbody/tr[3]/td/span/div/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/input").get_attribute('value')


        task_tab = driver.current_window_handle
        driver.switch_to.new_window('tab')
        driver.get("https://mc.prod.hulu.com/access-manager")
        time.sleep(5)

        if ("auth" in driver.current_url):
            try:
                login_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/div/form/div/div/input[2]").click()
            except Exception as e:
                print(e)
                return False
            time.sleep(1.3)

        if ("login.myid.disney.com" in driver.current_url):
            success = myid_login(driver)
            if not success:
                return False
            driver.get("https://mc.prod.hulu.com/access-manager")

        

    except Exception as e:
        print(e)
        return False
        
    

    

            




def tasks():
    custom_profile_path = "/Users/kyler.rynear.-nd/Library/Application Support/Google/Chrome/User Data"
    service = Service(executable_path='/opt/homebrew/Caskroom/chromedriver/120.0.6099.71/chromedriver-mac-arm64/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={custom_profile_path}")
    options.add_argument(f"--profile-directory=Profile 2")
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    driver = webdriver.Chrome(options=options, service=service)


    count = int(input("how many tickets to do: "))

    success = login(driver)
    if not success:
        driver.quit()
        return False

    actions = ActionChains(driver)
    iframe = driver.find_element(By.XPATH, "//iframe[@id='gsft_main']")
    driver.switch_to.frame(iframe)
    
    for i in range(count):
        time.sleep(0.8)
        task = get_task(driver)
        if not task:
            driver.quit()
            return False
        
        new_task = task.click()
        time.sleep(1.8)
        try:
            task_type = driver.find_element(By.XPATH, "//*[@id='sys_display.sc_task.cmdb_ci']")
            task_name = task_type.get_attribute("value")
        except Exception as e:
            print(e)
            return False
        
        if (task_name == "Vault Access Request"):
            success = vault_task(driver)
            if not success:
                driver.quit()
                return False
            
        elif (task_name == "Charles Proxy"):
            success = CP_task(driver)
            if not success:
                driver.quit()
                return False 
            
        elif ("Mission Control" in task_name):
            success = MC_task(driver)
            if not success:
                driver.quit()
                return False     

        
    



    return True

tasks()
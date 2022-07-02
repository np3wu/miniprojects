from numpy import append
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
import pandas as pd

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--window-size=1920,1020")

driver = webdriver.Chrome(options=options)
driver.get("https://www.ars.usda.gov/northeast-area/beltsville-md-barc/beltsville-agricultural-research-center/adaptive-cropping-systems-laboratory/docs/ppd/pesticide-list/")

popup = driver.find_element(By.XPATH , "//*[@id='prefix-dismissButton']").click()
#popup2 = driver.find_element(By.XPATH , '//*[@id="cfi_btnNoThanks"]')

#testing the button
#button = driver.find_element(By.XPATH , '//*[@id="main-content"]/div[3]/table[2]/tbody/tr/td/div/ul/li[1]/strong/a').click()


def get_text (driver, boundary):
    """Getting the molecular formula from the ars.usda.gov page""" 
    data = driver.find_element(By.XPATH, '/html/body/pre').text
    data_clean = re.search(boundary, data)
    return data_clean.group(1)
        
# Boundary information to get the specific data
molecular_formula_boudary = 'molecular formula: (.*)\nmolecular weight'
common_name_boundary = 'name: (.*)CASRN:'

#collect the number of items
items = len(driver.find_elements(By.XPATH, "//li//strong"))



#Failed to find by xpath because web dev people can't keep things consistent. 
#some is under /strong and some is under /a
# try and except is a god send
col1 = []
col2 = []
for itemNum in range (1 , int(items) + 1):
    wait = WebDriverWait(driver, 5)
#    if wait.until(driver.find_element(By.XPATH , '//*[@id="cfi_btnNoThanks"]')) == None:
    try:
        item = driver.find_element(By.XPATH , f'//*[@id="main-content"]/div[3]/table[2]/tbody/tr/td/div/ul/li[{itemNum}]/a').click()
        try:
            name = get_text(driver , common_name_boundary)
            formula = get_text(driver , molecular_formula_boudary)

            col1.append(name)
            col2.append(formula)
        except:
            pass
        driver.back()
    except:
        item = driver.find_element(By.XPATH , f'//*[@id="main-content"]/div[3]/table[2]/tbody/tr/td/div/ul/li[{itemNum}]/strong/a').click()
        try:
            name = get_text(driver , common_name_boundary)
            formula = get_text(driver , molecular_formula_boudary)

            col1.append(name)
            col2.append(formula)
        except:
            pass
        driver.back()

data = list (zip(col1 , col2))

df = pd.DataFrame(data , columns=['Common Name' , 'Chemical Formula'])

df.to_csv('usda.csv')


from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


def add_crns(g_num, web_pin, courses):
    #Login to Banner Web
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://ssb-prod.ec.gram.edu/PROD/twbkwbis.P_GenMenu?name=homepage")
    enter_secure_area = driver.find_element(By.XPATH,'/html/body/div[3]/table[1]/tbody/tr[1]/td[2]/a')
    enter_secure_area.click()
    driver.find_element(By.XPATH,'//*[@id="UserID"]').send_keys(g_num)
    pin = driver.find_element(By.XPATH,'//*[@id="PIN"]')
    pin.send_keys(web_pin, Keys.ENTER)
    
    #student
    driver.find_element(By.XPATH,'/html/body/div[3]/table[1]/tbody/tr[3]/td[2]/a').click()

    #Registation
    driver.find_element(By.XPATH, '/html/body/div[3]/table[1]/tbody/tr[2]/td[2]/a').click()
    
    #Add or drop classes
    driver.find_element(By.XPATH, '/html/body/div[3]/table[1]/tbody/tr[3]/td[2]/a').click()
    driver.find_element(By.XPATH, '/html/body/div[3]/form/input').click()
    
    #add CRNs
    for index, crn  in enumerate(courses):
        driver.find_element(By.XPATH,f'/html/body/div[3]/form/table[3]/tbody/tr[2]/td[{index+1}]/input[2]').send_keys(crn)
    
    #submit classes
    driver.find_element(By.XPATH, '/html/body/div[3]/form/input[19]').click()

add_crns("G00450781", "838383", ['22315', '21606', '21173', '21495', '22623'])
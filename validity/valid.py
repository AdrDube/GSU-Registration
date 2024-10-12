from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



def valid_works(reg_name, password):
    """
    Checks if the username and password Degree Works are valid
    Returns True or False

    :param reg_name: Username for degree works
    :type reg_name: string

    :param password: Password for degree works
    :type password: string

    :returns whether degree works information is valid
    :rtype: bool
    """
    driver = webdriver.Chrome()
    driver.get("https://dw-prod.ec.gram.edu/responsiveDashboard/worksheets/WEB31")
    driver.find_element("xpath","/html/body/div/div/div/div/form/div[1]/input[1]").send_keys(reg_name)
    driver.find_element(By.XPATH,"/html/body/div/div/div/div/form/div[2]/input").send_keys(password)
    driver.find_element("xpath","/html/body/div/div/div/div/form/div[3]/div/button").click()
    sleep(5)
    try:
        driver.find_element("xpath","/html/body/div/div/div/div/form/div[2]/input[1]")
        return False
    except:
        return True
  
def valid_web(g_num, web_pin):
    """
    Checks if the username and password for Banner Web are valid
    Returns True or False

    :param g_num: Username for banner web
    :type g_num: string

    :param password: Password/Pin for banner web
    :type password: string

    :returns whether banner web information is valid
    :rtype: bool
    """

    driver = webdriver.Chrome()
    driver.get("https://ssb-prod.ec.gram.edu/PROD/twbkwbis.P_GenMenu?name=homepage")
    enter_secure_area = driver.find_element(By.XPATH,'/html/body/div[3]/table[1]/tbody/tr[1]/td[2]/a')
    enter_secure_area.click()
    driver.find_element(By.XPATH,'//*[@id="UserID"]').send_keys(g_num)
    pin = driver.find_element(By.XPATH,'//*[@id="PIN"]')
    pin.send_keys(web_pin, Keys.ENTER)
    try:
        driver.find_element(By.XPATH,'//*[@id="UserID"]')
        return False
    except:
        return True
    


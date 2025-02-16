from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
import time


def get_transcripts(name, password):
    driver = webdriver.Chrome()
    driver.get("https://dw-prod.ec.gram.edu/responsiveDashboard/worksheets/WEB31")

    driver.find_element(By.ID, "username").send_keys(name)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "/html/body/div/div/div/div/form/div[2]/div[3]/div/button").click()
    menu = False
    extracted=False

    while not extracted:
        try:
            while not menu:
                menu_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div/div/div[2]/div/main/div/div[1]/div/div")))

                time.sleep(1)  # Give time for animations
                menu_element.click()

                driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/ul/li/div/span").click()
                menu = True

            time.sleep(2)
            elements = driver.find_elements(By.TAG_NAME, "table")
            classes_taken = []

            for element in elements:
                if not element.text.strip():
                    continue
                extracted=True
                element_text = element.text
                for courses in element_text.split("\n"):
                        course_elem = courses.split()
                        classes_taken.append(course_elem[0] + " " + course_elem[1])
            
        
        except StaleElementReferenceException:
            print("Stale Elem. Reload in progress")
        except TimeoutException:
            print("Timeout")


    
    driver.quit()
    return classes_taken[1:]

def get_degree_info(name, password):
    driver = webdriver.Chrome()
    driver.get("https://dw-prod.ec.gram.edu/responsiveDashboard/worksheets/WEB31")

    
    driver.find_element(By.ID, "usernameUserInput").send_keys(name)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "/html/body/div/div/div/div/form/div[2]/div[3]/div/button").click()
    menu = False
    extracted=False
    profile={}
    timeout=0
    while not extracted:
        try:
            while not menu:
                menu_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div/div/div[2]/div/main/div/div[1]/div/div")))
                
                profile["id"] = driver.find_element(By.ID, 'student-id').get_attribute('value')
                profile["name"]= driver.find_element(By.ID, 'student-name').get_attribute('value')
                profile["degree"]= driver.find_element(By.ID, 'degree').get_attribute('value')
                info = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/div/main/div/div[2]/div[2]/div[2]/div/div')
                profile['level']  = info[0].text.split()[1]
                profile['classification']= info[1].text.split()[1]
                profile['major']  =  " ".join(info[4].text.split()[1:])
                profile['college']  = " ".join(info[4].text.split()[1:])
                profile['credits']  = info[6].text.split()[-1]
                profile['gpa']= info[8].text.split()[-1]

                time.sleep(1)  # Give time for animations
                menu_element.click()

                driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/ul/li/div/span").click()
                menu = True

            time.sleep(2)
            elements = driver.find_elements(By.TAG_NAME, "table")
            classes_taken = []

            for element in elements:
                if not element.text.strip():
                    continue
                extracted=True
                element_text = element.text
                for courses in element_text.split("\n"):
                        course_elem = courses.split()
                        classes_taken.append(course_elem[0] + " " + course_elem[1])
            
        
        except StaleElementReferenceException:
            print("Stale Elem. Reload in progress")
        except TimeoutException:
            timeout+=1
            try:
                driver.find_element("xpath","/html/body/div/div/div/div/form/div[2]/input[1]")
                return { "error": "Your password has changed. Check your login details and try"}
            except:
                pass
            if timeout==3:
                return {"error": "Degree works is currently unavailable, please try agiain later"}
            print("Timeout")


    
    driver.quit()
    profile["classes_taken"] = classes_taken
    return profile



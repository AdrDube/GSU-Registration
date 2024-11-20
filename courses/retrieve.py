from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_transcripts(name, password):
    driver = webdriver.Chrome()
    driver.get("https://dw-prod.ec.gram.edu/responsiveDashboard/worksheets/WEB31")

    driver.find_element(By.XPATH, "/html/body/div/div/div/div/form/div[1]/input[1]").send_keys(name)
    driver.find_element(By.XPATH, "/html/body/div/div/div/div/form/div[2]/input").send_keys(password)
    driver.find_element(By.XPATH, "/html/body/div/div/div/div/form/div[3]/div/button").click()
    time.sleep(5)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div/div/div[2]/div/main/div/div[1]/div/div"))).click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/ul/li/div/span").click()
    elements = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(
        (By.TAG_NAME, "tbody")))
    
    classes_taken = []
    for element in elements:
        element_text = element.text
        if element_text:
            for courses in element_text.split("\n"):
                course_elem = courses.split()
                if len(course_elem) >= 2:
                    classes_taken.append(course_elem[0] + " " + course_elem[1])
                else:
                    print(f"Skipping course_elem due to insufficient length: {course_elem}")
    
    driver.quit()
    return classes_taken

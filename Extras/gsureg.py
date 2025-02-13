from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time



driver = webdriver.Chrome()

def get_transcripts(name, password):
    driver = webdriver.Chrome()
    driver.get("https://dw-prod.ec.gram.edu/responsiveDashboard/worksheets/WEB31")

    driver.find_element(By.XPATH,"/html/body/div/div/div/div/form/div[1]/input[1]").send_keys(name)
    driver.find_element(By.XPATH,"/html/body/div/div/div/div/form/div[2]/input").send_keys(password)
    driver.find_element(By.XPATH,"/html/body/div/div/div/div/form/div[3]/div/button").click()
    time.sleep(5)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located
                    ((By.XPATH,"/html/body/div/div/div[2]/div/main/div/div[1]/div/div"))).click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/ul/li/div/span").click()
    elements = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located
                    ((By.TAG_NAME, "tbody")))
    classes_taken = []
    for element in elements:
        element=element.text
        if element:
            for courses in element.split("\n"):
                course_elem = courses.split()
                classes_taken.append(course_elem[0] + " " + course_elem[1])
    driver.quit()
    return classes_taken

def find_classes(g_num, web_pin, semester, year) :
   
    #enter bannerweb and login
    driver.get('https://ssb-prod.ec.gram.edu/PROD/twbkwbis.P_GenMenu?name=homepage')
    driver.find_element(By.XPATH,'/html/body/div[3]/table[1]/tbody/tr[1]/td[2]/a').click()
    
    user_id = driver.find_element(By.XPATH,'//*[@id="UserID"]')
    user_id.send_keys(g_num)

    pin = driver.find_element(By.XPATH,'//*[@id="PIN"]')
    pin.send_keys(web_pin)
    pin.send_keys(Keys.ENTER)
    
    #navigate to the lookup page
    driver.find_element(By.XPATH,'/html/body/div[3]/table[1]/tbody/tr[3]/td[2]/a').click()
    driver.find_element(By.XPATH,'/html/body/div[3]/table[1]/tbody/tr[2]/td[2]/a').click()
    driver.find_element(By.XPATH,'/html/body/div[3]/table[1]/tbody/tr[4]/td[2]/a').click()

   #find the specific semester and enter the page

   #convert year and semester to array with formatting used in website 
    requested = [year, semester.title()]
    print(requested)
    xpath = driver.find_element(By.XPATH,"/html/body/div[3]/form/table/tbody/tr/td/select/option[2]")
    semester = xpath.text.split()[:2]
    print(semester)
    
    if semester == requested:
       xpath = driver.find_element(By.XPATH,"/html/body/div[3]/form/table/tbody/tr/td/select/option[2]").click()
    else:
        xpath = driver.find_element(By.XPATH,"/html/body/div[3]/form/table/tbody/tr/td/select/option[3]").click()

    driver.find_element(By.XPATH,"/html/body/div[3]/form/input[2]").click()

def specific_times(chosen):
    res = {}
    for elem in chosen :
        sub = elem.split()
        option_element = driver.find_element(By.CSS_SELECTOR,f"option[value='{sub[0]}']").click()
        search = driver.find_element(By.XPATH, "/html/body/div[3]/form/input[17]").click()
        
        #This is for finding the class number e.g Hist 104... we'll be looking for the number 104
        #Also implemented the driver wait function for 
        class_num = WebDriverWait(driver, 5).until(EC.presence_of_element_located
                    ((By.XPATH,f'//td[text()="{sub[1]}"]')))

        #this is for navigating back to the parent node (which is the same row where there is the number we were looking for and the "submit" button. 
        parent_row = class_num.find_element(By.XPATH,"ancestor::tr")

        #this is the "submit" button we need to click after finding the number. 
        button = parent_row.find_element(By.XPATH,".//input[@type='submit']").click()
        
        
        #collecting CRN, DAYS, TIM, and professor
        table = driver.find_element(By.XPATH,"/html/body/div[3]/form/table/tbody")

    
        rows = table.find_elements(By.TAG_NAME,"tr")[2:]
        res[elem] = []
        
        for row in rows:         
            CRN = row.find_element(By.XPATH,".//td[2]").text
            DAYS = row.find_element(By.XPATH,".//td[9]").text
            TIME = row.find_element(By.XPATH,".//td[10]").text
            PROF = row.find_element(By.XPATH,".//td[20]").text
            res[elem].append([CRN,DAYS,TIME,PROF])
                
        driver.back()
        driver.back()
        driver.back()
        driver.find_element(By.XPATH,"/html/body/div[3]/form/input[2]").click()
    
    return res

def all_times():

       
    data_cell = driver.find_element(By.XPATH,"/html/body/div[3]/form/table[1]/tbody/tr/td[2]")
    rows = data_cell.find_elements(By.TAG_NAME,"option")
    
    
    for i in range(len(rows)):
        data_cell = driver.find_element(By.XPATH,"/html/body/div[3]/form/table[1]/tbody/tr/td[2]")
        row = data_cell.find_elements(By.TAG_NAME,"option")[i]
        row.click()
        search = driver.find_element(By.XPATH, "/html/body/div[3]/form/input[17]").click()
        course_list_table = driver.find_element(By.XPATH,"/html/body/div[3]/table[2]/tbody")
        
        # Find an element with an attribute "value" equal to "your_value"
        buttons = course_list_table.find_elements(By.CSS_SELECTOR, '[value="View Sections"]')
        courses = (len(buttons))
        
        #course_rows = course_list_table.find_elements(By.TAG_NAME,"tr")[2:]

        #course_rows[0].find_element(By.XPATH,"/html/body/div[3]/table[2]/tbody/tr[3]/td[3]/form/input[30]").click()

        for i in range(len(buttons)):
            course_list_table = driver.find_element(By.XPATH,"/html/body/div[3]/table[2]/tbody")
            course_list_table.find_elements(By.CSS_SELECTOR, '[value="View Sections"]')[i].click()
            print(i)
            driver.back()
        driver.back()
        driver.back()
        driver.find_element(By.XPATH,"/html/body/div[3]/form/input[2]").click()

        
if __name__=="__main__":
    find_classes("G00450781", "838383", "fall", "2024")
    #subjects=specific_times(['FYE 102', 'BIOL 113', 'MATH 154', 'BIOL 115', 'CS 120', 'HIST 104', 'ENG 102'])
    #all_courses = all_times()
   

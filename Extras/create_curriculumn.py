from Reg import get_curriculumn2
import mysql.connector
import mysql.connector
import os
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

"""
Once off code to extract curriculumn and classes available from webpage and add it to our remote database in AWS
Can be modified to help create curriculumn for other courses

Step1 - extract curriculumn from website
      - ensure the package Reg is available first
      - program has been moved to ensure readablity

Step2 - place data inside our DB
"""


env = os.path.join("../.env")
secrets = dotenv_values(env)
dbs = mysql.connector.connect(
    host=secrets["mysql_host"],
    port=secrets["port"],
    user=secrets["mysql_user"],
    password=secrets["mysql_password"],
    database=secrets["mysql_database"],
)
cursor = dbs.cursor()
driver = webdriver.Chrome()

#cursor.execute("CREATE TABLE Classes (CRN INT PRIMARY KEY, SUBJECT VARCHAR(5), COURSE VARCHAR(3), DAYS VARCHAR(3), TIME VARCHAR(20))")
#cursor.execute("INSERT INTO Classes (CRN, SUBJECT, COURSE, DAYS, TIME) VALUES (12447, 'HIST', 103, 'TR', '01:00pm - 02:20pm')")
#cursor.execute("ALTER TABLE Classes MODIFY COLUMN COURSE VARCHAR(6)")

def create_course(var):    
    #Check if data with the same CRN Exists
    cursor.execute("SELECT 1 FROM Classes WHERE CRN = %s",var[0])
    result = cursor.fetchone()
    if result is None:
        #If CRN doesnt exist then insert the data into the table
        cursor.execute("INSERT INTO Classes (CRN, SUBJECT, COURSE, DAYS, TIME, PROFESSOR) VALUES (%s, %s, %s, %s, %s, %s)", var)
        dbs.commit()
    else:
        #otherwise continue
        return 
        


def create_cs_curriculum():
    curriculumn = get_curriculumn2()
    cursor.execute(
        "CREATE TABLE cs_curriculumn (course VARCHAR(10) PRIMARY KEY, title VARCHAR(75), credits SMALLINT, prerequisite VARCHAR(15), year SMALLINT)"
    )
    cursor.executemany(
        "INSERT INTO cs_curriculumn (course, title, credits, prerequisite, year) VALUES (%s, %s, %s, %s, %s)",
        curriculumn,
    )
    dbs.commit()
    cursor.execute(
        "UPDATE cs_curriculumn SET prerequisite = 'CS 120' WHERE course='CS 201'"
    )
    cursor.execute(
        "UPDATE cs_curriculumn SET course='HIST 103' WHERE course='HIST 101'"
    )
    cursor.execute("SELECT * FROM cs_curriculumn")
    val = cursor.fetchall()
    print(val)


def find_classes(g_num, web_pin, semester, year):

    # enter bannerweb and login
    driver.get("https://ssb-prod.ec.gram.edu/PROD/twbkwbis.P_GenMenu?name=homepage")
    driver.find_element(
        By.XPATH, "/html/body/div[3]/table[1]/tbody/tr[1]/td[2]/a"
    ).click()

    user_id = driver.find_element(By.XPATH, '//*[@id="UserID"]')
    user_id.send_keys(g_num)

    pin = driver.find_element(By.XPATH, '//*[@id="PIN"]')
    pin.send_keys(web_pin)
    pin.send_keys(Keys.ENTER)

    # navigate to the lookup page
    driver.find_element(
        By.XPATH, "/html/body/div[3]/table[1]/tbody/tr[3]/td[2]/a"
    ).click()
    driver.find_element(
        By.XPATH, "/html/body/div[3]/table[1]/tbody/tr[2]/td[2]/a"
    ).click()
    driver.find_element(
        By.XPATH, "/html/body/div[3]/table[1]/tbody/tr[4]/td[2]/a"
    ).click()

    # find the specific semester and enter the page

    # convert year and semester to array with formatting used in website
    requested = [year, semester.title()]
    print(requested)
    xpath = driver.find_element(
        By.XPATH, "/html/body/div[3]/form/table/tbody/tr/td/select/option[2]"
    )
    "/html/body/div[3]/form/table/tbody/tr/td/select/option[2]"
    semester = xpath.text.split()[:2]
    print(semester)

    if semester == requested:
        xpath = driver.find_element(
            By.XPATH, "/html/body/div[3]/form/table/tbody/tr/td/select/option[2]").click()

    else:
        xpath = driver.find_element(
            By.XPATH, "/html/body/div[3]/form/table/tbody/tr/td/select/option[3]"
        ).click()

    driver.find_element(By.XPATH, "/html/body/div[3]/form/input[2]").click()


def specific_times(chosen):
    res = {}
    for elem in chosen:
        sub = elem.split()
        option_element = driver.find_element(
            By.CSS_SELECTOR, f"option[value='{sub[0]}']"
        ).click()
        search = driver.find_element(
            By.XPATH, "/html/body/div[3]/form/input[17]"
        ).click()

        # This is for finding the class number e.g Hist 104... we'll be looking for the number 104
        # Also implemented the driver wait function for
        class_num = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, f'//td[text()="{sub[1]}"]'))
        )

        # this is for navigating back to the parent node (which is the same row where there is the number we were looking for and the "submit" button.
        parent_row = class_num.find_element(By.XPATH, "ancestor::tr")

        # this is the "submit" button we need to click after finding the number.
        button = parent_row.find_element(By.XPATH, ".//input[@type='submit']").click()

        # collecting CRN, DAYS, TIM, and professor
        table = driver.find_element(By.XPATH, "/html/body/div[3]/form/table/tbody")

        rows = table.find_elements(By.TAG_NAME, "tr")[2:]
        # res[elem] = []

        for row in rows:
            CRN = row.find_element(By.XPATH, ".//td[2]").text
            DAYS = row.find_element(By.XPATH, ".//td[9]").text
            TIME = row.find_element(By.XPATH, ".//td[10]").text
            PROF = row.find_element(By.XPATH, ".//td[20]").text
            # res[elem].append([CRN,DAYS,TIME,PROF])

        for i in range(3):
            driver.back()
        driver.find_element(By.XPATH, "/html/body/div[3]/form/input[2]").click()

    return res


def all_times():
    data_cell = driver.find_element(
        By.XPATH, "/html/body/div[3]/form/table[1]/tbody/tr/td[2]"
    )
    rows = data_cell.find_elements(By.TAG_NAME, "option")

    for i in range(len(rows)):
        data_cell = driver.find_element(
            By.XPATH, "/html/body/div[3]/form/table[1]/tbody/tr/td[2]"
        )
        row = data_cell.find_elements(By.TAG_NAME, "option")[i]
        row.click()
        search = driver.find_element(
            By.XPATH, "/html/body/div[3]/form/input[17]"
        ).click()
        course_list_table = driver.find_element(
            By.XPATH, "/html/body/div[3]/table[2]/tbody"
        )

        # Find an element with an attribute "value" equal to "your_value"
        buttons = course_list_table.find_elements(
            By.CSS_SELECTOR, '[value="View Sections"]'
        )
        courses = len(buttons)

        # course_rows = course_list_table.find_elements(By.TAG_NAME,"tr")[2:]

        # course_rows[0].find_element(By.XPATH,"/html/body/div[3]/table[2]/tbody/tr[3]/td[3]/form/input[30]").click()

        for i in range(len(buttons)):
            course_list_table = driver.find_element(
                By.XPATH, "/html/body/div[3]/table[2]/tbody"
            )
            course_list_table.find_elements(By.CSS_SELECTOR, '[value="View Sections"]')[
                i
            ].click()
            table = driver.find_element(By.XPATH, "/html/body/div[3]/form/table/tbody")

            rows = table.find_elements(By.TAG_NAME, "tr")[2:]

            for row in rows:
                CRN = row.find_element(By.XPATH, ".//td[2]").text
                SUBJ = row.find_element(By.XPATH, ".//td[3]").text
                COURSE = row.find_element(By.XPATH, ".//td[4]").text
                DAYS = row.find_element(By.XPATH, ".//td[9]").text
                TIME = row.find_element(By.XPATH, ".//td[10]").text
                PROF = row.find_element(By.XPATH, ".//td[20]").text.split("(")[0]
                if TIME == "TBA":
                    DAYS = "ONLINE"
                res = (CRN, SUBJ, COURSE, DAYS, TIME, PROF)
                create_course(res)
                print("This data has been entered to the database:", res)
            driver.back()
        driver.back()
        driver.back()
        driver.find_element(By.XPATH, "/html/body/div[3]/form/input[2]").click()


if __name__ == "__main__":
    find_classes("G00450781", "838383", "spring", "2025")
    all_courses = all_times()

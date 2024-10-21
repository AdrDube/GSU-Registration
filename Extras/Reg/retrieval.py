from selenium import webdriver
from selenium.webdriver.common.by import By
def get_curriculumn2():
    """
    Retrieves an array of courses taken in a subjects.

    The returned 2D array contains courses in the format:
    [title, details, credits, prerequisite].
    :return: A list of courses taken.
    :rtype: 2D list
    """
    driver = webdriver.Chrome()
    driver.get("https://www.gram.edu/academics/majors/arts-and-sciences/compsci/curriculum/")
    #curriculumn=[]
    subjects=[]
    for year in range(1,5):
        if year==1:
            courses = driver.find_element(By.CSS_SELECTOR, "[data-title='Freshman Year']").text.split("\n")
            hrs= driver.find_element(By.CSS_SELECTOR, "[data-title='Hrs.']").text.split("\n")
        elif year==2:
            courses = driver.find_element(By.CSS_SELECTOR, "[data-title='Sophomore Year']").text.split("\n")
            hrs= driver.find_elements(By.CSS_SELECTOR, "[data-title='Hrs.']")[1].text.split("\n")
        elif year==3:
            courses = driver.find_elements(By.CSS_SELECTOR, "[data-title='Freshman Year']")[4].text.split("\n")
            hrs= driver.find_elements(By.CSS_SELECTOR, "[data-title='Hrs.']")[6].text.split("\n")
        else:
            courses = driver.find_elements(By.CSS_SELECTOR, "[data-title='Sophomore Year']")[3].text.split("\n")
            hrs= driver.find_elements(By.CSS_SELECTOR, "[data-title='Hrs.']")[7].text.split("\n")
            for i in range(4):
                courses.pop()
        for i in range(len(courses)):
            courses[i] = courses[i].split("(")
            if len(courses[i])==2:
                prereq=courses[i].pop().split()[1:3]
                prereq= " ".join(prereq)
                courses[i]=courses[i][0].split()
                subjects.append([' '.join(courses[i][:2]), ' '.join(courses[i][2:]), hrs[i], prereq[:len(prereq)-1], year])
            else:
                courses[i]=courses[i][0].split()
                subjects.append([' '.join(courses[i][:2]), ' '.join(courses[i][2:]), hrs[i], "None", year])
    return subjects


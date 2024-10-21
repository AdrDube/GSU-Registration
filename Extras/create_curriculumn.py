from Reg import get_curriculumn2
import mysql.connector
'''
Once off code to extract curriculumn from webpage and add it to our remote database in AWS
Can be modified to help create curriculumn for other courses

Step1 - extract curriculumn from website
      - ensure the package Reg is available first
      - program has been moved to ensure readablity

Step2 - place data inside our DB
'''
import mysql.connector
import os
from dotenv import dotenv_values
env = os.path.join('.env')
secrets = dotenv_values(env)
dbs = mysql.connector.connect(host=secrets["mysql_host"], 
                              user=secrets["mysql_user"],
                              password=secrets["mysql_password"], 
                              database=secrets["mysql_database"])
cursor=dbs.cursor()  
curriculumn= get_curriculumn2()
cursor.execute("DROP TABLE cs_curriculumn")
cursor.execute("CREATE TABLE cs_curriculumn (course VARCHAR(10) PRIMARY KEY, title VARCHAR(75), credits SMALLINT, prerequisite VARCHAR(15), year SMALLINT)")
cursor.executemany("INSERT INTO cs_curriculumn (course, title, credits, prerequisite, year) VALUES (%s, %s, %s, %s, %s)",curriculumn )
dbs.commit()


cursor.execute("UPDATE cs_curriculumn SET prerequisite = 'CS 120' WHERE course='CS 201'")
cursor.execute("SELECT * FROM cs_curriculumn WHERE course='CS 201'")
val=cursor.fetchall()
print(val)

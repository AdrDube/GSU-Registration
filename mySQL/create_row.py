import mysql.connector
from dotenv import dotenv_values

secrets = dotenv_values(".env")

try:
    dbs = mysql.connector.connect(
        host=secrets["mysql_host"],
        user=secrets["mysql_user"],
        password=secrets["mysql_password"],
        database=secrets["mysql_database"],
        port=secrets["port"]
    )
    cursor=dbs.cursor()
    print("Connection successful")
except mysql.connector.Error as err:
    print(f"Error: {err}")

dbs = mysql.connector.connect(host = secrets["mysql_host"],
                              port = secrets["port"], 
                              user = secrets["mysql_user"],
                              password = secrets["mysql_password"],
                              database = secrets["mysql_database"])
cursor = dbs.cursor()


'''
def add_works_info(reg_username, reg_password):
    
    cursor.execute("INSERT INTO students (username,password) VALUES (%s, %s)", (reg_username, reg_password))
    dbs.commit()
    return cursor.lastrowid

def add_web_info(id, g_num, web_pin):
    cursor.execute("UPDATE students SET g_num=%s, web_pin=%s WHERE id= %s", (g_num, web_pin, id) )
    return id

def is_valid_login(username, attempt):
    cursor.execute("SELECT password, id FROM students WHERE username=%s", (username,))
    passwords = cursor.fetchall()
    for password in passwords:
        if password[0] == attempt:
            True
    return False
'''

def val_in_dbs(reg_username, reg_password):
    cursor.execute("SELECT username FROM students WHERE (username,password)= (%s, %s)", (reg_username, reg_password))
    val=cursor.fetchall()
    if val:
        return True
    return False
    

import mysql.connector
import os
from dotenv import dotenv_values


env = os.path.join(os.path.dirname(__file__), '..', '.env')
secrets = dotenv_values(env)
dbs = mysql.connector.connect(
    host=secrets["mysql_host"],
    user=secrets["mysql_user"],
    password=secrets["mysql_password"],
    database=secrets["mysql_database"],
    port=secrets["port"]
)


cursor = dbs.cursor()

def taken_info(taken):
    taken_courses = []
    for course in taken:
        cursor.execute("SELECT * FROM cs_curriculumn WHERE course=%s", (course,))
        val = cursor.fetchone()
        if not val:
            continue
        taken_courses.append(val)
    return taken_courses

def get_remaining(taken):
    placeholders = ', '.join(['%s'] * len(taken))
    query = f"SELECT course FROM cs_curriculumn WHERE course NOT IN ({placeholders}) ORDER BY year"
    cursor.execute(query, tuple(taken))
    remaining = cursor.fetchall()
    return [i[0] for i in remaining]

'''def get_works_info(name, password):
    """
    Takes id of the data from table students in mySQL.

    Returns the tuple username and password.

    :param id: id of the data required.
    :type id: int

    :return: tuple consisting of the corresponding username and password.
    :rtype: tuple
    """
    cursor.execute("SELECT username,password  FROM students WHERE id=%s", (id,))
    val=cursor.fetchone()
    return val
'''


from cryptography.fernet import Fernet
cipher = Fernet(secrets["cipher"].encode('utf-8'))
cursor.execute("SELECT * FROM students")
val=cursor.fetchall()
for i in val:
    print(cipher.decrypt(i[2]).decode())
    print(cipher.decrypt(i[3]).decode())



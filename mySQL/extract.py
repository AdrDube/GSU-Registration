import mysql.connector
import os
from dotenv import dotenv_values


env = os.path.join(os.path.dirname(__file__), '..', '.env')
secrets = dotenv_values(env)

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





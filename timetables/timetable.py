import mysql.connector
import os
from dotenv import dotenv_values
env = os.path.join(os.path.dirname(__file__), '..', '.env')
secrets = dotenv_values(env)

dbs=mysql.connector.connect(host=secrets["mysql_host"],
                            port=secrets["port"],   
                            user=secrets["mysql_user"],
                            password=secrets["mysql_password"], 
                            database=secrets["mysql_database"])

cursor=dbs.cursor()

return_array=[]
chosen = [["BIOL", "113"], ["CS", "110"], ["CS", "120"], ["HIST", "104"], ["ENG", "101"]]



def create_timetable(chosen):
   
    #retrieve the credits in cs_curriculumn for the individual classes and store them in an array
    credits=[]
    for subject in chosen:
        cursor.execute("SELECT credits FROM cs_curriculumn WHERE course=%s", [' '.join(subject),])
        credits.append(cursor.fetchone()[0])
    print(credits)

    
    index = 0
    def dfs(index, timetable, total=0):
        #base cases-> timetable full, EOF

        if total>=12:
            return_array.append(timetable.copy())

        if index==len(chosen) or total > 18 or len(return_array) > 10:
            return
        #dfs algorithm to create the suitable timetable starting from index 0
        cursor.execute("SELECT CRN, DAYS, TIME FROM Classes WHERE SUBJECT= %s AND COURSE = %s", [chosen[index][0], chosen[index][1]])
        val=cursor.fetchall()
        for i in val:
            clash=False
            for j in timetable:
                #TODO check if time conflicts with any of the selected courses
                # if it conlicts do not add i to timetable
                pass
            if not clash:
                timetable.append(i[0])
                credits_to_add= credits[index]

            dfs(index + 1, timetable, total+credits_to_add)
            timetable.pop()
    dfs(0, [])

create_timetable(chosen)
print(return_array)
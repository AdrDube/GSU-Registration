import mysql.connector
from dotenv import dotenv_values
import os
from datetime import datetime
from collections import defaultdict


result = set()
env = os.path.join(os.path.dirname(__file__), '..', '.env')
secrets = dotenv_values(env)

dbs = mysql.connector.connect(host=secrets["mysql_host"], 
                              port = secrets["port"],
                              user=secrets["mysql_user"],
                              password=secrets["mysql_password"],
                              database=secrets["mysql_database"])
cursor = dbs.cursor()
query = "select * from Classes where SUBJECT = %s AND COURSE = %s"


def convert_time(time_range):
    """
    Convert a time range string into a tuple of datetime.time objects.

    Args:
        - time_range (str): Time range in the format "hh:mm am-hh:mm am/pm" 
          (e.g., "08:00 am-08:50 am").

    Returns:
        tuple: A tuple of (start_time, end_time), where each is a datetime.time object.
        It will return something that can be used to make the comparison cleaner and easier
    """
    if time_range == "TBA":
        return ("TBA",)
    start_str, end_str = time_range.split('-') 
    
    start_time = datetime.strptime(start_str, "%I:%M %p").strftime("%H:%M")
    end_time = datetime.strptime(end_str, "%I:%M %p").strftime("%H:%M")
    
    return (start_time, end_time)

def retrieve_offered_classes(lst, convert=True):
    result = defaultdict(list)
    for subj in lst:
        query = "select CRN, DAYS, TIME from Classes where SUBJECT = %s AND COURSE = %s"
        try:
            split_subj= subj.split()
            cursor.execute(query, (split_subj[0], split_subj[1]))
            val = cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving data for {subj}: {e}")
            continue
        
        for elem in val:
            elem = list(elem)
            if convert: elem[2] = convert_time(elem[2])
            result[subj].append((elem))
    return result

def retrieve_classes_website(classes_taken):
    """_summary_
    Args:
        lst (list): a list of subjects in the format ["BIOL 115", "CHEM 209"]
    Returns:
        defaultdict(list): the subject and its corresponding CRNs, Days and Times, Professor
    """
    return retrieve_offered_classes(classes_taken, convert=False)


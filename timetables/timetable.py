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



def days_conflict(days1, days2):
    """
    Check if the current class conflicts in days with any class in the timetable.

    Args:
        - current_class_days (str): Days of the current class (e.g., "MWF", "TR"). 
        this will the element on second indx of the current tuple of a class offering. 
        e.g (12334,"TR","10:00 am-10:50 am")
        
        - timetable_days (str): List of tuples of classes already selected. Each 
        tuple will contain CRN, DAYS, TIME (e.g (14212,"MWF","08:00 am-08:50 am'))

    Returns:
        bool: True if there's a conflict, False otherwise.
    """
    
    if days1 == "ONLINE" or days2=="ONLNE" or  not(set(days1) & set(days2)):
        return False
    return True

def time_conflict(conv_time,conv_sched_time):
    """Function serves to check if there are any conflicts between two classes 

    Args:
        - time (tuple): it is the tuple for the current class we will be checking.
        The tuple will have two variables, a start time and end time
        
        - sched_time (tuple): this will be a tuple for the class that will already 
        be in the time table. The tuple will have three variables, CRN, day and time. 
        we will use the time variable which will be a tuple with two variables,
        start and end time. E.g (14772, "MWF",(datetime.time(9, 30), datetime.time(10, 50)) 

    Returns:
        bool: False if there is no conflict, True otherwise
    """
    if conv_time == ("TBA",) or conv_sched_time == ("TBA",):
        return False
    print(conv_time)
    print(conv_sched_time)
    # Check for overlap
    start1, end1 = conv_time
    start2, end2 = conv_sched_time
        
    return not (end1 <= start2 or end2 <= start1)          

def clash(schedule, crn, subject, days, converted_time):
    if crn in schedule:
        return (True, "CRN already in your schedule")
    for course in schedule.values():
        if course["subject"]==subject:
            return (True, "Course already in your schedule")
        print(course["converted_time"])
        if days_conflict(course["days"], days) and time_conflict(converted_time, course["converted_time"]):
            return (True, f"Conflit with {course['subject']}")
    return (False, "Course successfully added")
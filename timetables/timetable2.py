
def days_conflict(days, timetable):
    """
    Check if the current class conflicts in days with any class in the timetable.

    Args:
        - current_class_days (str): Days of the current class (e.g., "MWF", "TR"). 
        this will the element on second indx of the current tuple of a class offering. 
        e.g (12334,"TR","10:00 am-10:50 am")
        
        - timetable_days (list): List of tuples of classes already selected. Each 
        tuple will contain CRN, DAYS, TIME (e.g (14212,"MWF","08:00 am-08:50 am'))

    Returns:
        bool: True if there's a conflict, False otherwise.
    """
    
    if days == "Online" or timetable == []:
        return False
    
    for subj in timetable:
        if subj[1] != "Online" and set(days) & set(subj[1]):
            return True 

    return False 

def time_conflict(time,sched_time):
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
    if time == ("TBA",):
        return False
    
    sched_time_range = sched_time[2]  # (start_time, end_time)

    # Check for overlap
    start1, end1 = time
    start2, end2 = sched_time_range
        
    return not (end1 <= start2 or end2 <= start1)          

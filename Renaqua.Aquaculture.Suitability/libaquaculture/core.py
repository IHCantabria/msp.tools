# Standard libs:
import json
from datetime import timedelta


# Functions:
def read_conf(file_name):
    """Read configuration, and return it as dictionary."""
    
    with open(file_name) as f:
        conf = json.load(f)
        
    return conf


def wednesdays_between(start_date, end_date):
    """Returns a list of datetime() objects, representing all the Wednesdays
    between start_date and end_date, including.
    """
    # 'd' is the amount of days to add to start_date to get the first Wednesday on the list.
    # If current weekday (w) is 2 (wednesday), then d = 0, obviously. For any other value of w,
    # d will be the number of days until next Wednesday... which one can realize is given
    # by the formula below:
    w = start_date.weekday()
    d = (9 - w) % 7

    # Build list of Wednesdays:
    wlist = []
    wednesday = start_date + timedelta(days=d)
    while wednesday <= end_date:
        wlist.append(wednesday)
        wednesday += timedelta(days=7)

    return wlist

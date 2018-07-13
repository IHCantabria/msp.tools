# Standard libs:
import json


# Functions:
def read_conf(file_name):
    """Read configuration, and return it as dictionary."""
    
    with open(file_name) as f:
        conf = json.load(f)
        
    return conf


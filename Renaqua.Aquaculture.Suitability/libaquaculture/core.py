# Standard libs:
import sys
import json
import argparse
from datetime import timedelta


# Functions:
def parse_args(args=sys.argv[1:]):
    """Read and parse arguments"""

    parser = argparse.ArgumentParser()

    parser.add_argument("-x", "--longitude",
                        help="Longitude of point to check. Default: None.",
                        type=float,
                        default=None)

    parser.add_argument("-y", "--latitude",
                        help="Latitude of point to check. Default: None.",
                        type=float,
                        default=None)

    parser.add_argument("-d", "--depth",
                        help="Depth of point to check. Default: 0.0.",
                        type=float,
                        default=0.0)

    return parser.parse_args(args)


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


def days_between(start_date, end_date):
    """Returns a list of datetime() objects, representing all the days
    between start_date and end_date, including.
    """
    dlist = []
    day = start_date
    while day <= end_date:
        dlist.append(day)
        day += timedelta(days=1)

    return dlist

def closest_index(value, values):
    """Returns index in array 'values', corresponding to the value closest to 'value'."""

    # Use decorate-sort-undecorate:
    return sorted([(abs(v-value), i) for i, v in enumerate(values)])[0][1]


def confine_to_0_360(n):
    """Return number 'n' confined to (0, 360).
    E.g.:
    33 -> 33
    370 -> 10
    -20 -> 340
    """
    return n % 360


def confine_to_plus_minus_90(n):
    """Return number 'n' confned to (-90, 90).
    E.g.:
    33 -> 33
    100 -> -80
    -110 -> 70

    Notice how we use '89.99' and not '90', so that the edge case n=90
    be translated to 90, and not -90.
    """
    return (n + 89.99) % 180 - 89.99


def confine_to_plus_minus_180(n):
    """Return number 'n' confned to (-180, 180).
    E.g.:
    33 -> 33
    100 -> -80
    -110 -> -110
    -200 -> 160

    Notice how we use '179.99' and not '180', so that the edge case n=180
    be translated to 180, and not -180.
    """
    return (n + 179.99) % 360 - 179.99

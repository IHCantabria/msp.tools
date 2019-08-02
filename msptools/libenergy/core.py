# Standard libs:
import argparse
from datetime import datetime
import json


# Functions:
def parse_args(args):
    """Read and parse arguments"""

    parser = argparse.ArgumentParser()

    parser.add_argument("-x", "--longitude",
                        help="Longitude of point. Default: None.",
                        type=float,
                        default=None)

    parser.add_argument("-y", "--latitude",
                        help="Latitude of point. Default: None.",
                        type=float,
                        default=None)

    parser.add_argument("--start",
                        help="Starting date of period to consider (in YYYY-MM-DD format). Default: None.",
                        type=str,
                        default=None)

    parser.add_argument("--end",
                        help="Ending date of period to consider (in YYYY-MM-DD format). Default: None.",
                        type=str,
                        default=None)

    parser.add_argument("--hs-max",
                        help="The maximum threshold significant wave height for the wind resource. Default: None.",
                        type=float,
                        default=None)

    opts = sanitize_args(parser.parse_args(args))

    ranges = {
        "hs_max": opts.hs_min
    }
    point = {
        "lon": opts.longitude,
        "lat": opts.latitude
    }
    dates = {
        "start": opts.start,
        "end": opts.end
    }
    return ranges, point, dates


def sanitize_args(opts):
    """Make sure all required options are passed, and in the correct format."""

    # Check coordinates:
    if opts.longitude is None or opts.latitude is None:
        raise ValueError(
            "Both latitude and longitude must be provided.")

    # Check if identifier is given:

    if opts.hs_max is None:
        raise ValueError(
            "It is required to provide all suitable ranges of variables for the wind resource.")

    # Check if period is correctly given:
    try:
        opts.start = datetime.strptime(opts.start, "%Y-%m-%d")
        opts.end = datetime.strptime(opts.end, "%Y-%m-%d")
        opts.end = opts.end.replace(hour=23, minute=59, second=59)
    except ValueError:
        raise ValueError(
            "Invalid start or end data format. Remember they must be in YYYY-MM-DD format.")
    except TypeError:
        raise TypeError("Remember both start and end date must be given.")

    return opts


def parse_input_web(params):
    """Date is converted, the rest of parameters have correct format
    {
        'config': {
            'hs_max': 5,
        },
        'point': {'lon': -13.016, 'lat': 28.486},
        'dates': {
            'start': '2015-01-01',
            'end': '2015-03-01',
        }
    }
    """
    input_data = sanitize_input_web(params)

    return input_data["point"], input_data["dates"], input_data["config"]


def sanitize_input_web(params):
    # Check coordinates:
    try:
        if params["point"]["lon"] is None or params["point"]["lat"] is None:
            raise ValueError("Both latitude and longitude must be provided.")
    except KeyError:
        raise ValueError("Both latitude and longitude must be provided.")
    # Check if identifier is given:

    try:
        if params["config"]["hs_min"] is None or params["config"]["hs_max"] is None:
            raise ValueError(
                "It is required to provide all suitable ranges of variables for resource.")
    except KeyError:
        raise ValueError(
            "It is required to provide all suitable ranges of variables for resource.")
    # Check if period is correctly given:
    try:
        params["dates"]["start"] = datetime.strptime(
            params["dates"]["start"], "%Y-%m-%d")
        params["dates"]["end"] = datetime.strptime(
            params["dates"]["end"], "%Y-%m-%d")
        params["dates"]["end"] = params["dates"]["end"].replace(
            hour=23, minute=59, second=59)
    except KeyError:
        raise ValueError(
            "Invalid start or end data format. Remember they must be in YYYY-MM-DD format.")
    except ValueError:
        raise ValueError(
            "Invalid start or end data format. Remember they must be in YYYY-MM-DD format.")
    except TypeError:
        raise TypeError("Remember both start and end date must be given.")

    return params


def build_windresource_conf(opts):
    """Build a configuration dictionary for windresource,
    from user-introduced command-line arguments.
    """
    return {
        "hs_max": opts.hs_max,
    }

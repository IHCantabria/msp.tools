# Standard libs:
import sys
import json
import argparse
from scipy.interpolate import interp1d
from datetime import timedelta, datetime


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

    parser.add_argument("--id",
                        help="Identifier of biological species. Default: None.",
                        default=None)

    parser.add_argument("--start",
                        help="Starting date of period to consider (in YYYY-MM-DD format). Default: None.",
                        type=str,
                        default=None)

    parser.add_argument("--end",
                        help="Ending date of period to consider (in YYYY-MM-DD format). Default: None.",
                        type=str,
                        default=None)

    parser.add_argument("--name",
                        help="Name of biological species (if ID not used). Default: None.",
                        type=str,
                        default=None)

    parser.add_argument("--temperature-min",
                        help="Minimum temperature the biological species likes (if ID not used). Default: None.",
                        type=float,
                        default=None)

    parser.add_argument("--temperature-max",
                        help="Maximum temperature the biological species likes (if ID not used). Default: None.",
                        type=float,
                        default=None)

    parser.add_argument("--salinity-min",
                        help="Minimum salinity the biological species likes (if ID not used). Default: None.",
                        type=float,
                        default=None)

    parser.add_argument("--salinity-max",
                        help="Maximum salinity the biological species likes (if ID not used). Default: None.",
                        type=float,
                        default=None)

    return parser.parse_args(args)


def sanitize_options(opts):
    """Make sure all required options are passed, and in the correct format."""

    # Check coordinates:
    if opts.longitude is None or opts.latitude is None:
        raise ValueError("Both latitude and longitude must be provided! Exiting...")

    if opts.depth < 0:
        raise ValueError("Invalid depth value. Depth value must be a positive number. e.g Depth 20 = -20")

    # Check if identifier is given:
    if opts.id is None:
        if opts.temperature_min is None or opts.temperature_max is None or opts.salinity_min is None \
                or opts.salinity_max is None or opts.name is None:
            msg = "You need to provide either an ID for the biological species, "
            msg += "or all of its growth characteristics! Exiting..."
            raise ValueError(msg)
    else:  # the user did introduce the ID
        if opts.temperature_min is not None or opts.temperature_max is not None or \
                opts.salinity_min is not None or  opts.salinity_max is not None or opts.name is not None:
            # Then the user introduced the characteristics of the species by hand, too
            # which should not happen. It's either one or the other.
            msg = "You must provide either an ID or a set of characteristics, not both."
            raise ValueError(msg)

    # Check if period is correctly given:
    try:
        opts.start = datetime.strptime(opts.start, "%Y-%m-%d")
        opts.end = datetime.strptime(opts.end, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid start or end data format. Remember they must be in YYYY-MM-DD format.")
    except TypeError:
        raise TypeError("Remember both start and end date must be given.")

    return opts


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
    """Returns a list of datetime() objects, representing all the days between start_date
    and end_date, including.
    """
    # Build day list:
    dlist = []
    day = start_date
    while day <= end_date:
        dlist.append(day)
        day += timedelta(days=1)

    return dlist


def months_between(start_date, end_date):
    """Returns a list of 'YYYY.MM' strings, representing all the months included within,
    or touched by, the period between start_date and end_date.
    """
    mlist = []
    day = start_date
    while day <= end_date:
        mlist.append(day.strftime("%Y.%m"))
        day += timedelta(days=1)

    return sorted(set(mlist))


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
    """Return number 'n' confined to (-90, 90).
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


def fill_temporal_gaps(period, data):
    """Fill gaps: dates in 'period' for which there is no value in 'data'.
    Return filled-in data.
    """
    # First check if data covers period (lest we try to extrapolate, which we can't do).
    # If lowest date in period is below data, use lowest data point, and if highest date
    # in period is above data, use highest data point.
    lowest_in_period = period[0]
    lowest_in_data = sorted(data.keys())[0]
    if lowest_in_period < lowest_in_data:
        data[lowest_in_period] = data[lowest_in_data]

    highest_in_period = period[-1]
    highest_in_data = sorted(data.keys())[-1]
    if highest_in_period > highest_in_data:
        data[highest_in_period] = data[highest_in_data]

    # Gather X,Y to interpolate to:
    X, Y = [], []
    for day, value in sorted(data.items()):
        x = day.timestamp()
        X.append(x)
        Y.append(value)

    # Generate interpolator, and perform interpolation:
    new_data = {}
    interpolator_function = interp1d(X, Y)
    for day in period:
        x = day.timestamp()
        s = interpolator_function(x)
        new_data[day] = s

    return new_data


def get_correct_species_conf(species_conf_file, opts):
    """Return the correct species_conf dictionary,
    either by reading from the JSON config file,
    or from user-provided options.
    """
    if opts.id is None:
        return build_species_conf(opts)
    else:
        return read_conf(species_conf_file)[opts.id]


def build_species_conf(opts):
    """Build a configuration dictionary for a species,
    from user-introduced command-line arguments.
    """
    return {
        "name": opts.name,
        "temperature_min": opts.temperature_min,
        "temperature_max": opts.temperature_max,
        "salinity_min": opts.salinity_min,
        "salinity_max": opts.salinity_max,
    }

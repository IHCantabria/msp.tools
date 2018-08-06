# Standard libs:
from datetime import datetime

# Our libs:
from libaquaculture import core
from libaquaculture import ihdata
from libaquaculture import biology


# Globals:
CONF_FILE = "conf/RenaquaAquacultureSuitability.json"
START_DATE = datetime(2012, 7, 1)
END_DATE = datetime(2012, 7, 31)


# Functions:
def main():
    """Main loop."""

    # Read command-line options:
    opts = core.parse_args()

    # Check options:
    if opts.longitude is None or opts.latitude is None:
        print("Both latitude and longitude must be provided! Exiting...")
        exit()

    if opts.id is None:
        print("You need to provide an ID for the biological species! Exiting...")
        exit()

    # Read configuration:
    conf = core.read_conf(CONF_FILE)

    # Salinity:
    wednesdays = core.wednesdays_between(START_DATE, END_DATE)
    salinity_data = {}
    for wednesday in wednesdays:
        salinity_file = ihdata.SalinityFile(conf, wednesday)
        salinity_data[wednesday] = salinity_file.get_salinity_of(opts.longitude, opts.latitude, opts.depth)

    # Temperature:
    days = core.days_between(START_DATE, END_DATE)
    temperature_data = {}
    for day in days:
        temperature_file = ihdata.TemperatureFile(conf, day)
        temperature_data[day] = temperature_file.get_temperature_of(opts.longitude, opts.latitude)

    # Expand salinity (weekly) data to all days. Also, fill missing days (if any) from temperature:
    salinity_data = core.fill_temporal_gaps(days, salinity_data)
    temperature_data = core.fill_temporal_gaps(days, temperature_data)

    # Create Species object:
    species = biology.Species(opts.id)
    #species.salinity_suitability_index(salinity_data.values())


# Main body:
if __name__ == '__main__':
    main()

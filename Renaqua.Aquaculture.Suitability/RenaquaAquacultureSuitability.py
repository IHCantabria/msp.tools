# Standard libs:
from datetime import datetime

# Our libs:
from libaquaculture import core
from libaquaculture import ihdata
from libaquaculture import biology


# Globals:
CONF_FILE = "conf/RenaquaAquacultureSuitability.json"
SPECIES_CONF_FILE = "conf/Species.json"


# Functions:
def main():
    """Main loop."""

    # Read command-line options:
    opts = core.parse_args()

    # Sanitize options:
    opts = core.sanitize_options(opts)

    # Read general configuration, and species configuration:
    conf = core.read_conf(CONF_FILE)
    species_conf = core.read_conf(SPECIES_CONF_FILE)[opts.id]

    # Salinity:
    wednesdays = core.wednesdays_between(opts.start, opts.end)
    salinity_data = {}
    for wednesday in wednesdays:
        salinity_file = ihdata.SalinityFile(conf, wednesday)
        salinity_data[wednesday] = salinity_file.get_salinity_of(opts.longitude, opts.latitude, opts.depth)

    # Temperature:
    days = core.days_between(opts.start, opts.end)
    temperature_data = {}
    for day in days:
        temperature_file = ihdata.TemperatureFile(conf, day)
        temperature_data[day] = temperature_file.get_temperature_of(opts.longitude, opts.latitude)

    # Expand salinity (weekly) data to all days. Also, fill missing days (if any) from temperature:
    salinity_data = core.fill_temporal_gaps(days, salinity_data)
    temperature_data = core.fill_temporal_gaps(days, temperature_data)

    # Create Species object:
    species = biology.Species(species_conf)
    print(species.biological_suitability_index(salinity_data, temperature_data))


# Main body:
if __name__ == '__main__':
    main()

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
    species_conf = core.get_correct_species_conf(SPECIES_CONF_FILE, opts)

    # Salinity:
    wednesdays = core.wednesdays_between(opts.start, opts.end)
    salinities = {}
    for wednesday in wednesdays:
        salinity_file = ihdata.SalinityFile(conf, wednesday)
        if salinity_file.file_url is not None:
            salinities[wednesday] = salinity_file.get_salinity_of(opts.longitude, opts.latitude, opts.depth)

    # Temperature:
    temperature_data = ihdata.TemperatureData(conf)
    days = core.days_between(opts.start, opts.end)
    temperatures = {}
    for day in days:
        temperatures[day] = temperature_data.get_temperature_of(opts.longitude, opts.latitude, day)

    # Expand salinity (weekly) data to all days. Also, fill missing days (if any) from temperature:
    salinities = core.fill_temporal_gaps(days, salinities)
    temperatures = core.fill_temporal_gaps(days, temperatures)

    # Create Species object:
    species = biology.Species(species_conf)
    print(species.biological_suitability_index(salinities, temperatures))


# Main body:
if __name__ == '__main__':
    main()

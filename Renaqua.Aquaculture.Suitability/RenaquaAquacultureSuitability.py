# Standard libs:
from datetime import datetime

# Our libs:
from libaquaculture import core
from libaquaculture import ihdata


# Globals:
CONF_FILE = "conf/RenaquaAquacultureSuitability.json"
START_DATE = datetime(2012, 7, 1)
END_DATE = datetime(2012, 7, 31)
X = 0.0  # longitude
Y = 0.0  # latitude


# Functions:
def main():
    """Main loop."""

    # Read configuration:
    conf = core.read_conf(CONF_FILE)

    # Get list of wednesdays, and operate on them:
    wednesdays = core.wednesdays_between(START_DATE, END_DATE)[:1]
    for wednesday in wednesdays:
        data_nc = ihdata.NCFile(conf, wednesday)
        print(data_nc.file_url)
        print(data_nc.indices_of(X, Y))
        #salinity = data_nc.get_variable("salinity")
        #print(salinity)


# Main body:
if __name__ == '__main__':
    main()

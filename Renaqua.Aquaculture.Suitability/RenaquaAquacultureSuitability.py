# Our libs:
from libaquaculture import core
from libaquaculture import ihdata


# Globals:
CONF_FILE = "conf/RenaquaAquacultureSuitability.json"


# Functions:
def main():
    """Main loop."""

    # Read configuration:
    conf = core.read_conf(CONF_FILE)

    # Instantiate an IHData object:
    thredds_ihdata = ihdata.IHData()
    salinity = thredds_ihdata.get_variable("sea_water_salinity", conf)
    print(salinity)

    #descargar(conf)


# Main body:
if __name__ == '__main__':
    main()

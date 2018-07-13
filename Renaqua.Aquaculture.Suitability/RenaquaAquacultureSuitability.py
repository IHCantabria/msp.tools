# Our libs:
from libaquaculture import ihdata
from libaquaculture import core


# Globals:
CONF_FILE = "conf/RenaquaAquacultureSuitability.json"


# Functions:
def main():
    """Main loop."""

    # Read configuration:
    conf = core.read_conf(CONF_FILE)

    # Instantiate an IHData object:
    thredds_ihdata = ihdata.IHData()
    thredds_ihdata.method_name("salchicha")

    #descargar(conf)


# Main body:
if __name__ == '__main__':
    main()

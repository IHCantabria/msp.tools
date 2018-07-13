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

    print(conf.get('thredds_url_base'))

    #descargar(conf)


# Main body:
if __name__ == '__main__':
    main()

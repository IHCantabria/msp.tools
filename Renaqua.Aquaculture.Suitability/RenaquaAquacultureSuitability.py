# Standard libs:
import json

# Our libs:
from libaquaculture import ihdata


# Globals:
CONF_FILE = "conf/RenaquaAquacultureSuitability.json"


# Functions:
def main():
    with open(CONF_FILE) as f:
        J = json.load(f)

    print(J)
    # qué poner aquí para que imprima la URL?
    #print(thredds_base_url)

    #descargar(conf)


# Main body:
if __name__ == '__main__':
    main()

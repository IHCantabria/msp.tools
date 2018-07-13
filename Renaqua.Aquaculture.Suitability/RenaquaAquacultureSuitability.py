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
    print(J.get('thredds_url_base'))

    # print(J)

    # descargar(conf)


# Main body:
if __name__ == '__main__':
    main()

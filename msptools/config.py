CONFIG = {
    "version": "0.8.5",
    "log": {
        # "filepath": "/var/www/apisctools/log/msp.tools.log",
        "filepath": "msp.tools.log",
        "level": "DEBUG"
    },
    "copernicus": {
        "global_reanalysis_physical": {
            "catalog": "http://thredds.ihcantabria.com/catalog/copernicus/CMEMS/catalog.xml"
        },
        "variables": [
            {
                "name": "thetao",
                "alias": "temperature",
                "units": "°"
            },
            {
                "name": "so",
                "alias": "salinity",
                "units": "psu"
            }
        ],
        "source": {
            "name": "CMEMS",
            "link": "http://marine.copernicus.eu/"
        }
    }

}

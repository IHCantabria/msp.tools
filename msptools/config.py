CONFIG = {
    "log": {
        "filepath": "msp.log",
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

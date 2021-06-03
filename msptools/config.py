CONFIG = {
    "version": "0.11.0",
    "log": {
        # "filepath": "/var/www/apisctools/log/msp.tools.log",
        "filepath": "msp.tools.log",
        "level": "DEBUG",
    },
    "datahub": {
        "urls": {"product": "https://datahub.ihcantabria.com/v1/public/Products/{id}"}
    },
    "copernicus": {
        "global_reanalysis_physical": {
            "catalog": "http://thredds.ihcantabria.com/catalog/copernicus/CMEMS/catalog.xml",
            "id": 7,
        },
        "variables": [
            {"name": "thetao", "alias": "temperature", "units": "°"},
            {"name": "so", "alias": "salinity", "units": "psu"},
        ],
        "source": {"name": "CMEMS", "link": "http://marine.copernicus.eu/"},
    },
    "ECMWF": {
        "ERA_Interim": {
            "catalog": "http://thredds.ihcantabria.com/catalog/era_interim/catalog.xml",
            "id": 20,
        },
        "wave": {
            "variables": [
                {"name": "swh", "alias": "hs", "units": "m"},
                {"name": "pp1d", "alias": "tp", "units": "s"},
                {"name": "mwp", "alias": "tm", "units": "s"},
            ],
        },
        "wind": {
            "variables": [
                {"name": "swh", "alias": "hs", "units": "m"},
                {"name": "u10", "alias": "u10", "units": "m/s"},
                {"name": "v10", "alias": "v10", "units": "m/s"},
            ],
        },
        "source": {
            "name": "ERA_Interim",
            "link": "https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era-interim",
        },
    },
        "specieranges":{
            "European seabass":{
                "name" : "European seabass",
                "salinity_min": 30,
                "salinity_max": 40,
                "temperature_min": 18,
                "temperature_max": 26,
            },
            "Cobia":{
                "name" : "Cobia",
                "salinity_min": 20,
                "salinity_max": 40,
                "temperature_min": 15,
                "temperature_max": 26,
            }
    } 
}
threddsIH = "https://ihthredds.ihcantabria.com/thredds/dodsC/"
CONFIG = {
    "version": "0.9.1",
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
            "catalog": "http://thredds.ihcantabria.com/catalog/era_interim/catalog.xml"
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
}

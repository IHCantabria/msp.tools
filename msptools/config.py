CONFIG = {
    "log": {
        "filepath":"msp.log",
        "level": "DEBUG"
    },
    "copernicus" :{
        "global_reanalysis_physical": {
            "catalog": "http://193.144.208.179:8080/thredds/catalog/copernicus_1/CMEMS/catalog.xml",
            "vars": {
                "temperature": "thetao",
                "salinity": "so"
            }
        }
    }
}
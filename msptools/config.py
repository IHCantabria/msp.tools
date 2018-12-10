CONFIG = {
    "log": {
        "filepath":"msp.log",
        "level": "DEBUG"
    },
    "copernicus" :{
        "global_reanalysis_physical": {
            "catalog": "http://thredds.ihcantabria.com/catalog/copernicus/CMEMS/catalog.xml",
            "vars": {
                "temperature": "thetao",
                "salinity": "so"
            }
        }
    }
}

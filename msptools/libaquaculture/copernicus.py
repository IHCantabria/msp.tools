from msptools.libaquaculture.thredds import Thredds
from msptools.config import CONFIG


def get_temperature_and_salinity_from_global_reanalysis_physical(point, dates):
    """ 
    Thredds request: temperature and salinity data for a specific point and a set period 
    Once received, they are got into another dictionary where key name is known."""

    var_temperature = CONFIG["copernicus"]["global_reanalysis_physical"]["vars"]["temperature"]
    var_salinity = CONFIG["copernicus"]["global_reanalysis_physical"]["vars"]["salinity"]
    variables = [var_temperature, var_salinity]
    url_catalog = CONFIG["copernicus"]["global_reanalysis_physical"]["catalog"]

    thredds = Thredds(url_catalog)
    data_from_thredds = thredds.get_data_in_point_between_dates(point, dates, variables)

    indexes = list(data_from_thredds.keys())
    data = {}
    for index in indexes:
        data[index] = {}
        data[index]["temperature"] = data_from_thredds[index]["thetao"]
        data[index]["salinity"] = data_from_thredds[index][var_salinity]
    return data

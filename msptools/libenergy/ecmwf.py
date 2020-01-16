import json
import requests
from msptools.libenergy.thredds import Thredds
from msptools.config import CONFIG


def get_url_catalog():
    id_catalog = CONFIG["ECMWF"]["ERA_Interim"]["id"]
    url_datahub = CONFIG["datahub"]["urls"]["product"].format(id=id_catalog)
    response = requests.get(url_datahub)
    if response.ok:
        data = json.loads(response.content)
    else:
        raise response.raise_for_status()
    url_catalog = "{urlBase}{urlXmlLatest}".format(
        urlBase=data[0]["urlBase"], urlXmlLatest=data[0]["urlXmlLatest"]
    )
    return url_catalog


def get_data_from_era_interim(point, dates, variables):
    """
    Thredds request: significant wave  height (hs) data for a specific point and a set period
    Once received, they are got into another dictionary where key name is known."""

    var_names = []
    for variable in variables:
        var_names.append(variable.get("name"))

    url_catalog = get_url_catalog()

    thredds = Thredds(url_catalog)
    data_from_thredds = thredds.get_data_in_point_between_dates(point, dates, var_names)

    indexes = list(data_from_thredds.keys())
    output_data = {}
    for index in indexes:
        output_data = set_output_data(
            index, data_from_thredds[index], variables, output_data
        )

    return output_data


def set_output_data(index, data, variables, output):
    output[index] = {}
    for variable in variables:
        output[index][variable["alias"]] = data[variable["name"]]
    return output

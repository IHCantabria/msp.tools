from datetime import datetime
import json
import requests
from msptools import utils
from msptools.config import CONFIG
from datahub.products import Products
from datahub.variables import Variables
from datahub.thredds import Catalog


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

    p = Products()
    product = p.get(CONFIG["ECMWF"]["ERA_Interim"]["id"])
    v = Variables()
    variables_json = v.get_by_product_filtered_by_name(product, var_names)

    c = Catalog(product)
    dates_str = {
        "start": dates["start"].strftime("%Y-%m-%dT%H:%M:%S"),
        "end": dates["end"].strftime("%Y-%m-%dT%H:%M:%S"),
    }

    data_from_thredds = data_from_thredds = c.data(point, dates_str, variables_json)
    utils.check_land_exception(data_from_thredds, var_names)

    output_data = {}
    for data in data_from_thredds:
        output_data = set_output_data(data["date"], data, output_data, variables)

    return output_data


def set_output_data(index, data, output, variables):
    index_datetime = datetime.strptime(index, "%Y-%m-%dT%H:%M:%SZ")
    output[index_datetime] = {}
    for variable in variables:
        output[index_datetime][variable["alias"]] = data[variable["name"]]
    return output

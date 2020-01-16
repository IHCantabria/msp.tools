from msptools.libenergy.thredds import Thredds
from msptools.config import CONFIG


def get_data_from_era_interim(point, dates, variables):
    """
    Thredds request: significant wave  height (hs) data for a specific point and a set period
    Once received, they are got into another dictionary where key name is known."""

    var_names = []
    for variable in variables:
        var_names.append(variable.get("name"))

    url_catalog = CONFIG["ECMWF"]["ERA_Interim"]["catalog"]

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

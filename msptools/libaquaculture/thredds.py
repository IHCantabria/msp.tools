# Standard libs:
from datetime import datetime
import logging

# Third parties
import pytz
import numpy as np
from siphon.catalog import TDSCatalog

from msptools.utils import LandException
from netCDF4 import num2date

# Classes:


class Thredds(object):
    """Class to manage access to a netCDF file in 'IHData'."""

    # Constructor:
    def __init__(self, url_catalog):
        self.logger = logging.getLogger("msp.aquaculture.thredds")
        self.url_catalog = url_catalog
        self.logger.debug("catalog: {}".format(self.url_catalog))

    # Public methods:
    def get_data_in_point_between_dates(self, point, dates, variables):
        """Request variables for a specific point and a set period from Thredds"""

        try:
            catalog = TDSCatalog(self.url_catalog)
            best_dataset = catalog.datasets[0]
            ncss = best_dataset.subset()
            query = ncss.query()

            query.lonlat_point(point["lon"], point["lat"]).time_range(
                dates["start"], dates["end"]
            )
            query.variables(",".join(variables))
            # Set extra params for performance #
            # query.vertical_level(0.49402499198913574)
            query.accept("netcdf")

            self.logger.debug(
                "thredds query lon: {lon}, lat: {lat}, start: {start}, end: {end}, vars: {vars}".format(
                    lon=point["lon"],
                    lat=point["lat"],
                    start=dates["start"],
                    end=dates["end"],
                    vars=",".join(variables),
                )
            )
            data = ncss.get_data(query)

            scale_factor = {}
            offset = {}
            for variable_name in variables:
                scale_factor[variable_name] = ncss.metadata.variables[variable_name][
                    "attributes"
                ]["scale_factor"][0]
                offset[variable_name] = ncss.metadata.variables[variable_name][
                    "attributes"
                ]["add_offset"][0]

            values = {}
            for i in range(data.variables.get("time").size):
                dictionary_date_variables = {}
                for variable_name in variables:
                    value = float(np.ma.getdata(data[variable_name][0][i], subok=True))
                    if (
                        float(
                            ncss.metadata.variables[variables[0]]["attributes"][
                                "missing_value"
                            ][0]
                        )
                        == value
                    ):
                        raise LandException(
                            "This point is located on land: lon: {lon}, lat: {lat}".format(
                                lon=point["lon"], lat=point["lat"]
                            )
                        )
                    dictionary_date_variables[variable_name] = self.get_real_value(
                        value, scale_factor[variable_name], offset[variable_name]
                    )

                date = num2date(
                    data.variables["time"][0][i],
                    data.variables["time"].units,
                    data.variables["time"].calendar,
                )
                if date.tzinfo is None:
                    date = date.replace(tzinfo=pytz.utc)
                values[date] = dictionary_date_variables
        except LandException as ex:
            self.logger.warning(
                "This point is located on land: lon: {lon}, lat: {lat}".format(
                    lon=point["lon"], lat=point["lat"]
                )
            )
            raise
        except Exception as err:
            self.logger.error("Fatal error in thredds.", exc_info=True)
            raise err

        return values

    def get_real_value(self, value, scale_factor, offset):
        return value * scale_factor + offset

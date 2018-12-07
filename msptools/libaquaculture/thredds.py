# Standard libs:
from datetime import datetime
import logging
# Third parties
from siphon.catalog import TDSCatalog

from msptools.libaquaculture.core import LandException

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

            query.lonlat_point(point['lon'], point['lat']).time_range(dates['start'], dates['end'])
            query.variables(",".join(variables))

            self.logger.debug("thredds query lon: {lon}, lat: {lat}, start: {start}, end: {end}, vars: {vars}".format(
                lon=point["lon"], lat=point["lat"],
                start=dates["start"], end=dates["end"],
                vars=",".join(variables)
            ))
            data = ncss.get_data(query)

            if ncss.metadata.variables[variables[0]]['attributes']['missing_value'] == data[variables[0]][0]:
                raise LandException("This point is located on land: lon: {lon}, lat: {lat}".format(lon=point["lon"], lat=point["lat"]))

            scale_factor = {}
            offset = {}
            for variable_name in variables:
                scale_factor[variable_name] = ncss.metadata.variables[variable_name]['attributes']['scale_factor'][0]
                offset[variable_name] = ncss.metadata.variables[variable_name]['attributes']['add_offset'][0]

            
            values = {}
            for i in range(len(data['date'])):
                dictionary_date_variables = {}
                for variable_name in variables:
                    dictionary_date_variables[variable_name] = self.get_real_value(data[variable_name][i], scale_factor[variable_name], offset[variable_name])

                values[data['date'][i]] = dictionary_date_variables
        except LandException as ex:
            self.logger.warn("This point is located on land: lon: {lon}, lat: {lat}".format(lon=point["lon"], lat=point["lat"]))
            raise
        except Exception as err:
            self.logger.error("Fatal error in thredds.", exc_info=True)
            raise err

        return values

    def get_real_value(self, value, scale_factor, offset):
        return value * scale_factor + offset

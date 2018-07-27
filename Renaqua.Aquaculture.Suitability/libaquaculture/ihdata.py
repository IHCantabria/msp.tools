# Standard libs:
import netCDF4 as nc4


# Classes:
class IHData(object):
    """Class to manage access to 'IHData' netCDFs."""

    # Constructor:
    def __init__(self, conf):
        self.conf = conf

    # Public methods:
    def get_variable(self, var_name):
        """Returns contents of variable 'var_name'."""

        with nc4.Dataset(self.file_url) as nc:
            var = nc.variables[var_name][0, 115, 115]

        return var

    # Public properties:
    @property
    def file_url(self):
        return self.conf["url_file"]


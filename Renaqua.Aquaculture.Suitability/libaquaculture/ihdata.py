# Standard libs:
import netCDF4 as nc4


# Classes:
class IHData(object):
    """Class to manage access to 'IHData' netCDFs."""

    def __init__(self):
        pass  # Empty constructor
    
    def get_variable(self, var_name, conf):
        """Returns contents of variable 'var_name'."""

        fn = conf["url_file"]

        with nc4.Dataset(fn) as nc:
            var = nc.variables.keys()

        return var


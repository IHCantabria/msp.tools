# Standard libs:
import netCDF4 as nc4


# Classes:
class NCFile(object):
    """Class to manage access to a netCDF file in 'IHData'."""

    BATCHES = ["20140420", "20130910"]

    # Constructor:
    def __init__(self, conf, file_date):
        self.conf = conf
        self.date = file_date

    # Public methods:
    def get_variable(self, var_name):
        """Returns contents of variable 'var_name'."""

        with nc4.Dataset(self.file_url) as nc:
            var = nc.variables[var_name][0, 115, 115]

        return var

    # Public properties:
    @property
    def file_url(self):
        """URL of remote netCDF in THREDDS."""

        url = self.conf["url_patt"].format(VAR="salinity", DATE=self.date, BATCH=self.BATCHES[0])

        return url


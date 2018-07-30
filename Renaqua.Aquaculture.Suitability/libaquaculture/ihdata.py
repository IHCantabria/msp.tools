# Standard libs:
import netCDF4 as nc4

# Our libs:
from libaquaculture import core


# Classes:
class NCFile(object):
    """Class to manage access to a netCDF file in 'IHData'."""

    # Constructor:
    def __init__(self, conf, file_date):
        self.conf = conf
        self.date = file_date
        self._file_url = None

    # Public methods:
    def get_variable(self, var_name):
        """Returns contents of variable 'var_name'."""

        with nc4.Dataset(self.file_url) as nc:
            var = nc.variables[var_name][0, 115, 115]

        return var

    def get_lons(self):
        """Returns array with longitudes."""

        with nc4.Dataset(self.file_url) as nc:
            return nc.variables["longitude"][:]

    def get_lats(self):
        """Returns array with latitudes."""

        with nc4.Dataset(self.file_url) as nc:
            return nc.variables["latitude"][:]

    def indices_of(self, lon, lat):
        """Given longitude 'lon' and latitude 'lat', return closest indices (i, j)."""

        lons = self.get_lons()
        lats = self.get_lats()

        i = core.closest_index(lon, lons)
        j = core.closest_index(lat, lats)

        return i, j

    # Public properties:
    @property
    def file_url(self):
        """URL of remote netCDF in THREDDS."""

        if self._file_url is not None:
            return self._file_url

        for batch in self.conf["salinity_batches"]:
            test_url = self.conf["url_patt"].format(VAR="Salinity", DATE=self.date, BATCH=batch)
            if self.exists(test_url):
                self._file_url = test_url
                break

        return self._file_url

    # Static methods:
    @staticmethod
    def exists(url):
        """Return True if file 'url' exists. False otherwise."""

        try:
            with nc4.Dataset(url):
                pass
            return True
        except OSError:
            return False


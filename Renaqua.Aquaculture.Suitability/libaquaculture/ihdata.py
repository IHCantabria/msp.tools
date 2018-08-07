# Standard libs:
import os
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
    def get_depths(self):
        """Returns array with depth values."""

        with nc4.Dataset(self.file_url) as nc:
            return nc.variables["depth"][:]

    def get_depth_index_of(self, depth):
        """Given depth of 'depth' meters, return closest index."""

        depths = self.get_depths()

        return core.closest_index(depth, depths)

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


class SalinityFile(NCFile):
    """An NCFile specifically for salinity."""

    # Constructor:
    def __init__(self, conf, file_date):
        super().__init__(conf, file_date)

    # Public methods:
    def get_variable(self, var_name, i, j, d):
        """Return value of variable 'var_name' at (lon, lat) indices (i, j), and depth index 'd'."""

        with nc4.Dataset(self.file_url) as nc:
            return nc.variables[var_name][d, j, i]

    def get_salinity_of(self, lon, lat, depth):
        """Given a (lon, lat), return salinity."""

        i, j = self.get_indices_of(lon, lat)
        d = self.get_depth_index_of(depth)

        return self.get_variable("salinity", i, j, d)

    def get_indices_of(self, lon, lat):
        """Given longitude 'lon' and latitude 'lat', return closest indices (i, j)."""

        # Confine longitude to (0, 360) and latitude to (-90, 90):
        lon = core.confine_to_0_360(lon)
        lat = core.confine_to_plus_minus_90(lat)

        # Get longitudes and latitudes:
        lons = self.get_longitudes()
        lats = self.get_latitudes()

        # Get corresponding indices for longitudes (i) and latitudes (j):
        i = core.closest_index(lon, lons)
        j = core.closest_index(lat, lats)

        return i, j

    def get_longitudes(self):
        """Returns array with longitudes."""

        with nc4.Dataset(self.file_url) as nc:
            return nc.variables["longitude"][:]

    def get_latitudes(self):
        """Returns array with latitudes."""

        with nc4.Dataset(self.file_url) as nc:
            return nc.variables["latitude"][:]

    # Public properties:
    @property
    def file_url(self):
        """URL of remote netCDF in THREDDS."""

        if self._file_url is None:
            for batch in self.conf["salinity_batches"]:
                test_url = self.conf["salinity_url_pattern"].format(DATE=self.date, BATCH=batch)
                if self.exists(test_url):
                    self._file_url = test_url
                    break

        return self._file_url


class TemperatureFile(NCFile):
    """An NCFile specifically for temperature."""

    # Constructor:
    def __init__(self, conf, file_date):
        super().__init__(conf, file_date)

    # Public methods:
    def get_variable(self, var_name, i, j, t):
        """Return value of variable 'var_name' at (lon, lat) indices (i, j), and time index "t"."""

        with nc4.Dataset(self.file_url) as nc:
            return nc.variables[var_name][j, i, t]

    def get_temperature_of(self, lon, lat):
        """Given a (lon, lat), return temperature."""

        i, j = self.get_indices_of(lon, lat)

        return self.get_variable("sst", i, j, self.time_index)

    def get_indices_of(self, lon, lat):
        """Given longitude 'lon' and latitude 'lat', return closest indices (i, j)."""

        # Confine longitude to (-180, 180) and latitude to (-90, 90):
        lon = core.confine_to_plus_minus_180(lon)
        lat = core.confine_to_plus_minus_90(lat)

        # Get longitudes and latitudes:
        lons = self.get_longitudes()
        lats = self.get_latitudes()

        # Get corresponding indices for longitudes (i) and latitudes (j):
        i = core.closest_index(lon, lons)
        j = core.closest_index(lat, lats)

        return i, j

    def get_longitudes(self):
        """Returns array with longitudes."""

        with nc4.Dataset(self.file_url) as nc:
            return nc.variables["lon"][:]

    def get_latitudes(self):
        """Returns array with latitudes."""

        with nc4.Dataset(self.file_url) as nc:
            return nc.variables["lat"][:]

    # Public properties:
    @property
    def file_url(self):
        """URL of remote netCDF in THREDDS."""

        if self._file_url is None:
            self._file_url = "/".join([self.conf["thredds_url_base"],
                                       self.conf["temperature_url_pattern"].format(DATE=self.date)])

        return self._file_url

    @property
    def time_index(self):
        """Return index in NetCDF, corresponding to current date."""

        return self.date.day - 1





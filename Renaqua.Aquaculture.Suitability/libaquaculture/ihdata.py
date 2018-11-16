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


class TemperatureData(NCFile):

    """An NCFile specifically for temperature. Saves all data, not just a file."""

    # Constructor:
    def __init__(self, conf):
        super().__init__(conf, None)

        # Joins "file_url" and corresponding data. This way, the second and succesive
        # times a given file_url is called, data is taken from here, not collected
        # from THREDDS again:
        self.monthly_data = {}

        # Helpers:
        self._i = None
        self._j = None

    # Public methods:
    def get_sst(self, url, i, j):
        """Return value of variable SST at (lon, lat) indices (i, j),
        for file at URL 'url'.
        """
        with nc4.Dataset(url) as nc:
            # return nc.variables["time"][:]
            return nc.variables["thetao"][:, 0, j, i]

    def get_temperature_of(self, lon, lat, day):
        """Given a (lon, lat) and a date 'day', return corresponding temperature."""

        url = self.file_url(day)

        if url not in self.monthly_data:
            i, j = self.get_indices_of(lon, lat, day)
            self.monthly_data[url] = self.get_sst(self.file_url(day), i, j)
            print(day)

        return self.monthly_data[url][self.time_index(day)]

    def get_indices_of(self, lon, lat, day):
        """Given longitude 'lon' and latitude 'lat', return closest indices (i, j)."""

        if self._i and self._j:
            return self._i, self._j

        lat = core.confine_to_plus_minus_90(lat)

        # Get longitudes and latitudes:
        lons = self.get_longitudes(day)
        lats = self.get_latitudes(day)
        print(lons, lats)

        # Get corresponding indices for longitudes (i) and latitudes (j):
        self._i = core.closest_index(lon, lons)
        self._j = core.closest_index(lat, lats)
        # Get indices and print closest longitudes and latitudes corresponding to indices
        print(lons[self._i], lats[self._j])
        return self._i, self._j

    def get_longitudes(self, day):
        """Returns array with longitudes."""

        with nc4.Dataset(self.file_url(day)) as nc:
            return nc.variables["longitude"][:]

    def get_latitudes(self, day):
        """Returns array with latitudes."""

        with nc4.Dataset(self.file_url(day)) as nc:
            return nc.variables["latitude"][:]

    def file_url(self, day):
        """URL of remote netCDF in THREDDS."""

        return "/".join([self.conf["thredds_url_base"],
                         self.conf["Copernicus"]])

    # Static methods:
    @staticmethod
    def time_index(day):
        """Return index in NetCDF, corresponding to current date."""

        return day.day - 1


class SalinityData(NCFile):
    """An NCFile specifically for salinity. Saves all data, not just a file."""

    # Constructor:
    def __init__(self, conf):
        super().__init__(conf, None)

        # Joins "file_url" and corresponding data. This way, the second and succesive
        # times a given file_url is called, data is taken from here, not collected
        # from THREDDS again:
        self.monthly_data = {}

        # Helpers:
        self._i = None
        self._j = None

    # Public methods:
    def get_salinity(self, url, i, j):
        """Return value of variable salinity at (lon, lat) indices (i, j),
        for file at URL 'url'.
        """
        with nc4.Dataset(url) as nc:
            return nc.variables["so"][:, 0, j, i]

    def get_salinity_of(self, lon, lat, day):
        """Given a (lon, lat) and a date 'day', return corresponding salinity."""

        url = self.file_url(day)

        if url not in self.monthly_data:
            i, j = self.get_indices_of(lon, lat, day)
            self.monthly_data[url] = self.get_salinity(
                self.file_url(day), i, j)

        return self.monthly_data[url][self.time_index(day)]

    def get_indices_of(self, lon, lat, day):
        """Given longitude 'lon' and latitude 'lat', return closest indices (i, j)."""

        if self._i and self._j:
            return self._i, self._j

        lat = core.confine_to_plus_minus_90(lat)

        # Get longitudes and latitudes:
        lons = self.get_longitudes(day)
        lats = self.get_latitudes(day)

        # Get corresponding indices for longitudes (i) and latitudes (j):
        self._i = core.closest_index(lon, lons)
        self._j = core.closest_index(lat, lats)

        return self._i, self._j

    def get_longitudes(self, day):
        """Returns array with longitudes."""

        with nc4.Dataset(self.file_url(day)) as nc:
            return nc.variables["longitude"][:]

    def get_latitudes(self, day):
        """Returns array with latitudes."""

        with nc4.Dataset(self.file_url(day)) as nc:
            return nc.variables["latitude"][:]

    def file_url(self, day):
        """URL of remote netCDF in THREDDS."""

        return "/".join([self.conf["thredds_url_base"],
                         self.conf["Copernicus"]])

    # Static methods:
    @staticmethod
    def time_index(day):
        """Return index in NetCDF, corresponding to current date."""

        return day.day - 1

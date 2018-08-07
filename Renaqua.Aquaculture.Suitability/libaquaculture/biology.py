# Classes:
class Species(object):
    """Description of a given biological species."""

    # Constructor:
    def __init__(self, conf):
        self.conf = conf

    # Public methods:
    def is_salinity_ok(self, salinity):
        """Return True if salinity 'salinity' is adequate for us, False otherwise."""

        return self.salinity_min < salinity < self.salinity_max

    def is_temperature_ok(self, temperature):
        """Return True if temperature 'temperature' is adequate for us, False otherwise."""

        return self.temperature_min < temperature < self.temperature_max

    def biological_suitability_index(self, salinity_series, temperature_series):
        """Return fraction of salinity and temperature values
        in corresponding series that are adequate for us.
        """
        n_ok = 0
        for day in salinity_series:
            s = salinity_series[day]
            t = temperature_series[day]
            if self.is_salinity_ok(s) and self.is_temperature_ok(t):
                n_ok += 1

        return float(n_ok)/len(salinity_series)

    # Public properties:
    @property
    def temperature_min(self):
        """Returns minimum acceptable temperature for species."""

        return self.conf["temperature_min"]

    @property
    def temperature_max(self):
        """Returns maximum acceptable temperature for species."""

        return self.conf["temperature_max"]

    @property
    def salinity_min(self):
        """Returns minimum acceptable salinity for species."""

        return self.conf["salinity_min"]

    @property
    def salinity_max(self):
        """Returns maximum acceptable salinity for species."""

        return self.conf["salinity_max"]

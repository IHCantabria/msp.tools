import logging
# Classes:
class Species(object):
    """Description of a given biological species."""

    # Constructor:
    def __init__(self, conf):
        self.logger = logging.getLogger("msp.aquaculture.biology")
        self.conf = conf
        
    # Public methods:
    def is_salinity_ok(self, salinity):
        """Return True if salinity 'salinity' is adequate for us, False otherwise."""

        return self.salinity_min < float(salinity) < self.salinity_max

    def is_temperature_ok(self, temperature):
        """Return True if temperature 'temperature' is adequate for us, False otherwise."""

        return self.temperature_min < float(temperature) < self.temperature_max

    def biological_suitability_index(self, data_serie):
        """Return fraction of salinity and temperature values
        in corresponding series that are adequate for us.
        """
        n_ok = 0
        dates = sorted(data_serie.keys())
        for day in dates:
            salinity = data_serie[day]['salinity']
            temperature = data_serie[day]['temperature']
            if self.is_salinity_ok(salinity) and self.is_temperature_ok(temperature):
                n_ok += 1
        total = len(data_serie)
        self.logger.debug("num ok: {ok}, total: {total}".format(ok=n_ok, total=total))
        return float(n_ok) / total

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

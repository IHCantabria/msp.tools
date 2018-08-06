# Classes:
class Species(object):
    """Description of a given biological species."""

    # Constructor:
    def __init__(self, identifier, conf):
        self.id = identifier
        self.conf = conf

    # Public methods:
    def salinity_value_ok(self, salinity):
        """Return True if salinity 'salinity' is adequate for us, False otherwise."""

        return self.min_sality < salinity < self.max_sality

    def salinity_suitability_index(self, salinity_series):
        """Return fraction of salinity values in 'salinity_series' that are adequate for us."""

        n_adequate = 0
        for salinity in salinity_series:
            if self.salinity_value_ok(salinity):
                n_adequate += 1

        return float(n_adequate)/len(salinity_series)

    def get_temperature_min(self):
        """Returns minimum acceptable temperature for species."""

        return self.conf[self.id]["temperature_min"]

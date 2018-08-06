# Classes:
class Species(object):
    """Description of a given biological species."""

    # Constructor:
    def __init__(self, identifier):
        self.id = identifier

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

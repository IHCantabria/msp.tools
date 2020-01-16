import logging
import math

# Classes:
class waveresource(object):
    """Description of wave resource"""

    # Constructor:
    def __init__(self, conf):
        self.logger = logging.getLogger("msp.aquaculture.waveresource")
        self.conf = conf

    # Public methods:

    def is_value_between_values(self, value, min, max):
        return min < float(value) < max

    def is_value_higher(self, value, min):
        return min < value

    def calculate_suitability(self, data_serie):
        """Return fraction of hs values
        in corresponding series that are adequate for us.
        """
        hs_ok = tp_ok = cge_ok = 0

        dates = sorted(data_serie.keys())
        for day in dates:
            hs = data_serie[day]["hs"]
            tp = data_serie[day]["tp"]
            tm = data_serie[day]["tm"]
            cge = self.calculate_cge(hs, tm)
            if self.is_value_between_values(hs, self.hs_min, self.hs_max):
                hs_ok += 1
            if self.is_value_between_values(tp, self.tp_min, self.tp_max):
                tp_ok += 1
            if self.is_value_higher(cge, self.cge_min):
                cge_ok += 1

        total = len(data_serie)
        # suitability = self.mean_value(
        #    hs_pu/total, tp_pu/total, cge_pu/total, cge_pu/total)
        suitability = self.mean_value(hs_ok, tp_ok, cge_ok, cge_ok) / total
        self.logger.debug("suitability: " + str(suitability))
        return suitability

    def mean_value(self, *args):
        total = 0
        for arg in args:
            total += arg
        return total / len(args)

    def calculate_cge(self, hs, tm):
        f = 1.025
        g = 9.81
        return 1 / (64 * math.pi) * f * math.pow(g, 2) * math.pow(hs, 2) * tm

    # Public properties:
    @property
    def hs_min(self):
        """Returns minimum acceptable hs for wave resource."""

        return self.conf["hs_min"]

    @property
    def hs_max(self):
        """Returns maximum acceptable hs for wave resource."""

        return self.conf["hs_max"]

    @property
    def tp_min(self):
        """Returns minimum acceptable hs for wave resource."""

        return self.conf["tp_min"]

    @property
    def tp_max(self):
        """Returns maximum acceptable hs for wave resource."""

        return self.conf["tp_max"]

    @property
    def cge_min(self):
        return self.conf["cge_min"]

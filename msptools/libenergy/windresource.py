import logging
import math
# Classes:
class windresource(object):
    """Description of wave resource"""

    # Constructor:
    def __init__(self, conf):
        self.logger = logging.getLogger("msp.aquaculture.windresource")
        self.conf = conf
        
    # Public methods:
    
    
    def is_value_lower(self, value, max):
        return value < max
    
    def calculate_suitability(self, data_serie):
        """Return fraction of hs values
        in corresponding series that are adequate for us.
        """
        hs_ok = potential_ok = 0
        dates = sorted(data_serie.keys())
        for day in dates:
            self.hs = data_serie[day]['hs']
            
            speed = self.get_speed(data_serie[day]['u10'], data_serie[day]['v10'])
            area_rotor = 1
            potential = self.get_potential(speed, area_rotor)
            if potential >= 400:
                potential_ok += 1
            if self.is_value_lower(data_serie[day]['hs'], self.hs_max):
                hs_ok += 1
            
        total = len(data_serie)

        hs_pu = hs_ok / total
        if hs_pu > 0.7:
            hs_pu = 1
        potential_pu = potential_ok / total
        if potential_pu > 0.7:
            potential_pu = 1

        return min (hs_pu, potential_pu)



    def get_speed(self, u, v):
        return math.sqrt(math.pow(u, 2) + math.pow(v,2))
    # Public properties:
    def get_potential(self, speed, area_rotor):
        return 1.225 / 2 * math.pow(speed, 3) * area_rotor

    @property
    def hs_max(self):
        """Returns maximum acceptable hs for wave resource."""
        return self.conf["hs_max"]

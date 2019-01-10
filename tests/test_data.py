import unittest

from msptools.libaquaculture import core
from msptools.libaquaculture import copernicus


class Test_Data(unittest.TestCase):

    def test_load_historical_serie(self):
        ocean_data = None
        params = {
            'point': {'lon': -13.016, 'lat': 28.486},
            'specie': {
                'name': 'European seabass',
                'salinity_min': 30,
                'salinity_max': 40,
                'temperature_min': 18,
                'temperature_max': 26
            },
            'dates': {
                'ini': '2015-01-01',
                'end': '2015-03-01'
            }
        }
        specie, point, dates = core.parse_input_web(params)
        ocean_data = copernicus.get_temperature_and_salinity_from_global_reanalysis_physical(
            point, dates)
        self.assertIsNotNone(ocean_data)
        self.assertIs(len(ocean_data), 60)

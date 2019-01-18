import unittest
import datetime

from msptools.libaquaculture import core
from msptools.libaquaculture import copernicus
from msptools.libaquaculture.thredds import Thredds
from msptools import aquaculture
from msptools.config import CONFIG


class Test_Data(unittest.TestCase):
    def setUp(self):
        self.params = {
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

    def test_load_historical_serie(self):
        ocean_data = None
        specie, point, dates = core.parse_input_web(self.params)
        ocean_data = copernicus.get_temperature_and_salinity_from_global_reanalysis_physical(
            point, dates)
        self.assertIsNotNone(ocean_data)
        self.assertIs(len(ocean_data), 60)

    def test_scale_factor(self):
        expected_value = 18.6481216738  # temp on 2/1/2015(day/month/year)
        thredds = Thredds(CONFIG["copernicus"]
                          ["global_reanalysis_physical"]["catalog"])
        raw_value = -3211

        real_value = thredds.get_real_value(raw_value, 7.324442E-4, 21)
        self.assertAlmostEqual(real_value, expected_value)

    def test_check_output_format(self):
        timestamp = 1420200000.0  # 2/1/2015
        expected_value = 18.6481216738  # temp on 2/1/2015(day/month/year)
        data = aquaculture.load_historical_serie(self.params)
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 60)
        self.assertIsInstance(data[timestamp]['date'], datetime.date)
        self.assertEqual(len(data[timestamp]['measures']), 2)
        self.assertEqual(data[timestamp]['measures']
                         [0]['value'], expected_value)

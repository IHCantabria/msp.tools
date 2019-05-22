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
        expected_salinity = 36.597797192  # salinity on 2/1/2015
        thredds = Thredds(CONFIG["copernicus"]
                          ["global_reanalysis_physical"]["catalog"])
        raw_value = -3211
        raw_salinity = 23985

        real_value = thredds.get_real_value(raw_value, 7.324442E-4, 21)
        real_salinity = thredds.get_real_value(
            raw_salinity, 0.0015259255, -0.0015259255)
        self.assertAlmostEqual(real_value, expected_value)
        self.assertAlmostEqual(real_salinity, expected_salinity)

    def test_check_output_format(self):
        data = aquaculture.load_historical_serie(self.params)
        self.assertIsNotNone(data)
        for measured_variable in data['measures']:
            self.assertIsNotNone(measured_variable['var_alias'])
            self.assertIsNotNone(measured_variable['var_name'])
            self.assertIsNotNone(measured_variable['units'])
            self.assertIsNotNone(measured_variable['values'])
            self.assertIsInstance(measured_variable['values'], list)

    def test_values_on_day(self):
        timestamp = 1420200000.0  # 2/1/2015 12:00:00
        expected_temperature = 18.6481216738  # temp on 2/1/2015
        expected_salinity = 36.597797192  # salinity on 2/1/2015
        data = aquaculture.load_historical_serie(self.params)
        self.assertEqual(len(data['measures'][0]['values']), 60)
        self.assertEqual(len(data['measures'][1]['values']), 60)
        # Check temperature
        for value in data['measures'][0]['values']:
            if (value[0] == timestamp):
                self.assertEqual(value[1], expected_temperature)
        # Check salinity
        for value in data['measures'][1]['values']:
            if (value[0] == timestamp):
                self.assertEqual(value[1], expected_salinity)

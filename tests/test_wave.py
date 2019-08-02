import unittest
from datetime import datetime


from msptools import waveenergy
from msptools import utils
from msptools.config import CONFIG


class Test_Wave(unittest.TestCase):
    def setUp(self):
        self.params = {
            'config': {
                'hs_min': 1,
                'hs_max': 5,
                'tp_min': 5,
                'tp_max': 14,
                'cge_min': 15,
            },
            'point': {'lon': -13.016, 'lat': 28.486},
            'dates': {
                'start': '2015-01-01',
                'end': '2015-03-01',
            }
        }

    def test_get_suitability(self):
        result = waveenergy.run_suitability(self.params)
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result, 0.7375)

    def test_throws_landException(self):
        self.params["point"]["lon"] = -2.445556
        self.params["point"]["lat"] = 42.47
        with self.assertRaises(utils.LandException):
            waveenergy.run_suitability(self.params)


if __name__ == '__main__':
    unittest.main()

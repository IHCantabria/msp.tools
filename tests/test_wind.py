import unittest
from datetime import datetime


from msptools import windenergy
from msptools import utils
from msptools.config import CONFIG


class Test_Wind(unittest.TestCase):
    def setUp(self):
        self.params = {
            "config": {"hs_max": 5, "pow": 400},
            "point": {"lon": -13.016, "lat": 28.486},
            "dates": {"start": "2015-01-01", "end": "2015-03-01",},
        }

    def test_get_result(self):
        result = windenergy.run_suitability(self.params)
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result, 0.45)

    def test_get_result(self):
        params = {
            "config": {"hs_max": 5, "pow": 400},
            "point": {"lon": -7.229, "lat": 48.75895},
            "dates": {"start": "2010-02-01", "end": "2010-02-05",},
        }
        result = windenergy.run_suitability(params)
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result, 1)

    def test_get_result_alt(self):
        params = {
            "config": {"hs_max": 5, "pow": 400},
            "point": {"lon": -2.37305, "lat": 47.06264},
            "dates": {"start": "2010-02-01", "end": "2010-02-05",},
        }
        result = windenergy.run_suitability(params)
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result, 0)

    def test_throws_landException(self):
        self.params["point"]["lon"] = -2.445556
        self.params["point"]["lat"] = 42.47
        with self.assertRaises(utils.LandException):
            windenergy.run_suitability(self.params)


if __name__ == "__main__":
    unittest.main()

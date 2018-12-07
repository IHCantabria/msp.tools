# Standard libs:
import unittest
import argparse
from datetime import datetime

# Our libs:
import msptools


# Classes:
class TestFunctions(unittest.TestCase):
    """Test the functions in core.py."""

    def setUp(self):
        self.params = {
            "point": { 
                "lon": -13.016, 
                "lat": 28.486
            },
            "specie": {
                "name": 'European seabass',
                "salinity_min": 30,
                "salinity_max": 40,
                "temperature_min": 18,
                "temperature_max": 26
            },
            "dates": {
                "ini": '2015-01-01',
                "end": '2015-03-01'
            }
        }

    def tearDown(self):
        pass

    def test_complete_run(self):
        self.assertAlmostEqual( msptools.aquaculture.run_biological(self.params),0.26, delta=0.01)

    def test_throws_landException(self):
        self.params["point"]["lon"] = -2.445556
        self.params["point"]["lat"] = 42.47
        #with self.assertRaises(Exception): aquaculture.run_biological(self.params)
        with self.assertRaises(msptools.aquaculture.core.LandException): msptools.aquaculture.run_biological(self.params)
   
if __name__ == '__main__':
    unittest.main()
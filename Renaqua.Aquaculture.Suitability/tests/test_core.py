# Standard libs:
import unittest
import argparse
from datetime import datetime

# Our libs:
from libaquaculture import core


# Classes:
class TestFunctions(unittest.TestCase):
    """Test the functions in core.py."""

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def test_parse_args_empty(self):
        ret = core.parse_args([])
        self.assertIsInstance(ret, argparse.Namespace)

    def test_parse_args_longitudes(self):
        cases = [
            ([], None),
            (["--longitude", "0"], 0.0),
            (["--longitude", "-90"], -90.0),
        ]
        for args, value in cases:
            ret = core.parse_args(args)
            self.assertEqual(ret.longitude, value)

    def test_wednesdays_between(self):
        wl = [
            datetime(2018, 1, 3),  datetime(2018, 1, 10), datetime(2018, 1, 17), datetime(2018, 1, 24),
            datetime(2018, 1, 31), datetime(2018, 2, 7),  datetime(2018, 2, 14), datetime(2018, 2, 21),
            datetime(2018, 2, 28), datetime(2018, 3, 7),  datetime(2018, 3, 14), datetime(2018, 3, 21),
            datetime(2018, 3, 28), datetime(2018, 4, 4),  datetime(2018, 4, 11), datetime(2018, 4, 18),
            datetime(2018, 4, 25), datetime(2018, 5, 2),  datetime(2018, 5, 9),  datetime(2018, 5, 16),
            datetime(2018, 5, 23), datetime(2018, 5, 30), datetime(2018, 6, 6),  datetime(2018, 6, 13),
            datetime(2018, 6, 20), datetime(2018, 6, 27)
        ]
        cases = [
            (datetime(2018, 1, 1),  datetime(2018, 1, 1),  []),  # no wednesday
            (datetime(2018, 1, 1),  datetime(2018, 1, 31), wl[:5]),  # just some days
            (datetime(2018, 1, 15), datetime(2018, 2, 28), wl[2:9]),  # ends in wednesday
            (datetime(2018, 1, 3), datetime(2018, 2, 28), wl[:9]),  # starts and ends in wednesday
            (datetime(2018, 2, 28), datetime(2018, 2, 28), wl[8:9]),  # just one day, a wednesday
            (datetime(2018, 1, 1),  datetime(2018, 6, 30), wl),  # the whole period
        ]

        for start, end, wednesdays in cases:
            w = core.wednesdays_between(start, end)
            self.assertEqual(w, wednesdays)


if __name__ == '__main__':
    unittest.main()
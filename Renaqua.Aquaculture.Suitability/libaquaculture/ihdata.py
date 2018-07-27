# Standard libs:
import netCDF4 as nc4


# Classes:
class IHData(object):
    """Class to manage access to 'IHData' netCDFs."""

    def __init__(self):
        pass  # Empty constructor
    
    def get_variable(self, var_name, conf):
        """Returns contents of variable 'var_name'."""

        fn = "http://test.opendap.org/dap/data/nc/coads_climatology.nc"
        fn = "ARMOR3D_REPv3-1_20130102_20140420.nc"

        fn = conf["url_file"]

        with nc4.Dataset(fn) as nc:
            print(nc.variables.keys())
            var = nc.variables["salinity"][0:5, 0:5, 0:5]

            print(var)

            return None

            #var = nc.variables["salinity"][0, 0, 0]
            #var = var[0, :2, :2]
            #print(var)

        return None
        print("abc")
        print("aaa")


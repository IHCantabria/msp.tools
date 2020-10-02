class LandException(Exception):
    pass
def check_land_exception(data, var_names):
    for var_name in var_names:
        for point in data:
            if point[var_name] is None:
                raise LandException()
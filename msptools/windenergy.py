from datetime import datetime
import logging 
import sys
import msptools.config
from msptools.config import CONFIG
from msptools.libenergy import core
from msptools.libenergy import ecmwf
from msptools.libenergy import windresource
logger = logging.getLogger("msp.windenergy")
logger.setLevel(logging.getLevelName(CONFIG["log"]["level"]))

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(CONFIG["log"]["filepath"])
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def run_from_cli():
    logger.debug("Starting from CLI")
    ranges, point, dates = core.parse_args(sys.argv[1:])
    result = get_suitability(point, dates, ranges)
    logger.info(result)


def run_suitability(params):
    logger.debug(params['point'])
    points, dates, config = core.parse_input_web(params)
    return get_suitability(points, dates, config)
    

def get_suitability(point, dates, ranges):
    values_from_global_atmospheric_reanalysis = ecmwf.get_data_from_era_interim(
        point, dates, CONFIG["ECMWF"]["wind"]["variables"])
    
    resource = windresource.windresource(ranges)
    
    suitability = resource.calculate_suitability(
        values_from_global_atmospheric_reanalysis)
    
    return suitability

# Main body:
if __name__ == '__main__':
    run_from_cli()

# Standard libs:
from datetime import datetime
import logging
import sys
# Our libs:
from msptools.libaquaculture import core
from msptools.libaquaculture import biology
from msptools.libaquaculture import copernicus
from msptools.config import CONFIG
# Globals:

logger = logging.getLogger("msp.aquaculture")
logger.setLevel(logging.getLevelName(CONFIG["log"]["level"]))

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(CONFIG["log"]["filepath"])
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def run_biological(params):
    """Function to run the library from Screening tool"""
    logger.debug("Starting from web")
    specie, point, dates = core.parse_input_web(params)
    return get_biological_probability(specie, point, dates)


def load_historical_serie(params):
    """Load data serie for salinity and temperature in a point between dates"""
    logger.debug("Load ocean data from web")
    specie, point, dates = core.parse_input_web(params)
    data_serie = copernicus.get_temperature_and_salinity_from_global_reanalysis_physical(
        point, dates)
    parsed_data_serie = standarize_data(data_serie)
    return parsed_data_serie


def standarize_data(data_serie):
    """ Normalize data from thredds """
    parsed_data_serie = {}
    i = 0
    for (key, values) in data_serie.items():
        # set standarized data object
        data = {}
        data['date'] = key
        data['measures'] = _get_data_measures(values)

        parsed_data_serie[key.timestamp()] = data
        i += 1
    return parsed_data_serie


def _get_data_measures(thredds_values):
    measures = []
    for variable in CONFIG["copernicus"]["variables"]:
        measure = {
            "name": variable["name"],
            "alias": variable["alias"],
            "units": variable["units"],
            "value": thredds_values[variable["alias"]]
        }
        measures.append(measure)
    return measures


def get_biological_probability(specie_config, point, dates):
    """It calculates the probability of growing specie, for a specific point and set period.To this end: 1) Download data for the specific point and set period from Copernicus provider, 2) Set up the suitable temperature and salinity range growth of the study specie, 3) Select suitable days of data period downloaded in order to calculate the probability of growing
    """

    values_from_global_reanalysis = copernicus.get_temperature_and_salinity_from_global_reanalysis_physical(
        point, dates)
    specie = biology.Species(specie_config)
    probability = specie.biological_suitability_index(
        values_from_global_reanalysis)

    return probability

# Functions:


def run_from_cli():
    logger.debug("Starting from CLI")
    specie, point, dates = core.parse_args(sys.argv[1:])
    logger.info(get_biological_probability(specie, point, dates))


# Main body:
if __name__ == '__main__':
    run_from_cli()

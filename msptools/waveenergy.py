from datetime import datetime
import logging
import sys
from msptools.config import CONFIG
from msptools.libenergy import core
from msptools.libenergy import ecmwf
from msptools.libenergy import waveresource

logger = logging.getLogger("msp.waveenergyresource")
logger.setLevel(logging.getLevelName(CONFIG["log"]["level"]))

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler(CONFIG["log"]["filepath"])
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def run_from_cli():
    logger.debug("Starting from CLI")
    waveresource, point, dates = core.parse_args(sys.argv[1:])
    result = get_waveresource_suitability(waveresource, point, dates)
    logger.info(result)


def run_suitability(params):
    point, dates, config = core.parse_input_web_wave(params)
    return get_waveresource_suitability(config, point, dates)


def get_waveresource_suitability(wave_config, point, dates):

    values_from_global_atmospheric_reanalysis = ecmwf.get_data_from_era_interim(
        point, dates, CONFIG["ECMWF"]["wave"]["variables"]
    )
    resource = waveresource.waveresource(wave_config)
    suitability = resource.calculate_suitability(
        values_from_global_atmospheric_reanalysis
    )
    return suitability


# Main body:
if __name__ == "__main__":
    run_from_cli()

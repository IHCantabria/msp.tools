def run_biological(params):
    from . import aquaculture

    return aquaculture.run_biological(params)


def load_historical_serie(params):
    from . import aquaculture

    return aquaculture.load_historical_serie(params)


def run_waveenergy(params):
    from . import waveenergy

    return waveenergy.run_suitability(params)


def run_windenergy(params):
    from . import windenergy

    return windenergy.run_suitability(params)


import xarray
import numpy as np
import matplotlib.pyplot as plt
import  netCDF4 as nc
import msptools
from msptools.utils import LandException


NetCDFProvider = xarray.open_dataset("C:/Users/abads/Downloads/GLOBAL_REANALYSIS_PHY_001_030.nc")
StartEndDate = NetCDFProvider.sel(time=slice("1993-01-01", "1993-02-01"))
extentStudy = StartEndDate.sel(longitude=slice(-0.179,1.34), latitude=slice(38.74,39.003))

listaLongitudes = extentStudy["longitude"]
numberLongitudes = len(listaLongitudes)
listaLatitudes = extentStudy["latitude"]
numberLatitudes = len(listaLatitudes)

dims = ("latitude", "longitude")
sizes = (len(extentStudy["latitude"].values), len(extentStudy["longitude"].values))
#crea una variable llamada suitability con todos los valores en 0
ds = xarray.Dataset(
        data_vars=dict(suitability=(dims, np.zeros(sizes))),
        coords={d: np.arange(s) for d, s in zip(dims, sizes)},
    ) 

ds["latitude"]=extentStudy["latitude"]
ds["longitude"]=extentStudy["longitude"]
contadorLon = 0
for longitude in listaLongitudes:
    contadorLat = 0
    for latitude in listaLatitudes:
        point = {"lon": np.asscalar(longitude), "lat": np.asscalar(latitude)}
        params = {"point": point,"specie": { "name": 'European seabass', "salinity_min": 20, "salinity_max": 40, "temperature_min": 15, "temperature_max": 16 }, "dates": { "ini": '2015-01-01', "end": '2015-03-01' }}
        try:
            value = msptools.run_biological(params)
            #asignar un valor, a un índice concreto
            ds["suitability"][contadorLat][contadorLon] = value
            print ("Analizado probabilidad biologica en punto " + f"{point}={value}")

        except LandException:
            print ("Se ha producido una excepción")
            pass
            print ("Terminado")
        contadorLat = contadorLat + 1
    contadorLon = contadorLon + 1
ds.to_netcdf("Test2.nc")




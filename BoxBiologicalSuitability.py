import xarray
import numpy as np
import  netCDF4 as nc
import msptools
from netCDF4 import Dataset
from msptools.utils import LandException
from msptools.config import threddsIH


NetCDFProviderInput = input('Enter your netcdf provider: ')
NetCDFProvider = xarray.open_dataset(NetCDFProviderInput)
StartDate, EndtDate = input("Enter Start and End analysis (dates separated by space). Format: Year-Month-Day ").split()
StartEndDate = NetCDFProvider.sel(time=slice(StartDate, EndtDate))
xmin,xmax,ymin,ymax = [float(x) for x in input("Enter longitudes and latitudes coordinates following this orden: xmin,xmax,ymin,ymax ").split()]
extentStudy = StartEndDate.sel(longitude=slice(xmin,xmax), latitude=slice(ymin,ymax)) 
specie = dict(name= 'European seabass', salinity_min= 20, salinity_max= 40, temperature_min= 15, temperature_max= 16)
dates = dict( ini= StartDate, end= EndtDate)


# NetCDFProvider = xarray.open_dataset(""https://ihthredds.ihcantabria.com/thredds/dodsC/COPERNICUS/CMEMS/GLOBAL_REANALYSIS_PHY_001_030/GLOBAL_REANALYSIS_PHY_001_030.nc"")
# StartEndDate = NetCDFProvider.sel(time=slice("1993-01-01", "1993-02-01"))
# extentStudy = StartEndDate.sel(longitude=slice(-0.179,1.34), latitude=slice(38.74,39.003))
# DiccionarioOld{"name": 'European seabass', "salinity_min": 20, "salinity_max": 40, "temperature_min": 15, "temperature_max": 16 }, "dates": { "ini": '2015-01-01', "end": '2015-03-01' }

listaLongitudes = extentStudy["longitude"]
numberLongitudes = len(listaLongitudes)
listaLatitudes = extentStudy["latitude"]
numberLatitudes = len(listaLatitudes)

#Accede al netcdf y selecciona las dimensiones relativas a las coordenadas gracias al atributo axis
dimens = NetCDFProvider.dims
varLongitude = None
varLatitude = None
for dim in dimens:
    if extentStudy.variables[dim].attrs["axis"] == "X":
        varLongitude = extentStudy.variables[dim].attrs["standard_name"]
    if extentStudy.variables[dim].attrs["axis"] == "Y":
        varLatitude = extentStudy.variables[dim].attrs["standard_name"]
print (varLongitude, varLatitude)

dims = (varLatitude, varLongitude)
sizes = (len(extentStudy[varLatitude].values), len(extentStudy[varLongitude].values))

#Crea una variable llamada suitability con todos los valores en 0
ds = xarray.Dataset(
        data_vars=dict(suitability=(dims, np.zeros(sizes))),
        coords={d: np.arange(s) for d, s in zip(dims, sizes)},
    ) 

ds[varLatitude]=extentStudy[varLatitude]
ds[varLongitude]=extentStudy[varLongitude]
contadorLon = 0
for longitude in listaLongitudes:
    contadorLat = 0
    for latitude in listaLatitudes:
        point = {"lon": np.asscalar(longitude), "lat": np.asscalar(latitude)}
        params = {"point": point,"specie": specie,"dates":{ "ini": '2015-01-01', "end": '2015-03-01' }}
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
ds.to_netcdf("SuitabilityOutput.nc")





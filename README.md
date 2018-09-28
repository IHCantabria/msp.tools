# Renaqua.Aquaculture.Suitability

> Screening tool for aquaculture suitability

## Getting Started

Toolbox developed in the framework of Renaqua project. The toolbox will be integrated in a Screening tool for calculate aquaculture suitability. It is organise in four tools : biological suitability for each specie & structural suitability for cage &  operational suitability for carry out operation and maintenance activities. & total suitability 

### Prerequisites

In case netCDF files are stored in thredds which need home authenticator account, you need add RC files (\\docs\conf_DAP) in your pc C:\Users\XXXX. Remember add a dot "." to .dodsrc file. This change must be carry out using terminal (Windows)

source: http://docs.opendap.org/index.php/DAP_Clients_-_Authentication#Matlab.2C_Ferret.2C_Other_applications_that_use_NetCDF_C


Give examples


### Installing

Python 3.7

Install requirements.txt

```
python RenaquaAquacultureSuitability.py --longitude -6.5 --latitude 43.8 --id "s0001"
 --start 2008-01-01 --end 2013-01-01
```

```
python RenaquaAquacultureSuitability.py --longitude -6.5 --latitude 43.8 --name “Sardina” --temperature-min 18 --temperature-max 27--salinity-min 30 --salinity-max 40
--start 2008-01-01 --end 2013-01-01
```

## Versioning



## License



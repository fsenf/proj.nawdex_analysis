# Observed TOA Radiation Flux Data and CRE (on TROPOS altair)
## TOA Radiation fluxes
TOA Radiation fluxes have been provided by Nicola Clerbaux (Belgium) as hdf5 files. The data are saved as `H5T_STD_I16BE` which means signed 16-bit integer (big endian). On TROPOS altair, TOA radiation data are saved under
```
/vols/talos/home/fabian/data/gerb-like
```
A NaN values seems to be set to -32767 (and need to be masked) and all other values have to be multiplied by 0.25 get to radiation fluxes with unit Wm**(-2).

### Input of Data
Functions to read and cutout TOA radiation flux data are available under pyhton package `nawdex_analysis.io.input_obs`.

The calls 
```
>>>import nawdex_analysis.io.input_obs as ioobs
>>>lwf, swf_net = ioobs.read_radiation_fluxes( t )
``` 
read observed long-wave fluxes (`lwf`) and net short-wave flux (`swf_net`) scaled to SEVIRI grid.

### Cutout of data
We only use a certain SEVIRI cutout for data analysis. This variable is saved under `nawdex_analysis.config`. An option to input cutted data on-the-fly is incorporated into `ioobs.read_radiation_fluxes( t )`.

### Output daily stacks to netcdf
To ease later analysis, daily stacks of TOA radiation flux data have been saved into netcdf format using 

```
>>>import nawdex_analysis.io.output_obs as oobs
>>>oobs.save_radflux_tstack( date )
```


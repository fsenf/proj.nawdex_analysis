# Observed TOA Radiation Flux Data and CRE (on TROPOS altair)
## TOA allsky Radiation Fluxes
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

### Run Script for Regridding and NetCDF Output
A python script on TROPOS is used for regridding and output of observed radiation fluxes:
```
cd /pf/b/b380352/proj/2017-07_nawdex_analysis/inout/
./save_toa_radflux4nawdex.py 20160930
```

### Final Allsky Radiation Data
These daily data stacks are saved under:
```
ls -1 /vols/talos/home/fabian/data/icon/nawdex/gerb-like/
toa_radflux-nawdex-20160915.nc
toa_radflux-nawdex-20160916.nc
toa_radflux-nawdex-20160917.nc
toa_radflux-nawdex-20160918.nc
toa_radflux-nawdex-20160919.nc
toa_radflux-nawdex-20160920.nc
toa_radflux-nawdex-20160921.nc
toa_radflux-nawdex-20160922.nc
toa_radflux-nawdex-20160923.nc
toa_radflux-nawdex-20160924.nc
toa_radflux-nawdex-20160925.nc
toa_radflux-nawdex-20160926.nc
toa_radflux-nawdex-20160927.nc
toa_radflux-nawdex-20160928.nc
toa_radflux-nawdex-20160929.nc
toa_radflux-nawdex-20160930.nc
toa_radflux-nawdex-20161001.nc
toa_radflux-nawdex-20161002.nc
toa_radflux-nawdex-20161003.nc
toa_radflux-nawdex-20161004.nc
toa_radflux-nawdex-20161005.nc
toa_radflux-nawdex-20161006.nc
toa_radflux-nawdex-20161007.nc
toa_radflux-nawdex-20161008.nc
toa_radflux-nawdex-20161009.nc
toa_radflux-nawdex-20161010.nc
toa_radflux-nawdex-20161011.nc
toa_radflux-nawdex-20161012.nc
toa_radflux-nawdex-20161013.nc
toa_radflux-nawdex-20161014.nc
```

An example is
```
ncdump -h /vols/talos/home/fabian/data/icon/nawdex/gerb-like/toa_radflux-nawdex-20160930.nc
netcdf toa_radflux-nawdex-20160930 {
dimensions:
	rows = 1004 ;
	cols = 2776 ;
	time = 24 ;
variables:
	short swf_up(time, rows, cols) ;
		swf_up:_FillValue = 0s ;
		swf_up:units = "W m**(-2)" ;
		swf_up:long_name = "TOA short-wave upwelling radiation flux" ;
		swf_up:coordinates = "lat lon" ;
		swf_up:scale_factor = 0.25 ;
	short swf_net(time, rows, cols) ;
		swf_net:_FillValue = 0s ;
		swf_net:units = "W m**(-2)" ;
		swf_net:long_name = "TOA short-wave net radiation flux" ;
		swf_net:coordinates = "lat lon" ;
		swf_net:scale_factor = 0.25 ;
	short lwf(time, rows, cols) ;
		lwf:_FillValue = 0s ;
		lwf:units = "W m**(-2)" ;
		lwf:long_name = "TOA long-wave radiation flux" ;
		lwf:coordinates = "lat lon" ;
		lwf:scale_factor = 0.25 ;
	float lat(rows, cols) ;
		lat:_FillValue = NaNf ;
		lat:units = "degrees_north" ;
		lat:long_name = "latitude" ;
	float lon(rows, cols) ;
		lon:_FillValue = NaNf ;
		lon:units = "degrees_east" ;
		lon:long_name = "longitude" ;
	double time(time) ;
		time:_FillValue = NaN ;
		time:units = "day as %Y%m%d.%f" ;
		time:long_name = "Time" ;
		time:calendar = "proleptic_gregorian" ;

// global attributes:
		:description = "GERB-like TOA radiation flux derived from Meteosat SEVIRI and obtained from Nicolas Clerbaux" ;
		:title = "TOA Radiation Fluxes" ;
		:institution = "Leibniz Institute for Tropospheric Research" ;
		:author = "Fabian Senf (senf@tropos.de)" ;
}

```


## TOA clearsky Radiation Fluxes
Clearsky is challenging for the observation because the investigation area is a very cloudy place and the time record (~one month) is rather short. Hence, methods that rely on temporal stacking and finding a close clearsky pixel are rather inaccurate!

We are going top use simulated clearsky instead (chosen the 10km grid spacing runs) with the drawback that bias corrections have to be applied.

### Bias Correction for Shortwave (on Mistral)
Two important points
  * It seems to be that the simulated clearsky ocean is too bright, i.e. outgoing SWF is too large for the simulations. Therefore, we apply a scale factor to reduce the bias.
  * The incoming SWF sensitively depends on the accurate time. The model time is exactly at 0 UTC, but the observational time is delayed by ~12 minutes due to the scanning strategy (from South to North). Therefore, the incoming flux is taken from the observational data (luckily included) and used as net incoming flux.


A general function exists that inputs simulated clearsky fluxes:
```
import nawdex_analysis.io.input_sim as isim
isim.read_simulated_clearsky_flux??
```


Python scripts are located on mistral and can be run via
```
cd /pf/b/b380352/proj/2017-07_nawdex_analysis/inout
./save_retrieved_clearsky_SWF.py $EXPNAME
```

### Bias Correction for Longwave
Bias correction for the longwave is done on the fly (at the moment - for simplicity). An offset of-2 W/m**2 is substracted from the simulation bases estimate. That is, simulaiton is slightly too warm. 

## Calculation of Average CRE
A general script exists to calculate the average CRE depending on cloud type (hence cloud type has be input as well). It can be run at TROPOS via
```
cd /vols/talos/home/fabian/proj/2017-07_icon-nawdex/inout
./save_ave_cre.py /vols/talos/home/fabian/data/icon/nawdex/gerb-like/toa_radflux-nawdex-20160922.nc -scaled
```

The script generates netcdf files which are stored under
```
ls -1 /vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled*nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20160915.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20160916.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20160917.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20160918.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20160919.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20160920.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20160921.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20160922.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20160923.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20160924.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20160925.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20160926.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20160927.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20160928.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20160929.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20160930.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20161001.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20161002.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20161003.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20161004.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20161005.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20161006.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20161007.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20161008.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20161009.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20161010.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20161011.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20161012.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20161013.nc
/vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20161014.nc
``` 

Example content:
```
ncdump -h /vols/talos/home/fabian/data/icon/nawdex/statistics/ave_cre-scaled_meteosat-nawdex-20160922.nc
netcdf ave_cre-scaled_meteosat-nawdex-20160922 {
dimensions:
	time = 24 ;
	ct = 11 ;
	string18 = 18 ;
variables:
	int64 time(time) ;
		time:units = "hours since 2016-09-22 00:00:00" ;
		time:calendar = "proleptic_gregorian" ;
	double lcre_ave(time, ct) ;
		lcre_ave:_FillValue = NaN ;
		lcre_ave:units = "W m^{-2}" ;
		lcre_ave:longname = "area-average longwave CRE " ;
	double afrac(time, ct) ;
		afrac:_FillValue = NaN ;
		afrac:units = "%" ;
		afrac:longname = "relative area fractions per cloud type" ;
	double scre_ave(time, ct) ;
		scre_ave:_FillValue = NaN ;
		scre_ave:units = "W m^{-2}" ;
		scre_ave:longname = "area-average shortwave CRE " ;
	char ct(ct, string18) ;
}
```



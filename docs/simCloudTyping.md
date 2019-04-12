# Simulated Cloud Typing

## Synthetic Satellite Data Calculation (Mistral)
The ICON simulation data have been transfered to DKRZ Mistral by Aiko Voigt. The "Synsat" forward operator has been applied to the simulation data using the script 
```
/pf/b/b380352/proj/2015-12_synsat/synsats4icon_nawdex/synsat_icon-nawdex.py
```
The script takes the `fg` filename as argument. The calculation are restricted to a satellite zenith angle of <75 degrees. The synsat data are saved as brightness temperatures for several infrared SEVIRI bands into hdf5 files. They are vectors using the mask = zen < 75 and are discretized as 0.01 Kelvin. Hence, the georeference and the masking condition is needed to recover the synsat data on the native model grid (which is also a vector in our case).

One example is e.g.
```
cd ~/data/synsat/nawdex/nawdexnwp-20km-mis-0001/

h5ls -r synsat_nawdexnwp-20km-mis-0001_2016092200_fg_DOM01_ML_0001_0_88576.h5
```
giving the output
```
/                        Group
/mcfarq_rescale_noccthresh Group
/mcfarq_rescale_noccthresh/IR_087 Dataset {1, 88576}
/mcfarq_rescale_noccthresh/IR_108 Dataset {1, 88576}
/mcfarq_rescale_noccthresh/IR_120 Dataset {1, 88576}
/mcfarq_rescale_noccthresh/IR_134 Dataset {1, 88576}
/mcfarq_rescale_noccthresh/WV_062 Dataset {1, 88576}
/mcfarq_rescale_noccthresh/WV_073 Dataset {1, 88576}
```
Thus, six different channels are included.

### SynSat Data Regridding
Regridding of synsat data is done with the tools described [here](simCloudRadiativeEffect.md). 

Similar to the radiation fluxes, synthetic sat data are regridded onto MSG grid using a python script on Mistral:
```
cd ~/proj/2017-07_nawdex_analysis/inout
./save_reproj_synsat.py /pf/b/b380352/data/synsat/nawdex/nawdexnwp-80km-mis-0001
```

## Applying Cloud Typing to the Synthetic Sat Data (TROPOS)
### Synsat@TROPOS
The synsat data have been transfered to TROPOS and are stored under
```
ls -1 /vols/talos/home/fabian/data/icon/nawdex/synsat/synsat*nc
synsat-nawdexnwp-10km-mis-0001.nc
synsat-nawdexnwp-10km-mis-0002.nc
synsat-nawdexnwp-10km-mis-0003.nc
synsat-nawdexnwp-10km-mis-0004.nc
synsat-nawdexnwp-10km-mis-0005.nc
synsat-nawdexnwp-10km-mis-0006.nc
synsat-nawdexnwp-10km-mis-0007.nc
synsat-nawdexnwp-10km-mis-0008.nc
synsat-nawdexnwp-10km-mis-0009.nc
synsat-nawdexnwp-10km-mis-0010.nc
synsat-nawdexnwp-10km-mis-0011.nc
synsat-nawdexnwp-10km-mis-0012.nc
synsat-nawdexnwp-20km-mis-0001.nc
synsat-nawdexnwp-20km-mis-0002.nc
synsat-nawdexnwp-20km-mis-0003.nc
synsat-nawdexnwp-20km-mis-0004.nc
synsat-nawdexnwp-20km-mis-0005.nc
synsat-nawdexnwp-20km-mis-0006.nc
synsat-nawdexnwp-20km-mis-0007.nc
synsat-nawdexnwp-20km-mis-0008.nc
synsat-nawdexnwp-20km-mis-0009.nc
synsat-nawdexnwp-20km-mis-0010.nc
synsat-nawdexnwp-2km-mis-0001.nc
synsat-nawdexnwp-2km-mis-0002.nc
synsat-nawdexnwp-2km-mis-0003.nc
synsat-nawdexnwp-2km-mis-0004.nc
synsat-nawdexnwp-2km-mis-0005.nc
synsat-nawdexnwp-2km-mis-0006.nc
synsat-nawdexnwp-2km-mis-0007.nc
synsat-nawdexnwp-2km-mis-0008.nc
synsat-nawdexnwp-2km-mis-0009.nc
synsat-nawdexnwp-2km-mis-0010.nc
synsat-nawdexnwp-2km-mis-0011.nc
synsat-nawdexnwp-2km-mis-0012.nc
synsat-nawdexnwp-40km-mis-0001.nc
synsat-nawdexnwp-40km-mis-0002.nc
synsat-nawdexnwp-40km-mis-0003.nc
synsat-nawdexnwp-40km-mis-0004.nc
synsat-nawdexnwp-40km-mis-0005.nc
synsat-nawdexnwp-40km-mis-0006.nc
synsat-nawdexnwp-40km-mis-0007.nc
synsat-nawdexnwp-40km-mis-0008.nc
synsat-nawdexnwp-40km-mis-0009.nc
synsat-nawdexnwp-40km-mis-0010.nc
synsat-nawdexnwp-5km-mis-0001.nc
synsat-nawdexnwp-5km-mis-0002.nc
synsat-nawdexnwp-5km-mis-0003.nc
synsat-nawdexnwp-5km-mis-0004.nc
synsat-nawdexnwp-5km-mis-0005.nc
synsat-nawdexnwp-5km-mis-0006.nc
synsat-nawdexnwp-5km-mis-0007.nc
synsat-nawdexnwp-5km-mis-0008.nc
synsat-nawdexnwp-5km-mis-0009.nc
synsat-nawdexnwp-5km-mis-0010.nc
synsat-nawdexnwp-5km-mis-0011.nc
synsat-nawdexnwp-5km-mis-0012.nc
synsat-nawdexnwp-80km-mis-0001.nc
synsat-nawdexnwp-80km-mis-0002.nc
synsat-nawdexnwp-80km-mis-0003.nc
synsat-nawdexnwp-80km-mis-0004.nc
synsat-nawdexnwp-80km-mis-0005.nc
synsat-nawdexnwp-80km-mis-0006.nc
synsat-nawdexnwp-80km-mis-0007.nc
synsat-nawdexnwp-80km-mis-0008.nc
synsat-nawdexnwp-80km-mis-0009.nc
synsat-nawdexnwp-80km-mis-0010.nc
```

An example content is
```
ncdump -h /vols/talos/home/fabian/data/icon/nawdex/synsat/synsat-nawdexnwp-80km-mis-0010.nc
netcdf synsat-nawdexnwp-80km-mis-0010 {
dimensions:
	time = 96 ;
	rows = 1004 ;
	cols = 2776 ;
	ndim = 2 ;
variables:
	short bt120(time, rows, cols) ;
		bt120:_FillValue = 0s ;
		bt120:units = "K" ;
		bt120:long_name = "Synthetic MSG SEVIRI Brightness Temperatures at 12.0 um" ;
		bt120:coordinates = "lat lon" ;
		bt120:scale_factor = 0.01 ;
	int64 msevi_region(ndim, ndim) ;
		msevi_region:long_name = "msg_seviri_region_cutout" ;
		msevi_region:description = "((row1, row2), (col1, col2))" ;
	short bt134(time, rows, cols) ;
		bt134:_FillValue = 0s ;
		bt134:units = "K" ;
		bt134:long_name = "Synthetic MSG SEVIRI Brightness Temperatures at 13.4 um" ;
		bt134:coordinates = "lat lon" ;
		bt134:scale_factor = 0.01 ;
	double zen(rows, cols) ;
		zen:units = "degrees" ;
		zen:lon0 = 0. ;
		zen:long_name = "satellite_zenith_angle" ;
		zen:coordinates = "lat lon" ;
	int64 nwcsaf_region(ndim, ndim) ;
		nwcsaf_region:long_name = "nwcsaf_region_cutout" ;
		nwcsaf_region:description = "((row_center, col_center), (nrows, ncols))" ;
	short bt087(time, rows, cols) ;
		bt087:_FillValue = 0s ;
		bt087:units = "K" ;
		bt087:long_name = "Synthetic MSG SEVIRI Brightness Temperatures at 8.7 um" ;
		bt087:coordinates = "lat lon" ;
		bt087:scale_factor = 0.01 ;
	short bt108(time, rows, cols) ;
		bt108:_FillValue = 0s ;
		bt108:units = "K" ;
		bt108:long_name = "Synthetic MSG SEVIRI Brightness Temperatures at 10.8 um" ;
		bt108:coordinates = "lat lon" ;
		bt108:scale_factor = 0.01 ;
	short bt073(time, rows, cols) ;
		bt073:_FillValue = 0s ;
		bt073:units = "K" ;
		bt073:long_name = "Synthetic MSG SEVIRI Brightness Temperatures at 7.3 um" ;
		bt073:coordinates = "lat lon" ;
		bt073:scale_factor = 0.01 ;
	short bt062(time, rows, cols) ;
		bt062:_FillValue = 0s ;
		bt062:units = "K" ;
		bt062:long_name = "Synthetic MSG SEVIRI Brightness Temperatures at 6.2 um" ;
		bt062:coordinates = "lat lon" ;
		bt062:scale_factor = 0.01 ;
	double lat(rows, cols) ;
		lat:units = "degrees_north" ;
		lat:long_name = "latitude" ;
	double lon(rows, cols) ;
		lon:units = "degrees_east" ;
		lon:long_name = "longitude" ;
	double time(time) ;
		time:units = "day as %Y%m%d.%f" ;
		time:long_name = "Time" ;
		time:calendar = "proleptic_gregorian" ;

// global attributes:
		:description = "Synthetic Infrared MSG-SEVIRI images from the Prime Service" ;
		:title = "Synthetic MSG-SEVIRI Brightness Temperatures" ;
		:institution = "Leibniz Institute for Tropospheric Research" ;
		:author = "Fabian Senf (senf@tropos.de)" ;
}
```


### NWCSAF patch

The cloud tpying is based on a patched version of the NWCSAF software version 2013. The patch
  * reads netcdf data (BTs)
  * output fake HRIT data with the considered BTs embedded
  * runs NWCSAF at permanent mid-night
  * emulates BTs from the 3.9 um channel (which are contaminated by sun light during day, but required by NWCSAF in night-mode)
 
The patching is done with the toolset hosted under
https://gitea.tropos.de/senf/proj.synNWCSAF


Further details are explained there.


### Synthetic cloud types
Cloud type data are stored under
```
ls -1 /vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf*nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-10km-mis-0001.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-10km-mis-0002.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-10km-mis-0003.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-10km-mis-0004.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-10km-mis-0005.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-10km-mis-0006.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-10km-mis-0007.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-10km-mis-0008.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-10km-mis-0009.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-10km-mis-0010.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-10km-mis-0011.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-10km-mis-0012.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-20km-mis-0001.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-20km-mis-0002.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-20km-mis-0003.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-20km-mis-0004.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-20km-mis-0005.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-20km-mis-0006.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-20km-mis-0007.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-20km-mis-0008.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-20km-mis-0009.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-20km-mis-0010.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-2km-mis-0001.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-2km-mis-0002.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-2km-mis-0003.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-2km-mis-0004.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-2km-mis-0005.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-2km-mis-0006.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-2km-mis-0007.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-2km-mis-0008.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-2km-mis-0009.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-2km-mis-0010.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-2km-mis-0011.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-2km-mis-0012.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-40km-mis-0001.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-40km-mis-0002.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-40km-mis-0003.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-40km-mis-0004.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-40km-mis-0005.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-40km-mis-0006.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-40km-mis-0007.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-40km-mis-0008.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-40km-mis-0009.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-40km-mis-0010.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-5km-mis-0001.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-5km-mis-0002.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-5km-mis-0003.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-5km-mis-0004.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-5km-mis-0005.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-5km-mis-0006.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-5km-mis-0007.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-5km-mis-0008.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-5km-mis-0009.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-5km-mis-0010.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-5km-mis-0011.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-5km-mis-0012.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-80km-mis-0001.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-80km-mis-0002.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-80km-mis-0003.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-80km-mis-0004.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-80km-mis-0005.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-80km-mis-0006.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-80km-mis-0007.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-80km-mis-0008.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-80km-mis-0009.nc
/vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-80km-mis-0010.nc
```

Example content is
```
ncdump -h /vols/talos/home/fabian/data/icon/nawdex/synsat/nwcsaf_synsat-nawdexnwp-80km-mis-0010.nc
netcdf nwcsaf_synsat-nawdexnwp-80km-mis-0010 {
dimensions:
	ndim = 2 ;
	time = 96 ;
	rows = 1004 ;
	cols = 2776 ;
variables:
	int64 msevi_region(ndim, ndim) ;
		msevi_region:long_name = "msg_seviri_region_cutout" ;
		msevi_region:description = "((row1, row2), (col1, col2))" ;
	int64 nwcsaf_region(ndim, ndim) ;
		nwcsaf_region:long_name = "nwcsaf_region_cutout" ;
		nwcsaf_region:description = "((row_center, col_center), (nrows, ncols))" ;
	short CTTH_HEIGHT(time, rows, cols) ;
		CTTH_HEIGHT:_FillValue = -1s ;
		CTTH_HEIGHT:units = "km" ;
		CTTH_HEIGHT:long_name = "cloud top height" ;
		CTTH_HEIGHT:description = "" ;
		CTTH_HEIGHT:coordinates = "lat lon" ;
		CTTH_HEIGHT:scale_factor = 200LL ;
	short CMa(time, rows, cols) ;
		CMa:_FillValue = -1s ;
		CMa:units = "km" ;
		CMa:long_name = "cloud top height" ;
		CMa:description = "" ;
		CMa:coordinates = "lat lon" ;
		CMa:scale_factor = 1LL ;
	short CT(time, rows, cols) ;
		CT:_FillValue = -1s ;
		CT:units = "km" ;
		CT:long_name = "cloud top height" ;
		CT:description = "" ;
		CT:coordinates = "lat lon" ;
		CT:scale_factor = 1LL ;
	double lat(rows, cols) ;
		lat:_FillValue = NaN ;
		lat:units = "degrees_north" ;
		lat:long_name = "latitutde" ;
	double lon(rows, cols) ;
		lon:_FillValue = NaN ;
		lon:units = "degrees_east" ;
		lon:long_name = "longitude" ;
	double time(time) ;
		time:_FillValue = NaN ;
		time:units = "day as %Y%m%d.%f" ;
		time:long_name = "Time" ;
		time:calendar = "proleptic_gregorian" ;

// global attributes:
		:description = "Based on synthetic Meteosat-SEVIRI images from the Prime Service" ;
		:title = "NWCSAF cloud products" ;
		:institution = "Leibniz Institute for Tropospheric Research" ;
		:author = "Fabian Senf (senf@tropos.de)" ;
}

```


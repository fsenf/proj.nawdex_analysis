# Simulated TOA Radiation and Cloud-Radiative Effects
## Original Simulation Data (on mistral)
### General File Location
All simulation files are saved on mistral under
```
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP
```

The following list is available:
```
find /work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP -type d -iname 'nawdexnwp*mis*'| sort
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-10km-mis-0001
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-10km-mis-0002
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-10km-mis-0003
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-10km-mis-0004
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-10km-mis-0005
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-10km-mis-0006
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-10km-mis-0007
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-10km-mis-0008
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-10km-mis-0009
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-10km-mis-0010
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-10km-mis-0011
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-10km-mis-0012
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-20km-mis-0001
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-20km-mis-0002
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-20km-mis-0003
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-20km-mis-0004
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-20km-mis-0005
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-20km-mis-0006
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-20km-mis-0007
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-20km-mis-0008
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-20km-mis-0009
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-20km-mis-0010
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0001
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0002
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0003
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0004
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0005
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0006
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0007
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0008
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0009
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0010
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0011
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0012
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-40km-mis-0001
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-40km-mis-0002
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-40km-mis-0003
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-40km-mis-0004
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-40km-mis-0005
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-40km-mis-0006
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-40km-mis-0007
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-40km-mis-0008
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-40km-mis-0009
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-40km-mis-0010
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-5km-mis-0001
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-5km-mis-0002
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-5km-mis-0003
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-5km-mis-0004
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-5km-mis-0005
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-5km-mis-0006
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-5km-mis-0007
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-5km-mis-0008
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-5km-mis-0009
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-5km-mis-0010
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-5km-mis-0011
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-5km-mis-0012
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-80km-mis-0001
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-80km-mis-0001_latbc
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-80km-mis-0001_with_icon-2.1.00
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-80km-mis-0002
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-80km-mis-0002_latbc
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-80km-mis-0003
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-80km-mis-0004
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-80km-mis-0005
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-80km-mis-0006
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-80km-mis-0007
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-80km-mis-0008
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-80km-mis-0009
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-80km-mis-0010
```

### Radiation Variables
The simulation data provide allsky radiation variable for up- and downwelling shortwave as well as longwave at TOA. Variable keys are  
```
['sod_t', 'sou_t', 'thb_t']       
```


Moreover, access to __net__ clearsky variables is possible. 
```
['swtoaclr', 'lwtoaclr']
```

The lev1 functions provide direct access to the data:
```
>>> import nawdex_analysis.io.input_sim as isim
>>> isim.read_icon_rad_vector??
```


### Georeference Mapping 
A mapper has been written that generates the georeference file name based on the forecast / simulation filename. All ICON geo-ref files are collected at

```
/work/bm0834/b380459/NAWDEX/grids
```


### Data Regridding
The simulation data will be regridded onto MSG grid for easy analysis and comparison. For regridding, two steps are needed.

1. Model Georeference is input and satellite zenith mask is calculated.
2. Model grid is mapped to SEVIRI grid.

Step one seems to be easy. Step two is a bit more complicated. One could generate and store a nearest neighbor index for the coarser model grids, but for the finer grid an other method should be applied. If several model grid box centers fall into one SEVIRI pixel then all radiances should be averaged (similar to an rediation-based averaging a satellite sensor would do).


Two sets of functions have been developed to regrid data, all are contained in the package `reproj`assessed by

```
>>>import nawdex_analysis.io.reproj as reproj
```

#### NN interpolation
The first set treats the nearest-neighbor-interpolation problem. Two steps are needed. First an interpolation index is calculated with

```
>>>index =  reproj.get_vector2msevi_index( vgeo )
```

where `vgeo` is a dictionary containing the geo reference. And second, the index (and some masking) is applied to a dataset (also dict).

```
>>>dset_nn_reproj =  reproj.nn_reproj_with_index( dset, ind ) 
```
The index must only be calculated once and can be applied thereafter in a very efficient way.

#### Box-average interpolation
The second set treats the box-average interpolation which is not trivial because the target grid is not rectangular. The calculation is also divided into two steps. First, reprojection parameters (depending on the grid) are calculated (similar to the nn index) with

```
>>>rparam = reproj.get_vector2msevi_rparam( vgeo )
```
where `vgeo` is again a dictionary containing the geo reference. A field is reprojected with

```
>>>fint = reproj.reproj_field(f, rparam)
```

#### Combined interpolation
The box averaging only fills grid boxes of the target grid that contain values from the initial simulation grid. For a coarse initial simulation grid, box averging results in a sparse dataset with missing values filled with Nans. Therefore, a combination of NN interpolation and box averaging is applied to a data set (again dict) using 

```
>>>dset_inter = reproj.combined_reprojection( dset, ind, rparam )
```

### Final Regridding Loops
The final regridding is done on mistral via the script:
```
cd /pf/b/b380352/proj/2017-07_nawdex_analysis/inout/
./save_reproj_sim_raddata.py /work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0001

```
The simulation path is the input argument and the final regridded data are saved under:
```
ls -1 /pf/b/b380352/data/nawdex/sim-toarad/
toa_clear_radflux-nawdexnwp-10km-mis-0001.nc
toa_clear_radflux-nawdexnwp-10km-mis-0002.nc
toa_clear_radflux-nawdexnwp-10km-mis-0003.nc
toa_clear_radflux-nawdexnwp-10km-mis-0004.nc
toa_clear_radflux-nawdexnwp-10km-mis-0005.nc
toa_clear_radflux-nawdexnwp-10km-mis-0006.nc
toa_clear_radflux-nawdexnwp-10km-mis-0007.nc
toa_clear_radflux-nawdexnwp-10km-mis-0008.nc
toa_clear_radflux-nawdexnwp-10km-mis-0009.nc
toa_clear_radflux-nawdexnwp-10km-mis-0010.nc
toa_clear_radflux-nawdexnwp-10km-mis-0011.nc
toa_clear_radflux-nawdexnwp-10km-mis-0012.nc
toa_clear_radflux-nawdexnwp-20km-mis-0001.nc
toa_clear_radflux-nawdexnwp-20km-mis-0002.nc
toa_clear_radflux-nawdexnwp-20km-mis-0003.nc
toa_clear_radflux-nawdexnwp-20km-mis-0004.nc
toa_clear_radflux-nawdexnwp-20km-mis-0005.nc
toa_clear_radflux-nawdexnwp-20km-mis-0006.nc
toa_clear_radflux-nawdexnwp-20km-mis-0007.nc
toa_clear_radflux-nawdexnwp-20km-mis-0008.nc
toa_clear_radflux-nawdexnwp-20km-mis-0009.nc
toa_clear_radflux-nawdexnwp-20km-mis-0010.nc
toa_clear_radflux-nawdexnwp-2km-mis-0001.nc
toa_clear_radflux-nawdexnwp-2km-mis-0002.nc
toa_clear_radflux-nawdexnwp-2km-mis-0003.nc
toa_clear_radflux-nawdexnwp-2km-mis-0004.nc
toa_clear_radflux-nawdexnwp-2km-mis-0005.nc
toa_clear_radflux-nawdexnwp-2km-mis-0006.nc
toa_clear_radflux-nawdexnwp-2km-mis-0007.nc
toa_clear_radflux-nawdexnwp-2km-mis-0008.nc
toa_clear_radflux-nawdexnwp-2km-mis-0009.nc
toa_clear_radflux-nawdexnwp-2km-mis-0010.nc
toa_clear_radflux-nawdexnwp-2km-mis-0011.nc
toa_clear_radflux-nawdexnwp-2km-mis-0012.nc
toa_clear_radflux-nawdexnwp-40km-mis-0001.nc
toa_clear_radflux-nawdexnwp-40km-mis-0002.nc
toa_clear_radflux-nawdexnwp-40km-mis-0003.nc
toa_clear_radflux-nawdexnwp-40km-mis-0004.nc
toa_clear_radflux-nawdexnwp-40km-mis-0005.nc
toa_clear_radflux-nawdexnwp-40km-mis-0006.nc
toa_clear_radflux-nawdexnwp-40km-mis-0007.nc
toa_clear_radflux-nawdexnwp-40km-mis-0008.nc
toa_clear_radflux-nawdexnwp-40km-mis-0009.nc
toa_clear_radflux-nawdexnwp-40km-mis-0010.nc
toa_clear_radflux-nawdexnwp-5km-mis-0001.nc
toa_clear_radflux-nawdexnwp-5km-mis-0002.nc
toa_clear_radflux-nawdexnwp-5km-mis-0003.nc
toa_clear_radflux-nawdexnwp-5km-mis-0004.nc
toa_clear_radflux-nawdexnwp-5km-mis-0005.nc
toa_clear_radflux-nawdexnwp-5km-mis-0006.nc
toa_clear_radflux-nawdexnwp-5km-mis-0007.nc
toa_clear_radflux-nawdexnwp-5km-mis-0008.nc
toa_clear_radflux-nawdexnwp-5km-mis-0009.nc
toa_clear_radflux-nawdexnwp-5km-mis-0010.nc
toa_clear_radflux-nawdexnwp-5km-mis-0011.nc
toa_clear_radflux-nawdexnwp-5km-mis-0012.nc
toa_clear_radflux-nawdexnwp-80km-mis-0001.nc
toa_clear_radflux-nawdexnwp-80km-mis-0002.nc
toa_clear_radflux-nawdexnwp-80km-mis-0003.nc
toa_clear_radflux-nawdexnwp-80km-mis-0004.nc
toa_clear_radflux-nawdexnwp-80km-mis-0005.nc
toa_clear_radflux-nawdexnwp-80km-mis-0006.nc
toa_clear_radflux-nawdexnwp-80km-mis-0007.nc
toa_clear_radflux-nawdexnwp-80km-mis-0008.nc
toa_clear_radflux-nawdexnwp-80km-mis-0009.nc
toa_clear_radflux-nawdexnwp-80km-mis-0010.nc
toa_radflux-nawdexnwp-10km-mis-0001.nc
toa_radflux-nawdexnwp-10km-mis-0002.nc
toa_radflux-nawdexnwp-10km-mis-0003.nc
toa_radflux-nawdexnwp-10km-mis-0004.nc
toa_radflux-nawdexnwp-10km-mis-0005.nc
toa_radflux-nawdexnwp-10km-mis-0006.nc
toa_radflux-nawdexnwp-10km-mis-0007.nc
toa_radflux-nawdexnwp-10km-mis-0008.nc
toa_radflux-nawdexnwp-10km-mis-0009.nc
toa_radflux-nawdexnwp-10km-mis-0010.nc
toa_radflux-nawdexnwp-10km-mis-0011.nc
toa_radflux-nawdexnwp-10km-mis-0012.nc
toa_radflux-nawdexnwp-20km-mis-0001.nc
toa_radflux-nawdexnwp-20km-mis-0002.nc
toa_radflux-nawdexnwp-20km-mis-0003.nc
toa_radflux-nawdexnwp-20km-mis-0004.nc
toa_radflux-nawdexnwp-20km-mis-0005.nc
toa_radflux-nawdexnwp-20km-mis-0006.nc
toa_radflux-nawdexnwp-20km-mis-0007.nc
toa_radflux-nawdexnwp-20km-mis-0008.nc
toa_radflux-nawdexnwp-20km-mis-0009.nc
toa_radflux-nawdexnwp-20km-mis-0010.nc
toa_radflux-nawdexnwp-2km-mis-0001.nc
toa_radflux-nawdexnwp-2km-mis-0002.nc
toa_radflux-nawdexnwp-2km-mis-0003.nc
toa_radflux-nawdexnwp-2km-mis-0004.nc
toa_radflux-nawdexnwp-2km-mis-0005.nc
toa_radflux-nawdexnwp-2km-mis-0006.nc
toa_radflux-nawdexnwp-2km-mis-0007.nc
toa_radflux-nawdexnwp-2km-mis-0008.nc
toa_radflux-nawdexnwp-2km-mis-0009.nc
toa_radflux-nawdexnwp-2km-mis-0010.nc
toa_radflux-nawdexnwp-2km-mis-0011.nc
toa_radflux-nawdexnwp-2km-mis-0012.nc
toa_radflux-nawdexnwp-40km-mis-0001.nc
toa_radflux-nawdexnwp-40km-mis-0002.nc
toa_radflux-nawdexnwp-40km-mis-0003.nc
toa_radflux-nawdexnwp-40km-mis-0004.nc
toa_radflux-nawdexnwp-40km-mis-0005.nc
toa_radflux-nawdexnwp-40km-mis-0006.nc
toa_radflux-nawdexnwp-40km-mis-0007.nc
toa_radflux-nawdexnwp-40km-mis-0008.nc
toa_radflux-nawdexnwp-40km-mis-0009.nc
toa_radflux-nawdexnwp-40km-mis-0010.nc
toa_radflux-nawdexnwp-5km-mis-0001.nc
toa_radflux-nawdexnwp-5km-mis-0002.nc
toa_radflux-nawdexnwp-5km-mis-0003.nc
toa_radflux-nawdexnwp-5km-mis-0004.nc
toa_radflux-nawdexnwp-5km-mis-0005.nc
toa_radflux-nawdexnwp-5km-mis-0006.nc
toa_radflux-nawdexnwp-5km-mis-0007.nc
toa_radflux-nawdexnwp-5km-mis-0008.nc
toa_radflux-nawdexnwp-5km-mis-0009.nc
toa_radflux-nawdexnwp-5km-mis-0010.nc
toa_radflux-nawdexnwp-5km-mis-0011.nc
toa_radflux-nawdexnwp-5km-mis-0012.nc
toa_radflux-nawdexnwp-80km-mis-0001.nc
toa_radflux-nawdexnwp-80km-mis-0002.nc
toa_radflux-nawdexnwp-80km-mis-0003.nc
toa_radflux-nawdexnwp-80km-mis-0004.nc
toa_radflux-nawdexnwp-80km-mis-0005.nc
toa_radflux-nawdexnwp-80km-mis-0006.nc
toa_radflux-nawdexnwp-80km-mis-0007.nc
toa_radflux-nawdexnwp-80km-mis-0008.nc
toa_radflux-nawdexnwp-80km-mis-0009.nc
toa_radflux-nawdexnwp-80km-mis-0010.nc
```

Output is splitted between all- and clear-sky.

## Regridded Simulation Data (altair / TROPOS store)
Data have been transfered to TROPOS and are actually saved at
```
 /vols/talos/home/fabian/data/icon/nawdex/sim-toarad/
```

### Example Output
An example of the TOA radiation file is given here:
```
ncdump -h /vols/talos/home/fabian/data/icon/nawdex/sim-toarad/toa_radflux-nawdexnwp-10km-mis-0001.nc
netcdf toa_radflux-nawdexnwp-10km-mis-0001 {
dimensions:
	time = 96 ;
	rows = 1004 ;
	cols = 2776 ;
variables:
	short swf_up(time, rows, cols) ;
		swf_up:_FillValue = 0s ;
		swf_up:units = "W m**(-2)" ;
		swf_up:long_name = "TOA  short-wave upwelling radiation flux" ;
		swf_up:coordinates = "lat lon" ;
		swf_up:scale_factor = 0.25 ;
	short swf_net(time, rows, cols) ;
		swf_net:_FillValue = 0s ;
		swf_net:units = "W m**(-2)" ;
		swf_net:long_name = "TOA  short-wave net radiation flux" ;
		swf_net:coordinates = "lat lon" ;
		swf_net:scale_factor = 0.25 ;
	short lwf(time, rows, cols) ;
		lwf:_FillValue = 0s ;
		lwf:units = "W m**(-2)" ;
		lwf:long_name = "TOA  long-wave radiation flux" ;
		lwf:coordinates = "lat lon" ;
		lwf:scale_factor = 0.25 ;
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
		:description = "instantaneous  TOA radiation fluxes simulated with ICON" ;
		:title = "TOA  Radiation Fluxes" ;
		:institution = "Leibniz Institute for Tropospheric Research" ;
		:author = "Fabian Senf (senf@tropos.de)" ;
}
```

### Generic Input
The level2 function
```
import nawdex_analysis.io.input_lev2 as ilev2
ilev2.read_data_field??
```

provides the functionality to input these data together with georef and regional masks.


### Input for CRE analysis
There is a second input functionality (collector) that reads allsky together with clearsky together with cloud type. This helps for the CRE calculations
```
ilev2.collect_data4cre_sim??
```


### Average CRE
The analysis toolset 
```
import  nawdex_analysis.analysis.ave_cre as acre
acre.ave_cre_from_radname
acre.ave_radfluxes_from_radname
```
provides functions to calculate domain-average CRE and radiation fluxes depending on cloud type as function of time. Looping over time index within each radfile is also possible.

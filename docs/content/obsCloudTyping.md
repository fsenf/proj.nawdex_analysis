# Observed Cloud Typing
## Simulation Data (on mistral)
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


### Georeference Mapping 
A mapper has been written that generates the georeference file name based on the forecast / simulation filename. All ICON geo-ref files are collected at

```
/work/bm0834/b380459/NAWDEX/grids
```

### Synthetic Satellite Data Calculation
The ICON simulation data have been transfered to DKRZ Mistral by Aiko Voigt. The "Synsat" forward operator has been applied to the simulation data using the script 
```
/pf/b/b380352/proj/2015-12_synsat/synsats4icon_nawdex/synsat_icon-nawdex.py
```
The script takes the `fg` filename as argument. The calculation are restricted to a satellite zenith angle of <75 degrees. The synsat data are saved as brightness temperatures for several infrared SEVIRI bands into hdf5 files. They are vectors using the mask = zen < 75 and are discretized as 0.01 Kelvin. Hence, the georeference and the masking condition is needed to recover the synsat data on the native model grid (which is also a vector in our case).

One example is e.g.
```
cd data/synsat/nawdex/nawdexnwp-20km-mis-0001/

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
For regridding of synsat data, two steps are needed.

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




## Observational Data (on TROPOS altair)
### TOA Radiation fluxes
TOA Radiation fluxes have been provided by Nicola Clerbaux (Belgium) as hdf5 files. The data are saved as `H5T_STD_I16BE` which means signed 16-bit integer (big endian). On TROPOS altair, TOA radiation data are saved under
```
/vols/talos/home/fabian/data/gerb-like
```
A NaN values seems to be set to -32767 (and need to be masked) and all other values have to be multiplied by 0.25 get to radiation fluxes with unit Wm**(-2).

#### Input of Data
Functions to read and cutout TOA radiation flux data are available under pyhton package `nawdex_analysis.io.input_obs`.

The calls 
```
>>>import nawdex_analysis.io.input_obs as ioobs
>>>lwf, swf_net = ioobs.read_radiation_fluxes( t )
``` 
read observed long-wave fluxes (`lwf`) and net short-wave flux (`swf_net`) scaled to SEVIRI grid.

#### Cutout of data
We only use a certain SEVIRI cutout for data analysis. This variable is saved under `nawdex_analysis.config`. An option to input cutted data on-the-fly is incorporated into `ioobs.read_radiation_fluxes( t )`.

#### Output daily stacks to netcdf
To ease later analysis, daily stacks of TOA radiation flux data have been saved into netcdf format using 

```
>>>import nawdex_analysis.io.output_obs as oobs
>>>oobs.save_radflux_tstack( date )
```


### SEVIRI BT data
SEVIRI BT are directly read out of the TROPOS archive at altair using the `ioobs.read_msevi(t1,t2)` where `t1` and `t2` are start and end time of the BT data stack.

The finally daily BT fields are output into netcdf files which are generated by 

```
>>>import nawdex_analysis.io.output_obs as oobs
>>>oobs.save_meteosat_tstack( date )
```
where `date` is a date string.

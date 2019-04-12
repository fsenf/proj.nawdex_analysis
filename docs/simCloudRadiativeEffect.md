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


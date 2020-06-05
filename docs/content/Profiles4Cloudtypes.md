# Vertical Profiles for different Cloud Types
As part of an in-depth analysis of the characteristics of the different ICON simulations, it become apparent that a comparison of different vertical profiles will be beneficial. Here, it is described 
* how vertical profiles for different cloud types are derived and 
* how the python package `nawdex_analysis`is used for that purpose

## General Structure of Intended Profile Data 
Following ideas are summarized:
* the data should be representative for a region / sub-domain which is chosen to cover several grid boxes of the coarser simulations
* the cloud typing fields are given in SEVIRI projection - we need to map the simulation data first to this projection and then do the spatial aggregation into sub-domains thereafter
* data will be 5-dimensional with `(time, lon, lat, level, cloud_type)` `lon` and `lat` refer to the centers of the sub-domains

### Cloud Type Data

### Simulation Data
Are stored under:
```
cd /work/bb1018/b380459/NAWDEX/ICON_OUTPUT_NWP
```

Several Experiments exist:
```
> ls -1
nawdexnwp-10km-mis-0001
nawdexnwp-10km-mis-0002
nawdexnwp-10km-mis-0003
nawdexnwp-10km-mis-0004
nawdexnwp-10km-mis-0005
nawdexnwp-10km-mis-0006
nawdexnwp-10km-mis-0007
nawdexnwp-10km-mis-0008
nawdexnwp-10km-mis-0009
nawdexnwp-10km-mis-0010
nawdexnwp-10km-mis-0011
nawdexnwp-10km-mis-0012
nawdexnwp-1km-mis-0002
nawdexnwp-1km-mis-0003
nawdexnwp-1km-mis-0004
nawdexnwp-1km-mis-0005
nawdexnwp-20km-mis-0001
nawdexnwp-20km-mis-0002
nawdexnwp-20km-mis-0003
nawdexnwp-20km-mis-0004
nawdexnwp-20km-mis-0005
nawdexnwp-20km-mis-0006
nawdexnwp-20km-mis-0007
nawdexnwp-20km-mis-0008
nawdexnwp-20km-mis-0009
nawdexnwp-20km-mis-0010
nawdexnwp-2km-mis-0001
nawdexnwp-2km-mis-0001-shcon
nawdexnwp-2km-mis-0002
nawdexnwp-2km-mis-0002-shcon
nawdexnwp-2km-mis-0003
nawdexnwp-2km-mis-0004
nawdexnwp-2km-mis-0005
nawdexnwp-2km-mis-0005-shcon
nawdexnwp-2km-mis-0006
nawdexnwp-2km-mis-0006-shcon
nawdexnwp-2km-mis-0007
nawdexnwp-2km-mis-0007c
nawdexnwp-2km-mis-0007-shcon
nawdexnwp-2km-mis-0008
nawdexnwp-2km-mis-0008c
nawdexnwp-2km-mis-0008-shcon
nawdexnwp-2km-mis-0009
nawdexnwp-2km-mis-0009-shcon
nawdexnwp-2km-mis-0010
nawdexnwp-2km-mis-0010-shcon
nawdexnwp-2km-mis-0011
nawdexnwp-2km-mis-0011-shcon
nawdexnwp-2km-mis-0012
nawdexnwp-2km-mis-0012-shcon
nawdexnwp-2km-mis-0013
nawdexnwp-40km-mis-0001
nawdexnwp-40km-mis-0002
nawdexnwp-40km-mis-0003
nawdexnwp-40km-mis-0004
nawdexnwp-40km-mis-0005
nawdexnwp-40km-mis-0006
nawdexnwp-40km-mis-0007
nawdexnwp-40km-mis-0008
nawdexnwp-40km-mis-0009
nawdexnwp-40km-mis-0010
nawdexnwp-5km-mis-0001
nawdexnwp-5km-mis-0002
nawdexnwp-5km-mis-0003
nawdexnwp-5km-mis-0004
nawdexnwp-5km-mis-0005
nawdexnwp-5km-mis-0006
nawdexnwp-5km-mis-0007
nawdexnwp-5km-mis-0008
nawdexnwp-5km-mis-0009
nawdexnwp-5km-mis-0010
nawdexnwp-5km-mis-0011
nawdexnwp-5km-mis-0012
nawdexnwp-80km-mis-0001
nawdexnwp-80km-mis-0002
nawdexnwp-80km-mis-0003
nawdexnwp-80km-mis-0004
nawdexnwp-80km-mis-0005
nawdexnwp-80km-mis-0006
nawdexnwp-80km-mis-0007
nawdexnwp-80km-mis-0008
nawdexnwp-80km-mis-0009
nawdexnwp-80km-mis-0010
nawdexnwp-80km-mis-0011
```

The data are typically 2-dimensional ( one horizontal dimension `ncells` and one vertical dimension ). The data are stroed for different times separately.
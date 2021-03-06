# Quick Restart
This document should help to quickly redo all analysis steps when new simulations are available.

## Synsats (Mistral)
### Calculation

* Go to the synsat scripts directory
```
cd ${HOME}/proj/2015-12_synsat/synsats4icon_nawdex
```

* Make a list (also change listname...)
```
EXPDIR=/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0002-shcon/
find ${EXPDIR} -iname '*fg*nc' | sort > lists/nawdexnwp-2km-mis-0002-shcon.lst
``` 

* Split list into parts if runs should be distributed across several mistralpp nodes
```
split -d -l 48 nawdexnwp-2km-mis-0002-shcon.lst nawdexnwp-2km-mis-0002-shcon.lst
```

* Open screen
```
screen -S synsat
. ~/.profile
```

* Parallel synsat runs
```
 start_proc_from_list -n 4 ./synsat_icon-nawdex.py lists/nawdexnwp-2km-mis-0001-shcon.lst01
```

* Wait 


### Regridding

After all synsat runs are finished: Regridding is done in parts (memory and speed issue)

* go to the dir
```
cd ${HOME}/proj/2017-07_nawdex_analysis/inout
./save_reproj_synsat.py ${HOME}/data/synsat/nawdex/nawdexnwp-80km-mis-0001
```

* make a list file that looks like this (default: 6 lines = 6 chunks). `vim regrid_synsat10.lst`
```
/pf/b/b380352/data/synsat/nawdex/nawdexnwp-2km-mis-0010-shcon 0 
/pf/b/b380352/data/synsat/nawdex/nawdexnwp-2km-mis-0010-shcon 1
/pf/b/b380352/data/synsat/nawdex/nawdexnwp-2km-mis-0010-shcon 2
/pf/b/b380352/data/synsat/nawdex/nawdexnwp-2km-mis-0010-shcon 3
/pf/b/b380352/data/synsat/nawdex/nawdexnwp-2km-mis-0010-shcon 4
/pf/b/b380352/data/synsat/nawdex/nawdexnwp-2km-mis-0010-shcon 5
```

* open a screen `screen -S regrid_synsat10`

* run 
```
start_proc_from_list -n 6 ./save_reproj_synsat_in_parts.py regrid_synsat10.lst
```

* goto the parts output dir
```
cd ~/data/nawdex/synsat-parts/
```

* combine file parts with cdo
```
cdo -z zip_4 cat synsat-nawdexnwp-2km-mis-0010-shcon-part?.nc synsat-nawdexnwp-2km-mis-0010-shcon.nc
```

* move the combine into the `../synsat` directory




## Combined Radiation Fluxes
### Regridding (Mistral)

__Similar to synsat regridding!!!__

Regridding is done in parts (memory and speed issue)

* go to the dir
```
cd ${HOME}/proj/2017-07_nawdex_analysis/inout/
```

* make a list file that looks like this (default: 6 lines = 6 chunks). `vim regrid_radflux10.lst`
```
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0010-shcon 0
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0010-shcon 1
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0010-shcon 2
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0010-shcon 3
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0010-shcon 4
/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0010-shcon 5
```

* open a screen `screen -S regrid_radflux10`

* run 
```
start_proc_from_list -n 6 ./save_reproj_sim_raddata_in_parts.py regrid_radflux10.lst
```

* goto the parts output dir
```
cd ~/data/nawdex/sim-toarad-parts/
```

* combine file parts with cdo
```
cdo -z zip_4 cat toa_clear_radflux-nawdexnwp-2km-mis-0010-shcon-part?.nc toa_clear_radflux-nawdexnwp-2km-mis-0010-shcon.nc
cdo -z zip_4 cat toa_radflux-nawdexnwp-2km-mis-0010-shcon-part?.nc toa_radflux-nawdexnwp-2km-mis-0006-shcon.nc
```

* move the combine into the `../sim-toarad` directory



### Transfer to TROPOS (Gauss)
Copy data to Gauss
```
cd ${LHOME}/data/icon/nawdex/sim-toarad
scp -r b380352@mistralpp.dkrz.de:/pf/b/b380352/data/nawdex/sim-toarad/*shcon.nc .
```

## Cloud Typing (Gauss)

### Transfer of Synsats to Gauss
Copy data to Gauss
```
cd  ${LHOME}/data/icon/nawdex/synsat/
scp -r b380352@mistralpp.dkrz.de:/pf/b/b380352/data/nawdex/synsat/*shcon.nc .
```

### Run Cloud Typing
```
cd ${LHOME}/proj/2019-08_NWCSAF/synNWCSAF/scripts
./run_NWCSAF4synsat ${LHOME}/data/icon/nawdex/synsat/synsat-nawdexnwp-2km-mis-0001.nc
```

## CRE (Gauss)
If regridded Radflux files & Synsat files are complete, then derived average rad-fluxes per CT (level3 data)

```
cd ${LHOME}/proj/2017-07_icon-nawdex/inout
./save_ave_radfluxes.py ${LHOME}/data/icon/nawdex/sim-toarad/toa_radflux-nawdexnwp-2km-mis-0001-shcon.nc
```

where the full filename refers to the regidded radflux file.


## Adjusting the Naming Scheme

The new expermients might have new names, e.g. `nawdexnwp-2km-mis-0001-shcon`. The new experiment need to be mapped into experiment categories.

`nawdex_analysis.io.selector` has to be modified.


* Go to the `nawdex_analysis` package development path
```
cd ${LHOME}/proj/2018-05_pypackage_devel/nawdex_analysis/nawdex_analysis/io
```

* Modify `selector.py`
```
emacs selector.py
```

* Change Version Number
```
cd ${LHOME}/proj/2018-05_pypackage_devel/nawdex_analysis/nawdex_analysis
vim _version.py
```

* Install new package version into thew system
```
cd ..
pip install --upgrade .
```
 




# Quick Restart
This document should help to quickly redo all analysis steps when new simulations are available.

## Synsats (Mistral)
### Calculation

* Go to the synsat scripts directory
```
cd /pf/b/b380352/proj/2015-12_synsat/synsats4icon_nawdex
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

After all synsat runs are finished (change the path to the synsats...)
```
cd ~/proj/2017-07_nawdex_analysis/inout
./save_reproj_synsat.py /pf/b/b380352/data/synsat/nawdex/nawdexnwp-80km-mis-0001
```




## Combined Radiation Fluxes (Mistral)

* Go to the nawdex scripts directory
```
cd /pf/b/b380352/proj/2017-07_nawdex_analysis/inout/
```

* Run Rad Flux regridding (!!!no trailing '/' in the path name!!!)

```
./save_reproj_sim_raddata.py /work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP/nawdexnwp-2km-mis-0001
``` 

## CRE (Gauss)
* Copy data to Gauss
```
cd /vols/fs1/store/senf/data/icon/nawdex/sim-toarad
scp -r b380352@mistralpp.dkrz.de:/pf/b/b380352/data/nawdex/sim-toarad/*shcon.nc .
```



## Cloud Typing (Gauss)
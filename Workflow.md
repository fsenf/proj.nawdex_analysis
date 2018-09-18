# Typical Workflow
## Simulation Data 
### Georeference Mapping
A mapper has been written that generates the georeference file name based on the forecast / simulation filename.

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


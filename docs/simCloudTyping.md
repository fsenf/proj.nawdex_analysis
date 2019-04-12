# Simulated Cloud Typing

## Synthetic Satellite Data Calculation
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
Regridding of synsat data is done with the tools described [here](simCloudRadiativeEffect.md)

## Synthetic Cloud Typing
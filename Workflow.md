# Typical Workflow
## Simulation Data 
### Georeference Mapping
A mapper has been written that generates the georeference file name based on the forecast / simulation filename.

### Synthetic Satellite Data
The ICON simulation data have been transfered to DKRZ Mistral by Aiko Voigt. The "Synsat" forward operator has been applied to the simulation data using the script 
```
/pf/b/b380352/proj/2015-12_synsat/synsats4icon_nawdex/synsat_icon-nawdex.py
```
The script takes the `fg` filename as argument. The calculation are restricted to a satellite zenith angle of <75 degrees. The synsat data are saved as brightness temperatures for several infrared SEVIRI bands into hdf5 files. They are vectors using the mask = zen < 75 and are discretized as 0.01 Kelvin. Hence, the georeference and the masking condition is needed to recover the synsat data as SEVIRI disk cutout.
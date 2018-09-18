# NAWDEX Analysis Toolset
This is a set of tools developed for the anaylsis of ICON simulations during the NAWDEX campaign. The study is done together with Aiko Voigt and will focus on cloud radiative effects in the Northern Atlantic and its dependence on grid spacing and microphysics parameterization.

## Typical Workflow
### Simulation Data and Synthetic Satellite Data
The ICON simulation data have been transfered to DKRZ Mistral by Aiko Voigt. The "Synsat" forward operator has been applied to the simulation data using the script 
```
/pf/b/b380352/proj/2015-12_synsat/synsats4icon_nawdex/synsat_icon-nawdex.py
```
The calculation are restricted to a satellite zenith angle of <70 degree.
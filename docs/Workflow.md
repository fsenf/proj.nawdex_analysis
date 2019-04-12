# Typical Workflow

We have two target quantities which will be derived from the analysis
  * net TOA radiation fields including the so-called cloud-radiative effect (CRE)
  * cloud typing (also based on TOA radiation observation

Both analysis targets will be derived from observations (esp. using Meteosat data) nad from simulation using ICON-NWP data.

## Analysis of Simulation Data
Simulation data are given on a icosahedral grid with different grid spacings. The following analysis steps are explained
  * regridding and preparation of TOA radiation fluxes for CRE calculation [simCloudRadiativeEffect.md]
  * 
# NAWDEX Analysis Toolset
## General Description
This is a set of tools developed for the analysis of ICON simulations during the NAWDEX campaign. The study is done together with Aiko Voigt (KIT) and will focus on observed and simulated cloud radiative effects in the Northern Atlantic and their dependence on grid spacing and microphysics parameterization.

## Data 
Two types of data go into the study: (i) observational data derived from Meteosat SEVIRI including cloud mask, cloud typing and long- and short-wave radiative fluxes, and (ii) simulation data obtained from differently configured ICON runs.

## Method
The simulation data will be transfered to observation space. Thereafter, synthetic cloud mask and typing is derived via the NWCSAF software. Cloud radiative effects are calculated. For observations, simulated clear-sky fluxes are used. More details about the workflow are described [here](docs/Workflow.md).

## Paper
The paper 

Senf, F., A. Voigt, N. Clerbaux, A. Hünerbein, and H. Deneke, Does increasing resolution and resolving convection improve simulated cloud-radiative effects over the North Atlantic?, J. Geophys. Res. Atmos., submitted in Jan. 2020

uses the package `nawdex_analysis` 

* to read (level-1.5) observation and simulation data (radiation fluxes and cloud types)
* to derived regridded (satellite grid) data to be analyzed (level-2)
* to performed statistical analysis (level-3)
* to make the plots / plot styles shown in the paper

The notebooks used for the paper plot are provide [here](https://github.com/fsenf/nbook.2018-11_CRE-Nawdex-Aiko)

# Collection of ToDos and Ideas for Future Development

## Clean-up Tasks
### Python Scripts

Domain-average cloud Cover and cloud-radiative effect are derived with these python scripts

```
cd /vols/talos/home/fabian/proj/2017-07_icon-nawdex/inout
ll save_nwcsaf_histograms_nawdex_analysis.py   save_ave_simulated_cre.py save_ave_observed_cre.py
```

These scripts contain analysis and output functions that should be merged into this library.

### Notebooks
We have a set of notebooks

http://localhost:8787/notebooks/proj/2017-07_icon-nawdex/nbooks/12-plot_cc_tseries_for_simulationsets.ipynb
http://localhost:8787/notebooks/proj/2017-07_icon-nawdex/nbooks/15-plot_cloudtype_statistics.ipynb
http://localhost:8787/notebooks/proj/2017-07_icon-nawdex/nbooks/16-plot_cre_statistics.ipynb

that are very dirty - a lot of different tasks and duplciates in there.

They do 
* input of CC and CRE data, 
* stacking, 
* set selection and collection --> output rearranged data 
* plotting of CC and CRE vs. cloud type plots

It would be great
* to have a common format for set collections and full collections 
* to include clear-sky fractions and CRE
* to define an extra data dimension of variables like LCRE, SCRE, etc or/and an extra dimension for experiments


## Analysis Task
* analysis clear-sky CRE --> bias in short- and longwave will give information about cloud masking, clearsky estimation
* 



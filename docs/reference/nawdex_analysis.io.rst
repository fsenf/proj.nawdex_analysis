nawdex_analysis.io package
==========================

The package controlls input fields to be analyzed and also 
give some tools to write output.


A distinction is made between 

* primary input fields that might have very different grids
* second analysis fields (on the same SEVIRI grid), level-2 data


Functions Overview
------------------
.. rubric:: nawdex_analysis.io.collector

A summary of functions that are contained in
the `nawdex_analysis.io.collector` module.

.. currentmodule:: nawdex_analysis.io.collector

.. autosummary::
   :toctree: generated/
   :nosignatures:

   collect_sim_ave_cre4set
   get_obs_cre4time_list
   get_cre4set
   get_radflux4set
   get_stat4set
   get_stat4all


.. rubric:: nawdex_analysis.io.input_lev2

A summary of functions that are contained in
the `nawdex_analysis.io.input_lev2` module.

.. currentmodule:: nawdex_analysis.io.input_lev2

.. autosummary::
   :toctree: generated/
   :nosignatures:

   read_mask
   read_data_field
   radname2ctname
   collect_data4cre_obs
   collect_data4cre_sim
   collect_data4cre


.. rubric:: nawdex_analysis.io.input_obs

A summary of functions that are contained in
the `nawdex_analysis.io.input_obs` module.

.. currentmodule:: nawdex_analysis.io.input_obs

.. autosummary::
   :toctree: generated/
   :nosignatures:

   msevi_setting
   read_msevi
   scale_radiation
   read_radiation_fluxes
   read_solar_flux
   read_cc_from_fluxdata
   read_radiation_flux_tstack


.. rubric:: nawdex_analysis.io.input_sim

A summary of functions that are contained in
the `nawdex_analysis.io.input_sim` module.

.. currentmodule:: nawdex_analysis.io.input_sim

.. autosummary::
   :toctree: generated/
   :nosignatures:

   subdir_from_fname
   get_grid_filename
   get_synsat_basename
   read_georef
   get_zen_mask
   read_synsat_vector
   read_iconvar_vector
   read_icon_rad_vector
   read_time
   read_generic_sim_data_flist
   read_radiation_flux_flist
   read_synsat_flist
   read_simulated_clearsky_flux


.. rubric:: nawdex_analysis.io.output_obs

A summary of functions that are contained in
the `nawdex_analysis.io.output_obs` module.

.. currentmodule:: nawdex_analysis.io.output_obs

.. autosummary::
   :toctree: generated/
   :nosignatures:

   save_meteosat_tstack
   save_meteosat_bt2nc
   save_radflux_tstack
   save_rad2nc


.. rubric:: nawdex_analysis.io.output_sim

A summary of functions that are contained in
the `nawdex_analysis.io.output_sim` module.

.. currentmodule:: nawdex_analysis.io.output_sim

.. autosummary::
   :toctree: generated/
   :nosignatures:

   save_synsat_flist
   save_synsat_bt2nc
   save_radflux_flist
   save_rad2nc
   save_retrieved_clearsky_swf2nc


.. rubric:: nawdex_analysis.io.reproj

A summary of functions that are contained in
the `nawdex_analysis.io.reproj` module.

.. currentmodule:: nawdex_analysis.io.reproj

.. autosummary::
   :toctree: generated/
   :nosignatures:

   set_msevi_proj
   msevi_ll2xy
   msevi_xy2ij
   msevi_ij2xy
   msevi_ij2ll
   msevi_lonlat
   slice2nwcsaf_region
   nwcsaf_region2slice
   get_vector2msevi_index
   get_msevi2vector_index
   nn_reproj_with_index
   get_reproj_param
   reproj_field
   get_vector2msevi_rparam
   combined_reprojection


.. rubric:: nawdex_analysis.io.selector

A summary of functions that are contained in
the `nawdex_analysis.io.selector` module.

.. currentmodule:: nawdex_analysis.io.selector

.. autosummary::
   :toctree: generated/
   :nosignatures:

   check_if_nc_has_varname
   check_if_nc_has_time
   check_varname_and_time_in_nc
   make_filetime_index
   set_selector
   set_initdate
   gather_simset
   extra_experiments
   set_dateslices
   expname2conf_str
   convert_explist2idlist


.. rubric:: nawdex_analysis.io.tools

A summary of functions that are contained in
the `nawdex_analysis.io.tools` module.

.. currentmodule:: nawdex_analysis.io.tools

.. autosummary::
   :toctree: generated/
   :nosignatures:

   convert_time
   convert_timevec
   roundTime
   round2day
   lonlat2azizen




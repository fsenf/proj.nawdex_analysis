#!/usr/bin/env python

import os, sys, glob
import numpy as np

import xarray as xr
import pandas as pd

from nawdex_analysis.config import nawdex_dir
from selector import  gather_simset, expname2conf_str, set_dateslices


'''
This is a pachake that collects data for different sets.
'''


######################################################################
######################################################################

def collect_sim_ave_cre4set( set_number, 
                             file_format = 'default', 
                             allowed_set_range = [1,4] ):

    '''
    Collects average CRE data for a selected set.


    Parameters
    ----------
    set_number : int
       numeric identifier of a selected experiment set.

    file_format : str, optional, default = 'default'
       a string that defines file format, 
       restriction: two %s are needed at the moment

    allowed_set_range : list, optional, default = [1, 4]
       min & max of the allow set range

    
    Returns
    --------
    dset_sim : xarray Dataset
       set that contains time series of simulated CRE effects.

    '''

    if set_number < allowed_set_range[0] or set_number > allowed_set_range[1]:
        raise ValueError('set_number is outside allowed range')
    

    # get experiment list
    # ====================
    explist = gather_simset( set_number )
    date_slice = set_dateslices( set_number )


    if file_format == 'default':
        file_format = '%s/statistics/ave_cre-%s.nc' 


    # collect the CRE data 
    # ====================
    dlist = []
    for expname in explist:
        
        # open dataset
        fname = file_format % (nawdex_dir, expname)
        d = xr.open_dataset( fname )
        

        # this makes an expanded copy
        dex = d.expand_dims('idname', axis = -1)

        
        idname = expname2conf_str( expname )
        dex['expname'] = xr.DataArray([expname, ], dims='idname')
        dex['idname'] = [idname, ]
        
        dlist += [dex.copy(), ]
        
    dset_sim = xr.merge( dlist )

    return dset_sim.sel( time = date_slice )


######################################################################
######################################################################


def get_obs_cre4time_list( time, file_part ='-scaled'):


    '''
    Collects average CRE data for a selected set.


    Parameters
    ----------
    time : xarray time data
       list of time fow which obs CRE is înput

    file_part : str, optional, default = '-scaled'
       selection of file part that specifies if bias correction of clearsky is used

    
    Returns
    --------
    dset_obs : xarray Dataset
       set that contains time series of observed CRE effects.

    '''


    # make a list of time objects
    # ==============================
    timeobj_lists = []
    for t in sorted( time ):
        timeobj_lists += [ pd.Timestamp( t.data ).to_pydatetime() ,]

    timeobj_lists = np.array( times )


    # read daily stacks of obs data
    # ==============================
    t1, t2 = times.min(), times.max()

    t = copy.copy( t1 )

    dt = datetime.timedelta( days = 1 )
    obsdat = []

    while t <= t2: 
    
        obsname = 'meteosat-nawdex-%s' % t.strftime('%Y%m%d')
        fname = '%s/statistics/ave_cre%s_%s.nc' % (nawdex_dir, file_part, obsname)
        obsdat += [ xr.open_dataset( fname ), ]
        
        t += dt
    
    
    # merge and prepare dataset
    # =========================
    d = xr.merge( obsdat )
    dex = d.expand_dims( 'idname', axis = -1)

    expname = 'msevi%s' % file_part
    dex['expname'] = xr.DataArray([expname, ], dims='idname')
    dex['idname'] = [expname, ]
    
    
    return dex.sel( time = time )

######################################################################
######################################################################

def get_cre4set( set_number, allowed_set_range = [1,4] ):


    '''
    Collects average CRE data for a selected set.


    Parameters
    ----------
    set_number : int
       numeric identifier of a selected experiment set.

    allowed_set_range : list, optional, default = [1, 4]
       min & max of the allow set range

    
    Returns
    --------
    dset : xarray Dataset
       set that contains time series of simulated and observed CRE effects.

    '''

    # get simulated CRE
    # ====================
    dsim = collect_sim_ave_cre4set( set_number, 
                                    allowed_set_range = allowed_set_range )

    
    # get the two observation variants
    # ========================================
    dobs_scaled = get_obs_cre4time_list( dsim.time, file_part ='-scaled')
    dobs_not_scaled = get_obs_cre4time_list( dsim.time, file_part ='-not_scaled')


    return xr.merge( [dsim, dobs_scaled, dobs_not_scaled] )

######################################################################
######################################################################

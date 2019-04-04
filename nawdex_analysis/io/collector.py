#!/usr/bin/env python

import os, sys, glob
import numpy as np

import xarray as xr
import netCDF4

from nawdex_analysis.config import nawdex_dir
from selector import  gather_simset, expname2conf_str


'''
This is a pachake that collects data for different sets.
'''


######################################################################
######################################################################

def collect_ave_cre4set( set_number, 
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
       set that contains time series of CRE effects.

    '''

    if set_number < allowed_set_range[0] or set_number > allowed_set_range[1]:
        raise ValueError('set_number is outside allowed range')
    

    # get experiment list
    # ====================
    explist = gather_simset( set_number )


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

    return dset_sim


######################################################################
######################################################################



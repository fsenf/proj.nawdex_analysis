#!/usr/bin/env python

'''
Tools for input of simulated data.
'''

import os, sys, copy
import numpy as np
import datetime
import xarray as xr

import tropy.io_tools.hdf as hio
import tropy.io_tools.netcdf as ncio
import tropy.analysis_tools.grid_and_interpolation as gi

from nawdex_analysis.config import nawdex_regions_file
from nawdex_analysis.io.tools import convert_time

######################################################################
# (1) Regridded Data for Further Analysis
######################################################################


def read_mask( region = 'full_region'):

    '''
    Read region mask.


    Parameters
    ----------
    region : str, optional, default = 'full_region'
        region keyword 


    Returns 
    --------
    dset : dict
        dataset dictionary

    '''

    # also get mask
    mfile = nawdex_regions_file
    dset = {'mask' : hio.read_var_from_hdf(mfile, region) }
    
    return dset

######################################################################
######################################################################

def read_data_field( fname, time, varname ):

    '''
    Reads "level2" data for analysis and plotting.

    Parameters
    ----------
    fname : str
        input data file name

    time : int or datetime object
        time index OR datetime object for which data is read

    varname : str
        name of the product read
    

    Returns 
    --------
    dset : dict
        dataset dictionary

    '''

    # read bt variables
    # dset = ncio.read_icon_4d_data(fname, [varname], itime = itime)
    xset = xr.open_dataset(fname)
    
    if type( time ) == type( 10 ):
        itime = time
        var = np.ma.masked_invalid( xset.isel(time = itime)[varname].data )
        
    elif type ( time ) == datetime.datetime :
        tfloat = convert_time( time ) 
        var = np.ma.masked_invalid( xset.sel(time = tfloat)[varname].data )

    dset = { varname : var }
    
    # read geo-ref
    geo = ncio.read_icon_4d_data(fname, ['lon', 'lat'], itime = None)
    dset.update( geo )

    # also get mask
    dset.update( read_mask( region = 'full_region' ) )
    
    dset['time_obj'] = ncio.read_icon_time(fname, itime = itime)
    dset['time_str'] =  dset['time_obj'].strftime('%Y-%m-%d %H:%M UTC')

    return dset

######################################################################
######################################################################

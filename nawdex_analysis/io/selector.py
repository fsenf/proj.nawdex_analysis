#!/usr/bin/env python

import os, sys
import numpy as np

import xarray as xr


from nawdex_analysis.config import nawdex_dir


'''
This is a selector tool box. Given a field name and a time object
all simulations and the observation is selected.
'''




######################################################################
######################################################################

def check_if_nc_has_varname( fname, varname ):

    '''
    Checks if netcdf file contains variable with a certain name.


    Parameters
    ----------
    fname : str
        name of file

    varname : str
        considered variable name


    Returns
    --------
    decision : bool
        decision if varname is in netcdf
    '''


    f = xr.open_dataset(fname, autoclose = True)
    decision = varname in f
    f.close()

    return decision



######################################################################
######################################################################

def check_if_nc_has_time( fname, time ):

    '''
    Checks if netcdf file contains time.


    Parameters
    ----------
    fname : str
        name of file

    time : datetime object
        time


    Returns
    --------
    decision : bool
        decision if time is in netcdf
    '''

    # convert time object into float
    tfloat = convert_time( time )

    # check file content
    f = xr.open_dataset(fname, autoclose = True)
    decision = np.any( tfloat == f.time.data )
    f.close()

    return decision

######################################################################
######################################################################


def make_filetime_index( varname, tobject ):
    
    '''
    The function generates an time index listing all filenames 
    that contain selected time and variable name.


    Parameters
    ----------
    varname : str
        considered variable name
    
    tobject : datetime object
        selected time slot


    Returns
    --------
    timefile_index : dict
        dictionary lists filenames depending on time slot
    '''

    


######################################################################
######################################################################

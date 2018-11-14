#!/usr/bin/env python

import os, sys, glob
import numpy as np

import xarray as xr
import netCDF4

from nawdex_analysis.config import nawdex_dir
from nawdex_analysis.io.tools import convert_time


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

    # this is slower
    # f = xr.open_dataset(fname, autoclose = True)
    # decision = varname in f
    # f.close()

    f = netCDF4.Dataset( fname ,'r')
    decision = varname in f.variables
    f.close()

    return decision



######################################################################
######################################################################

def check_if_nc_has_time( fname, time ):

    '''
    Checks if netcdf file contains variable name AND time.


    Parameters
    ----------
    fname : str
        name of file

    varname : str
        considered variable name

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

def check_varname_and_time_in_nc( fname, varname, time ):

    
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

    # variable decision
    var_decision = check_if_nc_has_varname( fname, varname )


    # only look at time if variable is there
    if var_decision:
        decision = check_if_nc_has_time( fname, time )
    else:
        decision = False

    return decision

######################################################################
######################################################################




def make_filetime_index( varname, tobject, 
                         filepart = '',
                         subdirs = ['meteosat', 'synsat', 'sim-toarad', 'gerb-like']):
    
    '''
    The function generates an time index listing all filenames 
    that contain selected time and variable name.


    Parameters
    ----------
    varname : str
        considered variable name
    
    tobject : datetime object
        selected time slot

    filepart : str
        a part of the filename given as substring to select
        only a subset of files

    subdirs : list of str, optional,  default = ['meteosat', 'synsat', 'sim-toarad', 'gerb-like']
        list of subdirectories where file search is done


    Returns
    --------
    timefile_index : dict
        dictionary lists filenames depending on time slot
    '''

    
    # gather full filelist
    flist = []

    for sdir in subdirs:
        flist += glob.glob('%s/%s/*%s*.nc' % (nawdex_dir, sdir, filepart))
    
    
    # over over files and generate index
    index = {}
    for fname in flist:
        fcheck = check_varname_and_time_in_nc( fname, varname, tobject )

        if fcheck:
            if not tobject in index:
                index[tobject] = []

            index[tobject] += [ fname ]


    return index

######################################################################
######################################################################

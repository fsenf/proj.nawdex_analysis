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
# (1) Check for netcdf files with same variables and times
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
    f = xr.open_dataset(fname )#, autoclose = True)
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
# (2) Define experiments sets 
######################################################################

def set_selector(set_number):
    
    '''
    Selects mis numbers based on (per-defined) experiment set.


    Parameters
    ----------
    set_number : int
        numerical ID for experiment set (1 ... 4)


    Returns
    --------
    fine_set : list
       list of mis numbers for fine resolution (<= 10 km)

    coarse_set : list
       list of mis numbers for coarse resolution (>= 20 km)
    '''

    if set_number == 1:
        fine_set = [5,6]
        coarse_set = [3,4]
        
    elif set_number == 2:
        fine_set = [1,2,3,4]
        coarse_set = [1,2]
        
    elif set_number == 3:
        fine_set = [7,8]
        coarse_set = [5,6]
        
    elif set_number == 4:
        fine_set = [9,10]
        coarse_set = [7,8]
    else:
        print 'set not defined'
            
    return fine_set, coarse_set

######################################################################
######################################################################


def set_initdate( set_number ):
        
    '''
    Selects init date based on (per-defined) experiment set.


    Parameters
    ----------
    set_number : int
        numerical ID for experiment set (1 ... 4)


    Returns
    --------
    initdate : str
        initialization date of simulation, fmt = '%Y-%m-%d'
    '''

    if set_number == 1:
        initdate = '2016-09-20'
    
    elif set_number == 2:
        initdate = '2016-09-22'
    
    elif set_number == 3:
        initdate = '2016-09-29'
    
    elif set_number == 4:
        initdate = '2016-10-04'
        
    return initdate


######################################################################
######################################################################



def gather_simset( set_number ):

    '''
    Collects a list of experiment names based on a selected set.


    Parameters
    ----------
    set_number : int
        numerical ID for experiment set (1 ... 4)


    Returns
    --------
    simset : list
        list of experiment names, e.g. ['nawdexnwp-2km-mis-0009', ... ]

    '''

    
    resolutions = ['2km', '5km', '10km', '20km', '40km', '80km']
    fine_set, coarse_set = set_selector( set_number )
    
    simset = []
    for res in resolutions:
    
        if res in ['2km', '5km', '10km']:
            mis_list = fine_set
            
        elif res in ['20km', '40km', '80km']:
            mis_list = coarse_set
        
        for mis in mis_list:
            expname = 'nawdexnwp-%s-mis-%s' % (res, str(mis).zfill(4))
        
        
            simset += [ expname, ]
            
    return simset

######################################################################
######################################################################


#!/usr/bin/env python

'''
Tools for input of simulated data.
'''

import os, sys, copy
import numpy as np
import scipy.ndimage
import datetime

import tropy.io_tools.hdf as hio
import tropy.io_tools.netcdf as ncio
import tropy.analysis_tools.grid_and_interpolation as gi

from nawdex_analysis.io.tools import lonlat2azizen


######################################################################
# (1) Variable Vectors
######################################################################


def get_grid_filename( subdir ):

    '''
    Returns the name of a NAWDEX gridfile depending on the sub directory name.
    
    
    Parameters
    -----------
    subdir : str
        name of subdirectory (which contains info about spatial resolution)


    Returns
    -------
    gridfile : str
        name of the NAWDEX grid file
    '''


    if '2km' in subdir:
        gridfile = '/work/bm0834/b380459/NAWDEX/grids/icon-grid_nawdex_78w40e23n80n_R2500m.nc'

    elif '5km' in subdir:
        gridfile = '/work/bm0834/b380459/NAWDEX/grids/icon-grid_nawdex_78w40e23n80n_R5000m.nc'

    elif '10km' in subdir:
        gridfile = '/work/bm0834/b380459/NAWDEX/grids/icon-grid_nawdex_78w40e23n80n_R10000m.nc'
        
    elif '20km' in subdir:
        gridfile = '/work/bm0834/b380459/NAWDEX/grids/icon-grid_nawdex_78w40e23n80n_R20000m.nc'
        
    elif '40km' in subdir:
        gridfile = '/work/bm0834/b380459/NAWDEX/grids/icon-grid_nawdex_78w40e23n80n_R40000m.nc'
        
    elif '80km' in subdir:
        gridfile = '/work/bm0834/b380459/NAWDEX/grids/icon-grid_nawdex_78w40e23n80n_R80000m.nc'

    return gridfile


######################################################################
######################################################################

def read_georef( expname, mask_with_zen = True, zen_max = 75. ):

    '''
    Reads geo reference of simulation.

    
    Parameters
    ----------
    expname : str
        this is the experiment name which should be equal to the subdirectory
        it is allowed to also pass the georef filename directly through this agrument

    mask_with_zen : bool, optional, default = True
        if zen mask should be applied

    zen_max : float, optional, default = 75
        maximum in satellite zenith angle (if zen_mask = True)


    Returns
    -------
    geo : dict of numpy arrays
    '''


    # get gridfile name
    if os.path.isfile( expname ):
        gridfile = expname
    else:
        gridfile = get_grid_filename( expname )


    # lon/lat input
    geo = ncio.read_icon_4d_data(gridfile, ['clon', 'clat'], itime = None)

    # calculate zenith angle
    clon, clat = geo['clon'], geo['clat']
    clon, clat = np.rad2deg( clon ), np.rad2deg( clat )

    geo['azi'], geo['zen'] = lonlat2azizen(clon, clat)
    

    # do masking with satellite zenith angle
    if mask_with_zen:
        mask = (geo['zen'] <= zen_max)

        for vname in geo.keys():
            geo[vname] = geo[vname][mask]

    return geo

######################################################################
######################################################################

def get_zen_mask(expname, geo = {}, zen_max = 75.):
    
    '''
    Calculates a satellite zenith angle mask.

    
    Parameters
    ----------
    expname : str
        this is the experiment name which should be equal to the subdirectory
        it is allowed to also pass the georef filename directly through this agrument

    geo : dict, optional, default ={}
        contains georef information if this is available in advance

    Returns
    -------
    mask : bool numpy array
        mask where satellite zenith angle condition is valid
    '''

    # get georef if needed
    if geo == {}:
        geo = read_georef( expname )
    
    
    # calculate mask
    mask = (geo['zen'] <= zen_max)
    
    
    return mask
    
######################################################################
######################################################################

#!/usr/bin/env python

'''
Tools for reprojection or regridding of data.
'''

import os, sys, copy
import numpy as np
import scipy.ndimage
import datetime

import tropy.analysis_tools.grid_and_interpolation as gi
import tropy.io_tools.netcdf as ncio

from nawdex_analysis.config import  meteosat_georef_file


######################################################################
# (1) Nearest Neighbor Interpolation
######################################################################

def get_vector2msevi_index( vgeo, msevi_georef_file = None ):

    '''
    Calculates nearest neighbor index for the conversion between 
    ICON output vectors and the Msevi grid.

    Parameters
    ----------
    vgeo : dict of numpy arrays
        set of fields containing vector geo-reference
      

    Returns
    --------
    ind : numpy array
        index for nn interpolation
    '''

    

    # read georef ----------------------------------------------------
    if msevi_georef_file is None:

        # hope that meteosat file is there
        msevi_georef_file = meteosat_georef_file
    
    msevi_georef = ncio.read_icon_4d_data( georef_file, ['lon', 'lat'], itime = None)


    # prepare the reprojection ---------------------------------------
    
    # reshape because gi - tools expects 2dim fields
    vlon = vgeo['clon'].reshape(1, -1)
    vlat = vgeo['clat'].reshape(1, -1)

    # tagret grid georef
    glon = msevi_georef['lon']
    glat = msevi_georef['lat']

    # use tool for nn interpolation
    ind = gi.create_interpolation_index(vlon, vlat, glon, glat)

    return ind[1] # go back to vector representation


######################################################################
######################################################################

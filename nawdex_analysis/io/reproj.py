#!/usr/bin/env python

'''
Tools for reprojection or regridding of data.
'''

import os, sys, copy
import numpy as np
import scipy.ndimage
import datetime
import pyproj
import warnings


import tropy.analysis_tools.grid_and_interpolation as gi

from nawdex_analysis.config import SEVIRI_cutout

######################################################################
# (1) SEVIRI projection and co-ordinate transformations
######################################################################


def msevi_ll2xy(lon, lat, hres = False, lon0 = 0):
        
        ''' 
        Returns line/column numbers in geostationary satellite
        projection
        
        Parameters
        ----------
        lon : numpy array
            longitude
        
        lat : numpy array
            latitude
            
        
        Returns
        -------
        x : numpy array
            x-coordinate in SEVIRI projection
        
        y : numpy array
            y-coordinate in SEVIRI projection

        '''
        geos_proj_param = {
                'proj':      'geos',
                'h':     35785831.0,
                'a':      6378169.0,
                'b':      6356583.8,
                'lon_0':        lon0
        }
        # 
        assert lat.shape==lon.shape
        
        # Apply MSG SEVIRI satellite projection
        msevi_proj = pyproj.Proj(**geos_proj_param)
        
        
        (x, y) = msevi_proj(lon.flatten(),lat.flatten())

        x = x.reshape(*lon.shape)
        y = y.reshape(*lat.shape)
        
        return x, y


######################################################################
######################################################################

def msevi_xy2ij(x, y, hres = False):
        
        '''
        Converts msevi xy coordinates into indices.
        
        
        Parameters
        ----------
        x : numpy array
            x-coordinate in SEVIRI projection
        
        y : numpy array
            y-coordinate in SEVIRI projection


        Returns
        -------
        irow : numpy array
             row index in SEVIRI projection
        
        icol : numpy array
            column index in SEVIRI projection

        '''
        
        # Convert to SEVIRI LRES full-disk lin/col indices
        if hres == False:
                res = 3000.40316582
                icol = x / res + 1856.0
                irow = 1856.0 - y / res
        else:
                res = 1000.1343886066667
                icol = x / res + (3*1856.0)
                irow = (3*1856.0) - y / res

        irow.shape = icol.shape = y.shape
        
        return irow, icol

######################################################################
######################################################################


def msevi_ij2xy(irow, icol, hres = False):
        
        '''
        Converts msevi indices into xy coordinates.
        
        
        Parameters
        ----------
        irow : numpy array
             row index in SEVIRI projection
        
        icol : numpy array
            column index in SEVIRI projection


        Returns
        -------
        x : numpy array
            x-coordinate in SEVIRI projection
        
        y : numpy array
            y-coordinate in SEVIRI projection

        '''
        
        # Convert to SEVIRI LRES full-disk lin/col indices
        if hres == False:
            res = 3000.40316582
            offset = 1856.0
        else:
            res = 1000.1343886066667
            offset = (3*1856.0)
            
        x = res * (icol - offset)
        y = res * (offset - irow)

        x.shape = y.shape = irow.shape
        
        return x,y


######################################################################
# (2) Nearest Neighbor Interpolation
######################################################################

def get_vector2msevi_index( vgeo ):

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

    # prepare target fields ..........................................
    
    # get shape
    (ir1, ir2), (ic1, ic2) = SEVIRI_cutout
    nrows = ir2 - ir1
    ncols = ic2 - ic1

    # index set 
    irow, icol = gi.make_index_set(nrows, ncols)

    # and projection co-ordinates
    xsevi, ysevi = msevi_ij2xy(irow, icol)
    


    # prepare input fields ...........................................
    
    # reshape because gi - tools expects 2dim fields
    vlon = vgeo['lon'].reshape(1, -1)
    vlat = vgeo['lat'].reshape(1, -1)

    xsim, ysim = msevi_ll2xy(vlon, vlat, lon0 = 0)
    

    # use tool for nn interpolation ..................................
    ind = gi.create_interpolation_index(xsim, ysim, xsevi, ysevi, xy = True)
    

    return ind[1] # go back to vector representation


######################################################################
######################################################################

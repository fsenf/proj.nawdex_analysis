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
import tropy.io_tools.hdf as hio

from nawdex_analysis.config import SEVIRI_cutout, nawdex_regions_file 

######################################################################
# (1) SEVIRI projection and co-ordinate transformations
######################################################################


def set_msevi_proj(lon0 = 0):
        
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
        msevi_proj : pyproj object
            Meteosat SEVIRI projection

        '''
        geos_proj_param = {
                'proj':      'geos',
                'h':     35785831.0,
                'a':      6378169.0,
                'b':      6356583.8,
                'lon_0':        lon0
        }
        # 
        
        # Apply MSG SEVIRI satellite projection
        msevi_proj = pyproj.Proj(**geos_proj_param)

        return msevi_proj

        
######################################################################
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
######################################################################


def msevi_ij2ll(irow, icol, lon0 = 0, hres = False):
        
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
        lon : numpy array
            longitude
        
        lat : numpy array
            latitude

        '''

        # first get projection coordinates
        x, y = msevi_ij2xy(irow, icol, hres = hres)

        
        # set up projection
        msevi_proj = set_msevi_proj(lon0 = lon0)
        lon, lat = msevi_proj(x, y, inverse = True)

        
        return lon, lat




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
    nmax = 3712

    irow_all, icol_all = gi.make_index_set( nmax, nmax )
    irow = gi.cutout_fields( irow_all, SEVIRI_cutout)
    icol = gi.cutout_fields( icol_all, SEVIRI_cutout)


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


def nn_reproj_with_index( dset, ind, apply_mask = True, Nan = 0 ):

    '''
    Reprojects data field intpo Meteosat SEVIRI projection.


    Parameters
    ----------
    dset : dict of numpy arrays
        set of fields that should be reprojected

    ind : numpy array
        interpolation index that maps the field in dset into SEVIRI grid
    
    apply_mask : bool, optional, default = True
        switch if masking with domain mask should be applied

    Nan : float
        value inserted for positions with mask == False



    Returns
    --------
    dset_inter :  dict of numpy arrays
        set of fields that have been interpolated onto SEVIRI grid
    '''


    # prepare masking
    if apply_mask:
            mask = hio.read_var_from_hdf( nawdex_regions_file, 'full_region' )
            mask = mask.astype( np.bool ) 


    # apply interpolation index
    dset_inter = {}
    
    for vname in dset.keys():
        
        # do interpolation
        v = dset[vname][ind]
        
        
        # apply masking if wanted
        if apply_mask:
            v = np.where( mask, Nan, v )
        
        dset_inter[vname] = v[:]
        
    return dset_inter


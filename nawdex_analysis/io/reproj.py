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
######################################################################

def msevi_lonlat(region = SEVIRI_cutout):

    '''
    Calcualtions MSG longitude and latitude for a certain cutout.


    Parameters
    ----------
    region : tuble of int, optional, default = SEVIRI_cutout
        cutout region defintion as ((ir1, ir2), (ic1, ic2))


    Returns
    --------
    vgeo : dict of numpy arrays
        georeference dictionary
    '''

    
    # prepare index field
    nmax = 3712

    irow_all, icol_all = gi.make_index_set( nmax, nmax )
    irow = gi.cutout_fields( irow_all, region )
    icol = gi.cutout_fields( icol_all, region )


    # and use geo-stationary projection
    lon, lat = msevi_ij2ll(irow, icol)

    vgeo = dict( lon = lon, lat = lat )

    return vgeo
    


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


def nn_reproj_with_index( dset, ind, 
                          vnames = 'all', apply_mask = True, Nan = 0 ):

    '''
    Reprojects data field intpo Meteosat SEVIRI projection.


    Parameters
    ----------
    dset : dict of numpy arrays
        set of fields that should be reprojected

    ind : numpy array
        interpolation index that maps the field in dset into SEVIRI grid

    vnames : string of list of strings, optional, default = 'all'
        list of variable names to be interpolated

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

    # prepare variable list
    if vnames == 'all':
        vlist = dset.keys()

    elif type( vnames ) == type( '' ):
        vlist = [ vnames, ]
        
    else:
        vlist = vnames
        
        

    # apply interpolation index
    dset_inter = {}
    
    for vname in vlist:
        
        # do interpolation
        v = dset[vname][ind]
        
        
        # apply masking if wanted
        if apply_mask:
            v = np.where( mask, v, Nan )
        
        dset_inter[vname] = v[:]
        
    return dset_inter

######################################################################
# (3) Box-average Interpolation and Reprojection
######################################################################



def get_reproj_param(lin, col, region, 
                 hres = False):

        '''
        Preparation of reprojection parameters.


        Parameters
        ----------
        lin : numpy array, 2dim
            line or row indices of points to be interpolated

        col : numpy array, 2dim
            column indices of points to be interpolated

        region : tuble or list of floats
            region tuble stating first and last row and first and last column
            e.g. region = ((ir1, ir2), (ic1, ic2))

        hres : bool, optional, default = False
            option for using high-resolution SEVIRI grid 

        
        Returns
        --------
        rparam : dict of numpy arrays
            reprojection parameters
        '''

        # extract region
        (ir1, ir2), (ic1, ic2) = region
        lin0 = ir1
        col0 = ic1

        nlin = ir2 - ir1
        ncol = ic2 - ic1

        # set high-res 
        # TODO: is offset right? Check against MSevi class
        if hres==True:
                lin0 = lin0*3
                col0 = col0*3
                nlin = nlin*3
                ncol = ncol*3

        # round line/column indices
        ilin = np.round(lin).astype(np.int)
        icol = np.round(col).astype(np.int)

        # Get region mask
        regmask = (ilin>=lin0)&(ilin<(lin0+nlin))&(icol>=col0)&(icol<(col0+ncol))

        # get flattened array index
        iflat = (ilin[regmask]-lin0)*ncol+(icol[regmask]-col0)

        # get ordering index
        isort = np.argsort(iflat)
        (iuniq,ifirst)=np.unique(iflat[isort],return_index=True)

        count = np.diff(np.append(ifirst,len(iflat)))

        rparam =  dict( count = count,
                        iuniq = iuniq,
                        ifirst = ifirst,
                        iflat = iflat, 
                        regmask = regmask,
                        lin0 = lin0,
                        col0 = col0,
                        nlin = nlin, 
                        ncol = ncol,
                        isort = isort)

        return rparam

######################################################################
######################################################################


def reproj_field(f, rparam, operator = np.nanmean):

    '''
    Reprojection field using reprojection parameters (and grid box avareging)
    
    
    Parameters
    ----------
    f : numpy array, 2dim
        field to be interpolated

    rparam : dict of numpy arrays
        reprojection parameters

    operator : numpy method, optional, default = np.nanmean
        operator used for calculations, e.g. averaging         


    Returns
    --------
    f_reproj
    '''

    # Mask for out-of-region pixels
    f = f[rparam['regmask']].flatten()

    # Sort by flat index
    f = f[rparam['isort']]

    # Create new field
    newf = np.empty(rparam['nlin']*rparam['ncol'])
    newf[:] = np.nan

    # # Calculate mean through cumulative sum/vectorized ##
    # cumsum = np.cumsum(f)[para['ilast']]
    # cumsum = np.append((cumsum[0],np.diff(cumsum)))
    # mean = cumsum/para['count']
    # newf[para['iuniq']]=mean
    # # Calculate mean by for-loop
    warnings.filterwarnings('ignore') ## all-nans result in Runtime warning

    for i,j,cnt in zip(rparam['iuniq'],rparam['ifirst'],rparam['count']):
        newf[i] = operator(f[j:(j+cnt)])


    f_reproj = newf.reshape((rparam['nlin'],rparam['ncol']))


    # ... and return
    return np.ma.masked_invalid( f_reproj )

######################################################################
######################################################################


def get_vector2msevi_rparam( vgeo, region = SEVIRI_cutout ):

    '''
    Calculates reprojection parameters for the conversion between 
    ICON output vectors and the Msevi grid.


    Parameters
    ----------
    vgeo : dict of numpy arrays
        set of fields containing vector geo-reference
      

    Returns
    --------
    rparam : dict of numpy arrays
        reprojection parameters
    '''

    # prepare input fields ...........................................
    vlon = vgeo['lon']
    vlat = vgeo['lat']

    xsim, ysim = msevi_ll2xy(vlon, vlat, lon0 = 0)
    lin, col = msevi_xy2ij( xsim, ysim ) 


    # calculation reprojection parameters ............................
    rparam = get_reproj_param(lin, col, region)

    return rparam


######################################################################
######################################################################

def combined_reprojection( dset, ind, rparam, 
                           vnames = 'all', apply_mask = True, Nan = 0 ):

    '''
    Combine nearest neighbor (nn) and box-average interpolation. If a grid box has no value, 
    the nn value is taken.


    Parameters
    ----------
    dset : dict of numpy arrays
        set of fields that should be reprojected

    ind : numpy array
        interpolation index that maps the field in dset into SEVIRI grid

    rparam : dict of numpy arrays
        reprojection parameters

    vnames : string of list of strings, optional, default = 'all'
        list of variable names to be interpolated

    apply_mask : bool, optional, default = True
        switch if masking with domain mask should be applied

    Nan : float
        value inserted for positions with mask == False


    Returns
    --------
    dset_inter :  dict of numpy arrays
        set of fields that have been interpolated onto SEVIRI grid
    '''

    # LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
    # (i) NN Interpolation
    # TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
    dset_nn = nn_reproj_with_index( dset, ind, 
                                    vnames = vnames, 
                                    apply_mask = apply_mask, 
                                    Nan = Nan )


    # LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
    # (ii) Box-averaging Interpolation and combination 
    # TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
    
    vlist = dset_nn.keys()

    # apply interpolation index
    dset_inter = {}
    
    for vname in vlist:
        
        # get field vector
        fvec = dset[vname]
        
        # do averaging interpolation
        fave = reproj_field( fvec, rparam )

        # get nn result and combine
        fnn = dset_nn[vname]

        # take nn where ave is not defined
        dset_inter[vname] = np.where( fave.mask, fnn, fave )
        
    return dset_inter

######################################################################
######################################################################

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
from nawdex_analysis.io.tools import  lonlat2azizen

######################################################################
# (1) SEVIRI projection and co-ordinate transformations
######################################################################


def set_msevi_proj(lon0 = 0):
        
        ''' 
        Geostationary projection object for Meteosat.


        Parameters
        ----------
        lon : numpy array
            longitude
        
        lat : numpy array
            latitude

        lon0 : float, optional, default = 0
            sub-satellite longitude

        
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


def msevi_ll2xy(lon, lat, lon0 = 0):
        
        ''' 
        Returns line/column numbers in geostationary satellite
        projection.
        

        Parameters
        ----------
        lon : numpy array
            longitude
        
        lat : numpy array
            latitude

        lon0 : float, optional, default = 0
            sub-satellite longitude

        
        
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

        hres : bool, optional, default = False
            switch if resolution coordinates have been input


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

        hres : bool, optional, default = False
            switch if resolution coordinates have been input


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

        lon0 : float, optional, default = 0
            sub-satellite longitude

        hres : bool, optional, default = False
            switch if resolution coordiante have been input


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

def msevi_lonlat(region = SEVIRI_cutout, return_azi_zen = False):

    '''
    Calcualtions MSG longitude and latitude for a certain cutout.


    Parameters
    ----------
    region : tuble of int, optional, default = SEVIRI_cutout
        cutout region defintion as ((ir1, ir2), (ic1, ic2))

    return_azi_zen : bool, optional, default = False
        switch if satellite azimuth and zenith angle is calculated and returned


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

    if return_azi_zen:
        azi, zen = lonlat2azizen(lon, lat)
        vgeo['azi'] = azi
        vgeo['zen'] = zen

    return vgeo


######################################################################
######################################################################

def slice2nwcsaf_region(region):
    
    '''
    Function that gets the NWCSAF region definition from a region slice (row1, row2), (col1, col2).
    
    
    Parameters
    ----------
    region : tuple of tuples of int
        region slice (row1, row2), (col1, col2)


    Returns
    -------
    icenter : tuple of int
        center index of the region cutout 
    
    ndims : tuple of int
        dimensions ( size ) of the region (nrows, ncols)
        
    '''
    
    
    # get sizes
    rowsize = region[0][1] - region[0][0]
    colsize = region[1][1] - region[1][0]
    
    ndims = rowsize, colsize
    
    
    # centerindex
    crow =  region[0][0] + rowsize / 2 + 1
    ccol =  region[1][0] + colsize / 2 + 1
    
    icenter = crow, ccol
    
    return icenter, ndims

######################################################################
######################################################################

def nwcsaf_region2slice(icenter, ndims):

    '''
    The region defintion of the NWCSAF (based on size and center coordinates)
    is converted to a region slice.
 

    
    Parameters
    ----------
    icenter : tuple of int
        center index of the region cutout 
    
    ndims : tuple of int
        dimensions ( size ) of the region (nrows, ncols)


    Returns
    -------
    region : tuple of tuples of int
        region slice (row1, row2), (col1, col2)

    
    '''


    crow, ccol = icenter

    crow, ccol = crow - 1, ccol - 1 # shift between 1-base and 0-base index system 
    nrows, ncols = ndims

    irow1 = crow - nrows / 2
    irow2 = irow1 + nrows

    icol1 = ccol - ncols / 2
    icol2 = icol1 + ncols


    return ((irow1, irow2), (icol1, icol2))
    


######################################################################
# (2) Nearest Neighbor Interpolation
######################################################################


def get_vector2msevi_index( vgeo, region = SEVIRI_cutout ):

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
    irow = gi.cutout_fields( irow_all, region)
    icol = gi.cutout_fields( icol_all, region)


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

def get_msevi2vector_index( vgeo, region = SEVIRI_cutout ):

    '''
    Calculates nearest neighbor index for the conversion between 
    MSevi grid and ICON output vectors. 

    Inverse transformation of `get_vector2msevi_index`.


    Parameters
    ----------
    vgeo : dict of numpy arrays
        set of fields containing vector geo-reference
      

    Returns
    --------
    ind : numpy array
        index for nn interpolation
    '''


    # get region properties
    # ======================
    (ir1, ir2), (ic1, ic2 ) = region
    
    nrows = ir2 - ir1
    ncols = ic2 - ic1
    

    # prepare input fields ...........................................
    
    # reshape because gi - tools expects 2dim fields
    vlon = vgeo['lon']
    vlat = vgeo['lat']

    
    # use projection to retrieve index set
    xsim, ysim = msevi_ll2xy(vlon, vlat, lon0 = 0)
    
    irow_full, icol_full = msevi_xy2ij( xsim, ysim )
    
    # apply offset
    irow = (np.round(irow_full) - ir1).astype(np.int)
    icol=  (np.round(icol_full) - ic1).astype(np.int)
    
    #and clip index range
    irow = np.clip(irow, 0, nrows - 1)
    icol = np.clip(icol, 0, ncols - 1)
       
    return irow, icol


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
        vlist = list(dset.keys())

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
      
    region : tuble of int, optional, default = SEVIRI_cutout
        cutout region defintion as ((ir1, ir2), (ic1, ic2))


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
                           vnames = 'all', 
                           apply_mask = True, 
                           only_apply_nn = False,
                           Nan = 0 ):

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

    only_apply_nn : bool, optional, default = False
        switch if only nearest neighbor interpolation is applied

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
    
    vlist = list(dset_nn.keys())

    # apply interpolation index
    dset_inter = {}
    
    for vname in vlist:
        
        # get field vector
        fvec = dset[vname]
        
        # get nn result and combine
        fnn = dset_nn[vname]

        # do averaging interpolation
        if not only_apply_nn:
            fave = reproj_field( fvec, rparam, operator = np.mean )
        else:
            fave = np.nan * np.ma.ones_like( fnn )
            fave = np.ma.masked_invalid( fave )


        # take nn where ave is not defined
        f_inter = np.where( fave.mask, fnn, fave )
        dset_inter[vname] = np.ma.masked_equal( f_inter, Nan )
        
        
    return dset_inter

######################################################################
######################################################################

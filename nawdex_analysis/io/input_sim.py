#!/usr/bin/env python

'''
Tools for input of simulated data.
'''

import os, sys, copy
import numpy as np
import scipy.ndimage
import datetime
import xarray as xr
import pandas as pd

import tropy.io_tools.hdf as hio
import tropy.io_tools.netcdf as ncio
import tropy.analysis_tools.grid_and_interpolation as gi

from nawdex_analysis.io.tools import lonlat2azizen
import nawdex_analysis.io.reproj


######################################################################
# (1) Variable Vectors
######################################################################

def subdir_from_fname( fname , npos = -1):

    '''
    Gets the sub-directory name from filename.
    
    Parameters
    ----------
    fname : str
        filename

    npos : int, optional, default = -1
        position where sub-directory is located in full path
    
    
    Returns
    --------
    subdir : str
        sub-directory name
    
    '''

    
    
    dirname = os.path.dirname( fname )

    subdir = dirname.split('/')[-1]

    return subdir 

######################################################################
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
        maximum in satellite zenith angle (if mask_with_zen = True)


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

    geo['lon'], geo['lat'] = clon, clat
    geo['azi'], geo['zen'] = lonlat2azizen(clon, clat)
    

    # do masking with satellite zenith angle
    if mask_with_zen:
        mask = (geo['zen'] <= zen_max)

        for vname in geo.keys():
            geo[vname] = geo[vname][mask]

    return geo

######################################################################
######################################################################

def get_zen_mask(expname, geo = {}, mask_with_zen = False, zen_max = 75.):
    
    '''
    Calculates a satellite zenith angle mask.

    
    Parameters
    ----------
    expname : str
        this is the experiment name which should be equal to the subdirectory
        it is allowed to also pass the georef filename directly through this agrument

    geo : dict, optional, default ={}
        contains georef information if this is available in advance

    mask_with_zen : bool, optional, default = True
        if zen mask should be applied


    Returns
    -------
    mask : bool numpy array
        mask where satellite zenith angle condition is valid
    '''

    # get georef if needed
    if geo == {}:
        geo = read_georef( expname, mask_with_zen = mask_with_zen, zen_max = zen_max )
    
    
    # calculate mask
    mask = (geo['zen'] <= zen_max)
    
    
    return mask
    
######################################################################
######################################################################

def read_synsat_vector( fname, bt_generation_mode = 'mcfarq_rescale_noccthresh' ):
    
    '''
    Input of Synsat BT vector (given at original ICON grid).


    Parameters
    ----------
    fname : str
        name of synsat file (should be hdf5 file generated by Synsat forward operator)

    bt_generation_mode : str, optional, default =  'mcfarq_rescale_noccthresh'
        mode used for Synsat generation (several options for Synsat are possible)


    Returns
    -------
    outset : dict of numpy arrays
        set of synsat and georef vectors
    '''


    # read brightness temperatures
    # =============================
    dset = hio.read_dict_from_hdf(fname)
    bts = dset[ bt_generation_mode ]


    # Scaling: BTs are saved as 100th of a Kelvin.
    # ========================================
    outset = {}
    for k in bts:
        btname = 'bt%s' % k[3:]
        outset[btname]  = bts[k].squeeze() / 100.
        
        
    # read georeference
    # ==================
    subdir =  subdir_from_fname( fname )
    geo = read_georef( subdir )
    
    outset.update( geo )


    return outset

######################################################################
######################################################################

def read_iconvar_vector( fname, vlist ):
    
    '''
    Input of ICON variable vector (given at original ICON grid and with applied 
    zenith angle mask).


    Parameters
    ----------
    fname : str
        name of ICON file (should be netcdf file)

    vname : list of str
        list of variable names


    Returns
    -------
    outset : dict of numpy arrays
        set of synsat and georef vectors
    '''

    
    # check if vlist is list
    # ====================
    if not type(vlist) == type([]):
        vlist = [vlist,]


    # read brightness temperatures
    # =============================
    dset = ncio.read_icon_4d_data(fname, vlist, itime = None)


       
    # read georeference
    # ==================
    subdir =  subdir_from_fname( fname )
    geo = read_georef( subdir, mask_with_zen = False )
    

    # get zenith angle mask
    # =====================
    mask =  get_zen_mask( subdir, geo = geo )


    # prepare dict output
    # ====================
    outset = dset.copy()
    outset.update( geo )
    
    for vname in outset.keys():
        outset[vname] = outset[vname].squeeze()[mask]


    return outset

######################################################################
######################################################################

def read_icon_rad_vector( fname, map_varnames = True, use_clear = False ):
    
    '''
    Reads ICON TOA radiation vector.


    Parameters
    ----------
    fname : str
        name of ICON file (should be netcdf file)

    map_varnames : bool, optional, default = True
        switch if original variable names are mapped to generic names

    use_clear :  bool, optional, default = False
        switch if clearsky or cloudy values are used


    Returns
    -------
    radset : dict of numpy arrays
        set of synsat and georef vectors
    '''


    if not use_clear:
        vlist =  ['sod_t', 'sou_t', 'thb_t']       
    else:
        vlist = ['swtoaclr', 'lwtoaclr']
    
    input_set = read_iconvar_vector(fname, vlist)


    # select input fields
    radset = {}
    if map_varnames:

        if not use_clear:
            swf_up   = input_set['sou_t']
            swf_down = input_set['sod_t']
        
            radset['swf_net'] = swf_up  -  swf_down
            radset['lwf'] = input_set['thb_t']
        else:
            radset['swf_net'] = input_set['swtoaclr']
            radset['lwf']     = input_set['lwtoaclr']

        radset['lon'] = input_set['lon']
        radset['lat'] = input_set['lat']

    else:
        radset = input_set

    

    return radset

######################################################################
######################################################################


def read_radiation_flux_flist( flist, 
                               use_clear = False,
                               interpolation2msevi = True ):
    
    '''
    Reads ICON TOA radiation vectors from filelist as time stack.


    Parameters
    ----------
    flist : list of str
        filename  list of ICON file (should be netcdf file)

    interpolation2msevi : bool, optional, default = True
        switch if output should be interpolated to MSG grid

    use_clear :  bool, optional, default = False
        switch if clearsky or cloudy values are used


    Returns
    -------
    radset : dict of numpy arrays
        set of synsat and georef vectors
    '''

  
    
    # init data set
    radset = dict( time = [] )


    # loop over file list
    flist = sorted( flist )
    for ifile, fname in enumerate( flist ):
        
        # input radiation vector
        vnames = ['lwf', 'swf_net']
        din = read_icon_rad_vector(fname, use_clear = use_clear)

        # do intrepolation to MSG grid
        if interpolation2msevi:

            # get reprojection parameters
            if ifile == 0:
                ind = nawdex_analysis.io.reproj.get_vector2msevi_index( din )
                rparam = nawdex_analysis.io.reproj. get_vector2msevi_rparam( din )


            # interpolate partial dataset
            dpart = {}
            for k in vnames:
                dpart[k] = din[k]

            dset_inter = nawdex_analysis.io.reproj.combined_reprojection( dpart, ind, rparam )
            

            # get also new georef
            geo = nawdex_analysis.io.reproj.msevi_lonlat()
            dset_inter.update( geo )

            # and rewrite final dataset
            dset = dset_inter


        else:
            dset = din
            

        # stack the data
        for k in vnames:
            if not k in radset:
                radset[k] = []

            radset[k] += [  np.ma.expand_dims(dset[k], axis = 0), ]

    
        # input time and convert to datetime object
        # (a bit complicated using xarray and pandas...)
        xset = xr.open_dataset(fname)
        time =  pd.to_datetime(  xset['time'].data[0] ).to_pydatetime()
        radset['time'] += [time,]
        xset.close()

    # add georef
    radset['lon'] = dset['lon']
    radset['lat'] = dset['lat']



    # stack data along time axis
    vnames += ['time',]
    for k in vnames:
        radset[k] = np.row_stack( radset[k] )

    radset['time'] = radset['time'].squeeze()


    return radset

######################################################################
######################################################################

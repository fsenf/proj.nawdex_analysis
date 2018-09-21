#!/usr/bin/env python

'''
Tools for input of observation data.
'''

import os, sys
import numpy as np
import scipy.ndimage
import datetime

import tropy.io_tools.hdf as hio
import tropy.analysis_tools.grid_and_interpolation as gi

from nawdex_analysis.config import SEVIRI_cutout


######################################################################
######################################################################

def scale_radiation( rad_flux, factor = 0.25, Nan = -32767, n_repeat = 3):

    '''
    The small helper function scales observed radiation data.
    
    
    Parameters
    ----------
    rad_flux : numpy array, 2dim
        radiation flux
    
    factor : float, optional, default = 0.25
        scale factor
    
    Nan : int or float, optional, default = -32767
        value which is set to "not a number"
        
    n_repeat : int, optional, default = 3
        field is repeated along each axis "n_repeat" times
        
        
    Returns
    -------
    rad_scaled : numpy array, 2dim
        scaled and repeated radiation flux
    '''

    # scaling
    rad_scaled = factor * np.ma.masked_equal( rad_flux, Nan )

    # repeating
    rad_repeated = rad_scaled.repeat(n_repeat, axis = 0).repeat(n_repeat, axis = 1)
    
    # smoothing
    rad_smoothed = scipy.ndimage.uniform_filter(rad_repeated.data, n_repeat)
    
    rad_scaled = np.ma.masked_where( rad_repeated.mask, rad_smoothed)
    
    return rad_scaled

######################################################################
######################################################################


def read_radiation_fluxes(t, 
                          fdir = '/vols/talos/home/fabian/data/gerb-like/',
                          do_cutout = True):
    
    '''
    Reads and scales radiation flux data based on GERB-like SEVIRI retrievals.
    
    
    Parameters
    ----------
    t : datetime object
        a time slot
        
    fdir : str, optional, default =  '/vols/talos/home/fabian/data/gerb-like/'
        file directory name

    do_cutout : bool, optional, default = True
        if SEVIRI cutout is applied
        
        
    Returns
    -------
    lwf : numpy array, 2dim
        long-wave radiation flux
        
    swf_net : numpy array, 2dim
        net short-wave radiation flux
    '''
    
    # get time string
    time_string = t.strftime('%Y%m%d_%H%M')
    
    # input data from hdf files
    fname = '%s/GL_SEV3_L20_HR_SOL_TH_%s00_ED01.hdf' % (fdir, time_string)

    
    lwflux_up = hio.read_var_from_hdf(fname, 'Thermal Flux', subpath='Radiometry').astype(np.int16)
    sfflux_up = hio.read_var_from_hdf(fname, 'Solar Flux', subpath='Radiometry').astype(np.int16)
    sfflux_down = hio.read_var_from_hdf(fname, 'Incoming Solar Flux', subpath='Angles').astype(np.int16)
    
    # do the scaling
    lwf = scale_radiation( lwflux_up )
    swf_down = scale_radiation( sfflux_down )
    swf_up = scale_radiation( sfflux_up )
    swf_net = swf_up  -  swf_down

    if do_cutout:
        return gi.cutout_fields([lwf, swf_net], SEVIRI_cutout)
    else:
        return lwf, swf_net

######################################################################
######################################################################

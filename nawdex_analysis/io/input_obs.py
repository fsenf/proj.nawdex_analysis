#!/usr/bin/env python

'''
Tools for input of observation data.
'''

import os, sys, copy
import numpy as np
import scipy.ndimage
import datetime

import tropy.io_tools.hdf as hio
import tropy.io_tools.netcdf as ncio
import tropy.analysis_tools.grid_and_interpolation as gi

# optional import of MSevi containers (for TROPOS)
try:
    from tropy.l15_msevi.msevi import MSevi
except:
    pass

from nawdex_analysis.config import SEVIRI_cutout, NWCSAF_region
from nawdex_analysis.config import meteosat_georef_file, gerb_like_dir

from nawdex_analysis.io.tools import lonlat2azizen

######################################################################
# (1) SEVIRI BTs
######################################################################


def msevi_setting(t):

    sett = {}
    sett['time'] = t
    sett['region'] =   SEVIRI_cutout
    sett['nwcsaf_region'] =  NWCSAF_region
    sett['scan_type'] = 'pzs'


    return sett

######################################################################
######################################################################


def read_msevi(t1, t2, dt = 60., zen_max = 75.):

    
    # read msevi georef ----------------------------------------------
    sett = msevi_setting(t1)

    s = MSevi(**sett)
    s.lonlat()

    slon = np.ma.masked_invalid(s.lon)
    slat = np.ma.masked_invalid(s.lat)
    nrow, ncol = slon.shape

    azi, zen = lonlat2azizen(slon, slat)
    zen = np.ma.masked_invalid(zen)    
    zenmask = zen > 75.


    d = dict(lon = slon, lat = slat, zen = zen)
    # ================================================================

    
    # time length ----------------------------------------------------
    d['time'] = []
    ntime = 0
    t = copy.copy(t1)
    dt = datetime.timedelta(minutes = dt)
    while t <= t2:
        d['time'].append( t )
        ntime += 1
        t += dt
    # ================================================================

    # init chan arrays -----------------------------------------------
    chanlist =  [  'IR_039', 'WV_062', 'WV_073', 'IR_087', 
                   'IR_097', 'IR_108', 'IR_120', 'IR_134' ]
    for chan in chanlist:
        d[chan] = np.ma.zeros( (ntime, nrow, ncol) )

    # ================================================================



    # msevi channels -------------------------------------------------
    t = copy.copy(t1)
    n = 0
    while t <= t2:
        sett = msevi_setting(t)
        s = MSevi(**sett)
        s.load(chanlist)
        s.rad2bt()

        for chan in chanlist:
            v = s.bt[chan]
            vm = np.ma.masked_where(zenmask, v)

            d[chan][n] = vm

        

        t += dt
        n += 1

    # ================================================================

    d['msevi_region'] = sett['region']
    d['nwcsaf_region'] = sett['nwcsaf_region']

    return d


######################################################################
# (2) TOA Radiation Fluxes
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
    rad_scaled.data[rad_scaled.mask] = 0

    # repeating
    rad_repeated = rad_scaled.repeat(n_repeat, axis = 0).repeat(n_repeat, axis = 1)
    
    # smoothing
    rad_smoothed = scipy.ndimage.uniform_filter(rad_repeated.data, n_repeat)
    
    rad_scaled = np.ma.masked_where( rad_repeated.mask, rad_smoothed )
    
    return rad_scaled

######################################################################
######################################################################


def read_radiation_fluxes(t, 
                          fdir = gerb_like_dir,
                          do_cutout = True):
    
    '''
    Reads and scales radiation flux data based on GERB-like SEVIRI retrievals.
    
    
    Parameters
    ----------
    t : datetime object
        a time slot
        
    fdir : str, optional, default =  gerb_like_dir
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

def read_solar_flux(t, 
                    fluxtype = 'incoming', 
                    fdir = gerb_like_dir,
                    do_cutout = True):
    
    '''
    Reads and scales incoming solar radiation flux data based on GERB-like SEVIRI retrievals.
    
    
    Parameters
    ----------
    t : datetime object
        a time slot

    fluxtype : str, optional, default = 'incoming',
        specify the type of solar flux ('incoming' or 'downwelling' vs. 'upwelling')       
        
    fdir : str, optional, default =  gerb_like_dir
        file directory name

    do_cutout : bool, optional, default = True
        if SEVIRI cutout is applied
        
        
    Returns
    -------
    swf : numpy array, 2dim
        up- or downwelling short-wave radiation flux
    '''
    
    # get time string
    time_string = t.strftime('%Y%m%d_%H%M')
    
    # input data from hdf files
    fname = '%s/GL_SEV3_L20_HR_SOL_TH_%s00_ED01.hdf' % (fdir, time_string)

    if fluxtype in ['incoming', 'downwelling']:
        sfflux = hio.read_var_from_hdf(fname, 'Incoming Solar Flux', subpath='Angles').astype(np.int16)
    elif fluxtype == 'upwelling':
        sfflux = hio.read_var_from_hdf(fname, 'Solar Flux', subpath='Radiometry').astype(np.int16)

    
    # do the scaling
    swf = scale_radiation( sfflux )

    if do_cutout:
        return gi.cutout_fields(swf, SEVIRI_cutout)
    else:
        return swf

######################################################################
######################################################################

def read_cc_from_fluxdata(t, 
                          fdir = gerb_like_dir,
                          do_cutout = True):
    
    '''
    Reads and scales cloud cover based on GERB-like SEVIRI retrievals.
    
    
    Parameters
    ----------
    t : datetime object
        a time slot
        
    fdir : str, optional, default =  gerb_like_dir
        file directory name

    do_cutout : bool, optional, default = True
        if SEVIRI cutout is applied
        
        
    Returns
    -------
    cc_scaled : numpy array, 2dim
        cloud cover field
    '''
    
    # get time string
    time_string = t.strftime('%Y%m%d_%H%M')
    
    # input data from hdf files
    fname = '%s/GL_SEV3_L20_HR_SOL_TH_%s00_ED01.hdf' % (fdir, time_string)


    cc = hio.read_var_from_hdf(fname, 'Cloud Cover', subpath='Scene Identification').astype(np.int16)
    
    # do the scaling
    cc_scaled = scale_radiation( cc, factor = 0.01 )

    if do_cutout:
        return gi.cutout_fields(cc_scaled, SEVIRI_cutout)
    else:
        return cc_scaled


######################################################################
######################################################################

def read_radiation_flux_tstack(date, 
                               fdir = gerb_like_dir,
                               georef_file = None,
                               ntimes = 24,
                               do_cutout = True):
    
    '''
    Reads and scales radiation flux data based on GERB-like SEVIRI retrievals.
    
    
    Parameters
    ----------
    date : string
        date string as %Y%m%d
        
    fdir : str, optional, default =  gerb_like_dir
        file directory name

    georef_file : str, optional, default = None
        filename where lon and lat can be found

    ntimes : int, optional, default = 24
        number of time step included (starting at mid-night)

    do_cutout : bool, optional, default = True
        if SEVIRI cutout is applied
        
        
    Returns
    -------
    dset : dict of numpy arrays, 3dim
        set of fields incl. long- and short-wave radiaton
        
    '''

    # set time ranges
    t1 = datetime.datetime.strptime( date, '%Y%m%d')
    t2 = t1 + datetime.timedelta( hours = ntimes - 1 )

    dt = datetime.timedelta( hours = 1 )


     # stack data in time loop
    dset = dict( time = [] )
    t = copy.copy(t1)
    n = 0
    while t <= t2:
        
        lwf, swf_net = read_radiation_fluxes(t, 
                                             fdir = fdir, 
                                             do_cutout = do_cutout)

        # initialize -------------------------------------------------
        if n == 0:
            
            nrows, ncols = lwf.shape

            lwf_stack = np.ma.zeros( (ntimes, nrows, ncols) )
            swf_net_stack = np.ma.zeros( (ntimes, nrows, ncols) )
        # ============================================================

        lwf_stack[n] = lwf[:]
        swf_net_stack[n] = swf_net[:]

        dset['time'] += [ copy.copy( t ) ]

        t += dt
        n += 1

    dset['lwf'] = lwf_stack
    dset['swf_net'] = swf_net_stack
    # ================================================================


    # read georef ----------------------------------------------------
    if georef_file is None:

        # hope that meteosat file is there
        georef_file = meteosat_georef_file
    
    georef = ncio.read_icon_4d_data( georef_file, ['lon', 'lat'], itime = None)

    dset.update( georef )
    # ================================================================

    return dset

######################################################################
######################################################################

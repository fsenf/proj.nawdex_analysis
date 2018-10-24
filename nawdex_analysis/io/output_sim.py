#!/usr/bin/env python

######################################################################
'''
This is a collection of output scripts to rewrite 
observational data.

Esp. for
* Meteosat BTs
* Meteosat-based "GERB-like" radiation fluxes
'''
######################################################################


import os, sys, glob, copy
import numpy as np
import xarray as xr
import datetime

import tropy.analysis_tools.grid_and_interpolation as gi
from tropy.standard_config import local_data_path

from nawdex_analysis.io.tools import convert_time
from nawdex_analysis.io.input_sim import read_radiation_flux_flist


######################################################################
# (1) SEVIRI BTs
######################################################################

######################################################################
# (2) TOA radiation fluxes
######################################################################


def save_radflux_flist( flist, outname, 
                        use_clear = False,
                        interpolation2msevi = True ):    

    '''
    Saves full time stack of simulated TOA radiation flux data to netcdf file.

    
    Parameters
    ----------
    flist : list of str
        filename  list of ICON file (should be netcdf file)

    outname : str
        output file name, if None a local dir on altair is chosen

    interpolation2msevi : bool, optional, default = True
        switch if output should be interpolated to MSG grid

    use_clear :  bool, optional, default = False
        switch if clearsky or cloudy values are used


    Returns
    -------
    None
    '''


    # input of radiation data
    dout = read_radiation_flux_flist( flist, 
                                      use_clear = use_clear,
                                      interpolation2msevi = interpolation2msevi )


    # output 
    save_rad2nc( outname, dout )

    return

######################################################################
######################################################################


def save_rad2nc( outname, dset, fill_val = 0, use_clear = False ):

    '''
    Saves Radiaiton fluxes to netcdf.


    Parameters
    ----------
    dset : dict of numpy arrays
        TOA radiation flux dataset to be saved into netcdf
        dataset incl. lon, lat, time, and lwf, swf_net

    outname : str
        output filename

    fill_val : float or int, optional, default = 0
        fill value to be replace by NaNs

    use_clear :  bool, optional, default = False
        switch if clearsky or cloudy values are used


    Returns
    --------
    None
    '''

    # Replacing NaN with FillValue
    rad = {}

    for vname in dset.keys():
        if  vname in ['lwf', 'swf_net']:
        
            # interpolation
            v = dset[vname]
        
            # masking
            rad[vname] = np.where(v.mask, fill_val, v) 


    # ### Time Variables
    tvec = []
    for t in dset['time']:
        time = convert_time( t )
        tvec.append( time )
    tvec = np.array( tvec )

    # ### Lon-Lat Variables as Columns
    lon = dset['lon']
    lat = dset['lat']


    if use_clear:
        clear_attrib = 'clearsky'
    else:
        clear_attrib = ''

    # ### Dataset Attributes

    # Global attributes for the data set
    att_glob = {'author': 'Fabian Senf (senf@tropos.de)', 
                'institution': 'Leibniz Institute for Tropospheric Research',
                'title': 'TOA %s Radiation Fluxes' % clear_attrib,
                'description': 'instantaneous %s TOA radiation fluxes simulated with ICON' % clear_attrib}


    # Attributes for the single variables
    att_time = {'units': 'day as %Y%m%d.%f',
                'long_name': 'Time',
                'calendar': 'proleptic_gregorian'}

    att_lon = dict( long_name = "longitude" , units = "degrees_east"  )
    att_lat = dict( long_name = "latitude" , units = "degrees_north" ) 

           
    att_rad = dict( units = 'W m**(-2)')



    outset = {}
    encoding = {}

    # LONG-WAVE ------------------------------------------------------
    vname = 'lwf'
    long_name = 'TOA %s long-wave radiation flux' % clear_attrib
    
    atts = copy.copy( att_rad ) 
    atts['long_name'] = copy.copy( long_name )
    outset[vname] = (['time', 'rows', 'cols'], rad[vname], atts)
    encoding[vname] = {'zlib': True, 
                       '_FillValue': fill_val,
                       'dtype': 'int16', 
                       'scale_factor': 0.25}

    # SHORT-WAVE ------------------------------------------------------
    vname = 'swf_net'
    long_name = 'TOA %s short-wave net radiation flux' % clear_attrib
    
    atts = copy.copy( att_rad ) 
    atts['long_name'] = copy.copy( long_name )
    outset[vname] = (['time', 'rows', 'cols'], rad[vname], atts)
    encoding[vname] = {'zlib': True, 
                       '_FillValue': fill_val,
                       'dtype': 'int16', 
                       'scale_factor': 0.25}



   # Create the data set
    ds_out = xr.Dataset(outset,
                        coords = {'time': ('time', tvec, att_time),
                                  'lon': (['rows', 'cols'], lon, att_lon),
                                  'lat': (['rows', 'cols'], lat, att_lat), 
                                  },
                        attrs = att_glob)




    print '... write output to', outname
    ds_out.to_netcdf(outname, encoding = encoding)

    return 

######################################################################
######################################################################

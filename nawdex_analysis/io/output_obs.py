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
from nawdex_analysis.io.input_obs import read_msevi, read_radiation_flux_tstack



######################################################################
# (1) SEVIRI BTs
######################################################################


def save_meteosat_tstack( date, outname = None ):    

    '''
    Saves full time stack of daily Meteosat BT data to netcdf file
    for nawdex region.

    
    Parameters
    ----------
    date : str
        date string as %Y%m%d

    outname : str, optional, default = None
        output file name, if None a local dir on altair is chosen


    Returns
    -------
    None
    '''

    t = datetime.datetime.strptime( date, '%Y%m%d')
    t2 = t + datetime.timedelta( hours = 23 )


    d = read_msevi(t, t2)
   
    if outname is None:
        outname = '%s/icon/nawdex/meteosat/msevi-nawdex-%s.nc' % (local_data_path,
                                                            date)
    save_meteosat_bt2nc( outname, d)

    return

######################################################################
######################################################################


def save_meteosat_bt2nc( outname, dset, fill_val = 0 ):

    '''
    Saves Meteosat BTs to netcdf.


    Parameters
    ----------
    dset : dict of numpy arrays
        BT dataset to be saved into netcdf
        dataset incl. lon, lat, time, and BTs

    outname : str
        output filename

    fill_val : float or int, optional, default = 0
        fill value to be replace by NaNs


    Returns
    --------
    None
    '''

    # Replacing NaN with FillValue
    bts = {}

    for var_name in dset.keys():

        if 'IR' in var_name or 'WV' in var_name:
            vname = 'bt%s' % var_name[3:]
        else:
            vname = var_name


        if 'bt' in vname:
        
            # interpolation
            v = dset[var_name]
        
            # masking
            bts[vname] = np.where(v.mask, fill_val, v) 


    # ### Time Variables
    tvec = []
    for t in dset['time']:
        time = convert_time( t )
        tvec.append( time )
    tvec = np.array( tvec )

    # ### Lon-Lat Variables as Columns
    lon = dset['lon']
    lat = dset['lat']



    # ### Dataset Attributes

    # Global attributes for the data set
    att_glob = {'author': 'Fabian Senf (senf@tropos.de)', 
                'institution': 'Leibniz Institute for Tropospheric Research',
                'title': 'Meteosat-SEVIRI Brightness Temperatures',
                'description': 'Infrared Meteosat-SEVIRI images from the Prime Service' }


    # Attributes for the single variables
    att_time = {'units': 'day as %Y%m%d.%f',
                'long_name': 'Time',
                'calendar': 'proleptic_gregorian'}

    att_lon = dict( long_name = "longitude" , units = "degrees_east"  )
    att_lat = dict( long_name = "latitude" , units = "degrees_north" ) 
    att_zen = dict( long_name = "satellite_zenith_angle" , 
                    units = "degrees",
                    lon0 = 0.) 

           
    att_BT = dict( units = 'K')



    outset = {}
    encoding = {}
    for vname in bts.keys():
        nu = np.float(vname[2:]) / 10.
        long_name = 'MSG SEVIRI Brightness Temperatures at %.1f um' % copy.copy( nu )
    
        atts = copy.copy( att_BT ) 
        atts['long_name'] = copy.copy( long_name )
        outset[vname] = (['time', 'rows', 'cols'], bts[vname], atts)
        encoding[vname] = {'zlib': True, 
                            '_FillValue': fill_val,
                            'dtype': 'int16', 
                            'scale_factor': 0.01}


    # if set has satellite zenith angle included
    if dset.has_key( 'zen' ):
        outset['zen'] = (['rows', 'cols'], dset['zen'], att_zen)


    # include region defintions

    reg = np.array( dset['msevi_region'] )

    att_reg = dict( long_name = 'msg_seviri_region_cutout',
                    description = '((row1, row2), (col1, col2))' )


    outset['msevi_region'] = (['ndim', 'ndim'], reg, att_reg)

    nreg = np.array( dset['nwcsaf_region'] )

    att_nreg = dict( long_name = 'nwcsaf_region_cutout',
                    description = '((row_center, col_center), (nrows, ncols))' )


    outset['nwcsaf_region'] = (['ndim', 'ndim'], nreg, att_nreg)

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
# (2) TOA radiation fluxes
######################################################################


def save_radflux_tstack( date, 
                         indir = '/vols/talos/home/fabian/data/gerb-like/',
                         outname = None ):    

    '''
    Saves full time stack of daily TOA radiation flux data to netcdf file
    for nawdex region.

    
    Parameters
    ----------
    date : str
        date string as %Y%m%d

    outname : str, optional, default = None
        output file name, if None a local dir on altair is chosen


    Returns
    -------
    None
    '''

    t = datetime.datetime.strptime( date, '%Y%m%d')
    t2 = t + datetime.timedelta( hours = 23 )


    d = read_radiation_flux_tstack(date, 
                                   fdir = indir,
                                   ntimes = 24,
                                   do_cutout = True)

   
    if outname is None:
        outname = '%s/icon/nawdex/gerb-like/toa_radflux-nawdex-%s.nc' % (local_data_path,
                                                            date)
    save_rad2nc( outname, d)

    return

######################################################################
######################################################################


def save_rad2nc( outname, dset, fill_val = 0 ):

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



    # ### Dataset Attributes

    # Global attributes for the data set
    att_glob = {'author': 'Fabian Senf (senf@tropos.de)', 
                'institution': 'Leibniz Institute for Tropospheric Research',
                'title': 'TOA Radiation Fluxes',
                'description': 'GERB-like TOA radiation flux derived from Meteosat SEVIRI and obtained from Nicolas Clerbaux' }


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
    long_name = 'TOA long-wave radiation flux'
    
    atts = copy.copy( att_rad ) 
    atts['long_name'] = copy.copy( long_name )
    outset[vname] = (['time', 'rows', 'cols'], rad[vname], atts)
    encoding[vname] = {'zlib': True, 
                       '_FillValue': fill_val,
                       'dtype': 'int16', 
                       'scale_factor': 0.25}

    # SHORT-WAVE ------------------------------------------------------
    vname = 'swf_net'
    long_name = 'TOA short-wave net radiation flux'
    
    atts = copy.copy( att_rad ) 
    atts['long_name'] = copy.copy( long_name )
    outset[vname] = (['time', 'rows', 'cols'], rad[vname], atts)
    encoding[vname] = {'zlib': True, 
                       '_FillValue': fill_val,
                       'dtype': 'int16', 
                       'scale_factor': 0.25}

    # SHORT-WAVE ------------------------------------------------------
    vname = 'swf_up'
    long_name = 'TOA short-wave upwelling radiation flux'
    
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

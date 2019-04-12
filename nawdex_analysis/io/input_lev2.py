#!/usr/bin/env python

'''
Tools for input of simulated data.
'''

import os, sys, copy
import numpy as np
import datetime
import xarray as xr
import scipy.ndimage

import tropy.io_tools.hdf as hio
import tropy.io_tools.netcdf as ncio
import tropy.analysis_tools.grid_and_interpolation as gi

from nawdex_analysis.config import nawdex_dir
from nawdex_analysis.config import nawdex_regions_file
from nawdex_analysis.io.tools import convert_time
import nawdex_analysis.io.selector

######################################################################
# (1) Regridded Data for Further Analysis
######################################################################


def read_mask( region = 'full_region'):

    '''
    Read region mask.


    Parameters
    ----------
    region : str, optional, default = 'full_region'
        region keyword 


    Returns 
    --------
    dset : dict
        dataset dictionary

    '''

    # also get mask
    mfile = nawdex_regions_file
    dset = {'mask' : hio.read_var_from_hdf(mfile, region) }
    
    return dset

######################################################################
######################################################################

def read_data_field( fname, time, varname, region = 'full_region' ):

    '''
    Reads "level2" data for analysis and plotting.


    Parameters
    ----------
    fname : str
        input data file name

    time : int or datetime object
        time index OR datetime object for which data is read

    varname : str
        name of the product read
 
    region : str, optional, default = 'full_region'
        region for which mask is input


    Returns 
    --------
    dset : dict
        dataset dictionary

    '''

    # read bt variables
    # dset = ncio.read_icon_4d_data(fname, [varname], itime = itime)
    xset = xr.open_dataset(fname)
    
    # time is given as index
    if type( time ) == type( 10 ):
        itime = time
        var = np.ma.masked_invalid( xset.isel(time = itime)[varname].data )
        time_obj = ncio.read_icon_time(fname, itime = itime)
        
    # time is given as datetime object
    elif type ( time ) == datetime.datetime :
        tfloat = convert_time( time ) 
        var = np.ma.masked_invalid( xset.sel(time = tfloat, method = 'nearest')[varname].data )
        time_obj = time
        
    dset = { varname : var }
    
    # read geo-ref
    geo = ncio.read_icon_4d_data(fname, ['lon', 'lat'], itime = None)
    dset.update( geo )

    # also get mask
    dset.update( read_mask( region = region ) )
    
    dset['time_obj'] = time_obj
    dset['time_str'] =  dset['time_obj'].strftime('%Y-%m-%d %H:%M UTC')

    return dset

######################################################################
# (2) Specifically tailored Input for CRE analysis
######################################################################



def radname2ctname( radname, datatype = 'obs' ):
    
    '''
    Name converter: Converts the standard filename of TOA allsky files to 
    corresponding cloud type files.


    Parameters
    ----------
    radname : str
       name of toa allsky radiation file

    datatype : str, optional, default = 'obs'
       select conversion either for obs OR sim files 


    Returns
    --------
    ctname : str
       cloud type filename
    '''
    
    if datatype == 'obs':
        ctname = radname.replace('gerb-like', 'meteosat')
        ctname = ctname.replace('toa_radflux', 'nwcsaf_msevi')
    elif datatype == 'sim':
        ctname = radname.replace('sim-toarad', 'synsat')
        ctname = ctname.replace('toa_radflux', 'nwcsaf_synsat')

    return ctname

######################################################################
######################################################################


def collect_data4cre_obs( radname, itime, filepart = '-scaled', lwf_clear_offset = -2. ):
    
    '''
    Collects a set of observed data fields for cloud-radiative effect analysis.  
    
    Parameters
    ----------
    radname : str
       name of toa allsky radiation file

    itime : int
       time index of data fields ('swf_net' and 'lwf') in radname
    
    filepart : str, optional, default = '-scaled'
       part in the file that gives information about scaling of clear-sky fields
       either '-scaled' or '-not_scaled'

    lwf_clear_offset : float, optional, default = 2.
       due to the bias in the simulated LWF, we might use an predefined offset
       to correct this issue
       i.e. LWF_clear_simulated += lwf_clear_offset

    Returns
    --------
    dset : dict
       dataset dict containing swf, lwf and ct fields
    '''

    # set filenames
    # ==============
    clearname = radname.replace('toa_', 'toa_clear_')
    ctname = radname2ctname( radname, datatype = 'obs' )


    # read allsky data
    # =================
    dset = {}
    for vname in ['lwf', 'swf_net']:
        radset = read_data_field(radname, itime, vname, region='atlantic')
        dset[vname] = radset[vname]
        
        
        
    
    # find the right short-wave clear file
    # ===================================
    tobj = radset['time_obj']
    filemap = nawdex_analysis.io.selector.make_filetime_index('swf_net', tobj, 
                                                filepart = filepart, 
                                                subdirs=['retrieved_clearsky_netswf'])

    # print filemap    

    # input swf clear
    # ===============
    clearname = filemap[tobj][0]
    clearset = read_data_field(clearname, tobj, 'swf_net', region ='atlantic')
    dset['swf_net_clear'] = clearset['swf_net']    


    # long-wave filename
    # ====================
    lwfclearname = clearname.replace('retrieved_clearsky_netswf/clearsky_netswf-', 'sim-toarad/toa_clear_radflux-' )
    lwfclearname = lwfclearname.replace(filepart,'')

    print radname, clearname, lwfclearname

    # input lwf clear data
    # ====================
    lwfclearset = read_data_field(lwfclearname, tobj, 'lwf', region ='atlantic')
    dset['lwf_clear'] = lwfclearset['lwf'] + lwf_clear_offset
    


    # input cloud type
    # ====================
    ctset = read_data_field( ctname, tobj, 'CT', region = 'atlantic')
    dset.update( ctset )



    # select and modify region mask
    # ==============================
    region_mask = dset['mask']
        
    # possible extension (get away from coast)
    nedge = 11
    region_mask = scipy.ndimage.minimum_filter( region_mask, nedge)


    # finally prepare georef
    # =======================
    mlon =  dset['lon'][region_mask].mean()
    mlat =  dset['lat'][region_mask].mean()

    x, y = gi.ll2xyc( dset['lon'], dset['lat'], mlon = mlon, mlat = mlat )
    a = gi.simple_pixel_area(x, y, xy = True)

    # update mask and area
    dset['mask'] = region_mask
    dset['area'] = a
        
    return dset
                
######################################################################
######################################################################


def collect_data4cre_sim( radname, itime ):

    '''
    Collects a set of simulated data fields for cloud-radiative effect analysis.  

    
    Parameters
    ----------
    radname : str
       name of toa allsky radiation file

    itime : int
       time index of data fields ('swf_net' and 'lwf') in radname


    Returns
    --------
    dset : dict
       dataset dict containing swf, lwf and ct fields
    '''
    
    # set filenames
    clearname = radname.replace('toa_', 'toa_clear_')
    ctname = radname2ctname( radname, datatype = 'sim' )

    # read data
    dset = {}
    for vname in ['lwf', 'swf_net']:
        radset = read_data_field(radname, itime, vname, region='atlantic')
        dset[vname] = radset[vname]
        
        clearset = read_data_field(clearname, itime, vname, region ='atlantic')
        dset['%s_clear' % vname] = clearset[vname]
    
    ctset = read_data_field( ctname, radset['time_obj'], 'CT', region = 'atlantic')
    dset.update( ctset    )
    # select region mask
    region_mask = dset['mask']
        
    # possible extension (get away from coast)
    nedge = 11
    region_mask = scipy.ndimage.minimum_filter( region_mask, nedge)

    mlon =  dset['lon'][region_mask].mean()
    mlat =  dset['lat'][region_mask].mean()

    x, y = gi.ll2xyc( dset['lon'], dset['lat'], mlon = mlon, mlat = mlat )
    a = gi.simple_pixel_area(x, y, xy = True)

    # update mask and area
    dset['mask'] = region_mask
    dset['area'] = a
        
    return dset
        
######################################################################
######################################################################


def collect_data4cre( radname, itime, **kwargs ):

    '''
    Collects a set of data fields (observed or simulated) for cloud-radiative effect analysis.  

    
    Parameters
    ----------
    radname : str
       name of toa allsky radiation file

    itime : int
       time index of data fields ('swf_net' and 'lwf') in radname

    **kwargs : dict
       set of keywords for data input, e.g.
       filepart in ['-scaled', '-not_scaled']  only for obs !!!


    Returns
    --------
    dset : dict
       dataset dict containing swf, lwf and ct fields
    '''
    

    # select obs or sim reader
    if 'gerb' in radname:
        return collect_data4cre_obs( radname, itime, **kwargs)
    elif 'sim-toarad' in radname:
        return collect_data4cre_sim( radname, itime)


######################################################################
######################################################################



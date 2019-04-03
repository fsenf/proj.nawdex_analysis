#!/usr/bin/env python

import numpy as np
import xarray as xr

import tropy.io_tools.netcdf as ncio

from averaging import area_weighted_binwise_averages, area_fractions
import nawdex_analysis.io.input_lev2

######################################################################
######################################################################


def ave_cre_from_radname( radname, itime, **kwargs ):
       
    '''
    Calculate Cloud-radiative effect (CRE) for different cloud types.

    
    Parameters
    ----------
    radname : str
       name of toa allsky radiation file

    itime : int
       time index of data fields ('swf_net' and 'lwf') in radname

    filepart : str, optional, default = '-scaled'
       part in the file that gives information about scaling of clear-sky fields
       either '-scaled' or '-not_scaled'


    Returns
    --------
    outset : xarray Dataset
       dataset containing average longwave, short-wave CRE and area fractions
       depending on cloud type
    '''

    # input fields
    dset = nawdex_analysis.io.input_lev2.collect_data4cre( radname, itime, **kwargs )
    
    
    # prepare analysis array
    m = dset['mask']

    a = dset['area'][m]
    ct = dset['CT'][m]
    lcre = (dset['lwf'] - dset['lwf_clear'])[m]
    scre = (dset['swf_net'] - dset['swf_net_clear'])[m]

    # nan values for sun below ground ...
    scre[np.isnan(scre)] = 0.
    
    
    # calculate area-weighted CRE average
    ctbins =  np.arange(0,22)
    lcre_ave = area_weighted_binwise_averages(lcre, a, ct, ctbins)
    scre_ave = area_weighted_binwise_averages(scre, a, ct, ctbins)
    afrac = area_fractions( a, ct, ctbins ) * 100.
    
    # rewrite data into xarray
    ct_map = [2, 6, 8, 10, 12, 14, 15, 16, 17, 18, 19]

    ct_labels = [ 'clear_ocean',  'very low', 'low', 'middle', 'high opaque', 
                                 'very high opaque', 'semi. thin', 'semi. meanly thick', 
                                 'semi. thick', 'semi. above', 'fractional'
                             ] 
    
    outset = xr.Dataset({'ct' : ('ct', ct_labels, {}),
                     'time' : ('time', [dset['time_obj'],], {}),
                    'scre_ave' : (('time','ct'), np.array( [scre_ave,] )[:,ct_map], 
                                  {'units' : 'W m^{-2}', 'longname':'area-average shortwave CRE '}),
                    'scre_ave' : (('time','ct'), np.array( [scre_ave,] )[:,ct_map], 
                                  {'units' : 'W m^{-2}', 'longname':'area-average shortwave CRE '}),
                    'afrac' : (('time','ct'), np.array( [afrac,] )[:,ct_map], 
                                  {'units' : '%', 'longname':'relative area fractions per cloud type'})})

    return outset

######################################################################
######################################################################


def ave_cre_from_radname_tloop( radname, **kwargs ):

    '''
    Calculate Cloud-radiative effect (CRE) for different cloud types (time loop).

    
    Parameters
    ----------
    radname : str
       name of toa allsky radiation file

    filepart : str, optional, default = '-scaled'
       part in the file that gives information about scaling of clear-sky fields
       either '-scaled' or '-not_scaled'


    Returns
    --------
    outset : xarray Dataset
       dataset containing average longwave, short-wave CRE and area fractions
       depending on cloud type
    '''
    
    # get time dimension
    ntimes = ncio.read_icon_dimension(radname, 'time')

    outset = []
    for itime in range( ntimes ):
    #for itime in [2,3]:    
        try:
            outset += [ave_cre_from_radname(radname, itime, **kwargs), ]
        except:
            print 'error at %d' %  itime
        
    return xr.merge( outset )

######################################################################
######################################################################

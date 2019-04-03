#!/usr/bin/env python

import numpy as np
import xarray as xr

import tropy.io_tools.netcdf as ncio

from averaging import area_weighted_binwise_averages
import nawdex_tools.io.input_lev2

######################################################################
######################################################################


def ave_cre_from_radname( radname, itime ):
    
    # input fields
    dset = nawdex_tools.io.input_lev2.collect_data4cre( radname, itime )
    
    
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

    
    # rewrite data into xarray
    ct_map = [6, 8, 10, 12, 14, 15, 16, 17, 18, 19]

    ct_labels = [ 'very low', 'low', 'middle', 'high opaque', 
                                 'very high opaque', 'semi. thin', 'semi. meanly thick', 
                                 'semi. thick', 'semi. above', 'fractional'
                             ] 
    
    outset = xr.Dataset({'ct' : ('ct', ct_labels, {}),
                     'time' : ('time', [dset['time_obj'],], {}),
                    'scre_ave' : (('time','ct'), np.array( [scre_ave,] )[:,ct_map], 
                                  {'units' : 'W m^{-2}', 'longname':'area-average shortwave CRE '}),
                    'lcre_ave' : (('time','ct'), np.array( [lcre_ave,] )[:,ct_map], 
                                  {'units' : 'W m^{-2}', 'longname':'area-average longwave CRE '})})

    return outset

######################################################################
######################################################################


def ave_cre_from_radname_tloop( radname ):
    
    # get time dimension
    ntimes = ncio.read_icon_dimension(radname, 'time')

    outset = []
    for itime in range( ntimes ):
    #for itime in [2,3]:    
        try:
            outset += [ave_cre_from_radname(radname, itime), ]
        except:
            print 'error at %d' %  itime
        
    return xr.merge( outset )

######################################################################
######################################################################

#!/usr/bin/env python

import numpy as np
import xarray as xr

import tropy.io_tools.netcdf as ncio

from averaging import area_weighted_binwise_averages, area_fractions
import nawdex_analysis.io.input_lev2

######################################################################
######################################################################


def ave_cre_from_radname( radname, itime, factor = -1, **kwargs ):
       
    '''
    Calculate Cloud-radiative effect (CRE) for different cloud types.

    
    Parameters
    ----------
    radname : str
       name of toa allsky radiation file

    itime : int
       time index of data fields ('swf_net' and 'lwf') in radname

    factor : float
       factor used to convert direction conversion (outward vs. inward)

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
                    'scre_ave' : (('time','ct'), factor * np.array( [scre_ave,] )[:,ct_map], 
                                  {'units' : 'W m^{-2}', 'longname':'area-average shortwave CRE '}),
                    'lcre_ave' : (('time','ct'), factor * np.array( [lcre_ave,] )[:,ct_map], 
                                  {'units' : 'W m^{-2}', 'longname':'area-average longwave CRE '}),
                    'afrac' : (('time','ct'), np.array( [afrac,] )[:,ct_map], 
                                  {'units' : '%', 'longname':'relative area fractions per cloud type'})})

    return outset

######################################################################
######################################################################


def ave_radfluxes_from_radname( radname, itime, **kwargs ):
       
    '''
    Calculate Cloud-radiative effect (CRE) for different cloud types.

    
    Parameters
    ----------
    radname : str
       name of toa allsky radiation file

    itime : int
       time index of data fields ('swf_net' and 'lwf') in radname

    factor : float
       factor used to convert direction conversion (outward vs. inward)

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
    # ============
    dset = nawdex_analysis.io.input_lev2.collect_data4cre( radname, itime, **kwargs )
    
    
    # prepare analysis array
    # =======================
    m = dset['mask']
    a = dset['area'][m]
    ct = dset['CT'][m]


    # define cloud type bins 
    # =======================
    ctbins =  np.arange(0, 22)
    ct_map = [2, 6, 8, 10, 12, 14, 15, 16, 17, 18, 19]
    ct_labels = [ 'clear_ocean',  'very low', 'low', 'middle', 'high opaque', 
                                 'very high opaque', 'semi. thin', 'semi. meanly thick', 
                                 'semi. thick', 'semi. above', 'fractional'] 
    

    # prepare all variables
    # ======================
    radflux_namelist = ['lwf', 'lwf_clear', 'swf_net', 'swf_net_clear', 'swf_down', 'swf_up', 'swf_up_clear']

    ave_rflux = {}
    for rname in radflux_namelist:
        
        v = dset[rname][m].copy()

        # dirty bugfix: set missing SWF to zero
        if 'swf' in rname:
            v[np.isnan(v)] = 0.

        ave_rflux[ rname ] = area_weighted_binwise_averages(v, a, ct, ctbins)
        

    # calculate area-weighted CRE average
    # ===================================
    afrac = area_fractions( a, ct, ctbins ) * 100.
    

    # prepare variables
    # ==================
    attrs = {}
    attrs['lwf'] = {'units' : 'W m^{-2}', 'longname':'area-average longwave radiation flux (all-sky)'}
    attrs['lwf_clear'] = {'units' : 'W m^{-2}', 'longname':'area-average longwave radiation flux (clearsky)'}

    attrs['swf_net'] = {'units' : 'W m^{-2}', 'longname':'area-average net shortwave radiation flux (all-sky)'}
    attrs['swf_net_clear'] = {'units' : 'W m^{-2}', 'longname':'area-average net shortwave radiation flux (clearsky)'}

    attrs['swf_down'] = {'units' : 'W m^{-2}', 'longname':'area-average downwelling shortwave radiation flux'}

    attrs['swf_up'] = {'units' : 'W m^{-2}', 'longname':'area-average upwelling shortwave radiation flux (all-sky)'}
    attrs['swf_up_clear'] = {'units' : 'W m^{-2}', 'longname':'area-average upwelling shortwave radiation flux (clearsky)'}
    


    # prepare variable dict
    # =====================
    vardict = {}
    for rname in radflux_namelist:
        vardict[rname] = (('time','ct'), np.array( [ave_rflux[rname],] )[:,ct_map], attrs[rname])

    vardict['ct']    =  ('ct', ct_labels, {})
    vardict['time']  =  ('time', [dset['time_obj'],], {})
    vardict['afrac'] =  (('time','ct'), np.array( [afrac,] )[:,ct_map], 
                         {'units' : '%', 'longname':'relative area fractions per cloud type'})


    # rewrite data into xarray
    # =========================
    outset = xr.Dataset( vardict )


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

    # using a keyword to select output variable type
    output_vars = kwargs.pop('output_vars', 'cre')

    if output_vars == 'cre':
        calculate_average_function = ave_cre_from_radname
    elif output_vars == 'radfluxes':
        calculate_average_function = ave_radfluxes_from_radname

    
    # get time dimension
    ntimes = ncio.read_icon_dimension(radname, 'time')

    outset = []
    for itime in range( ntimes ):
    #for itime in [2,3]:    
        try:
            outset += [calculate_average_function(radname, itime, **kwargs), ]
        except:
            print 'error at %d' %  itime
        
    return xr.merge( outset )

######################################################################
######################################################################

def radflux2cre( dset, scaling = False, new_factor = 0.88, old_factor = 0.9 ):
    
    '''
    Converts radiation fluxes to CRE.
    
    
    Parameters
    ----------
    dset : xarray
        radiation flux dataset (incl. clearsky fluxes)
        
        also used for output
        
    scaling : bool, optional
        if True: re-scaling of clear observed SWF is applied

    new_factor :  float, optional
        only used if scaling == True, new factor to be used for clearsky scaling

    old_factor :  float, optional
        only used if scaling == True, old factor that was applied to scale the clearsky

    
    Returns
    --------
    None
        
    '''
    
    # if needed do scaling
    if scaling:
        
        # get position for re-scaling
        idlist = list( dset.idname.data )
        index4rescaling = idlist.index('msevi-scaled')
        
        # scaling array
        scaling = xr.DataArray( np.ones( len(idlist) ), dims = 'idname')
        scaling[index4rescaling] = new_factor / old_factor
        
        dset['swf_net_clear'] = scaling * dset['swf_net_clear']
        

    
    # net flux
    dset['fnet'] = dset['swf_net'] +  dset['lwf']
    dset['fnet_clear'] = dset['swf_net_clear'] +  dset['lwf_clear']
    
    
    # CREs
    dset['scre_ave'] = dset['swf_net_clear'] - dset['swf_net']
    dset['lcre_ave'] = dset['lwf_clear'] - dset['lwf']
    dset['net_cre_ave'] = dset['scre_ave'] + dset['lcre_ave']
    
    
    # CRE contributions (weighted by cloud fraction)
    weight =  dset['afrac'] / 100.
    dset['scre_contrib']    = weight * dset['scre_ave']
    dset['lcre_contrib']    = weight * dset['lcre_ave']
    dset['net_cre_contrib'] = weight * dset['net_cre_ave']
    
    return 

######################################################################
######################################################################

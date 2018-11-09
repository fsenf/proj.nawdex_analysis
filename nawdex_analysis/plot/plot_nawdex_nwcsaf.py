#!/usr/bin/env python

import os, sys
import numpy as np
import matplotlib
matplotlib.use('AGG')



import pylab as pl
import datetime

import nawdex_analysis.plot.nawdex_map as nawdex_map

import tropy.io_tools.netcdf as ncio
import tropy.io_tools.hdf as hio
from tropy.standard_config import *

######################################################################
######################################################################

def prepare_data_for_plotting( fname, itime, prodname):

    '''
    Prepares data for plotting.

    Parameters
    ----------
    fname : str
        input data file name

    itime : int
        time index for which data is read

    prodname : str
        name of the product read
    

    Returns 
    --------
    dset : dict
        dataset dictionary

    '''

    # read bt variables
    dset = ncio.read_icon_4d_data(fname, [prodname], itime = itime)
    
    # read geo-ref
    geo = ncio.read_icon_4d_data(fname, ['lon', 'lat'], itime = None)
    dset.update( geo )

    # also get mask
    mfile = '%s/icon/nawdex/region_masks_for_msevi_nawdex.h5' % local_data_path
    dset['mask'] = hio.read_var_from_hdf(mfile, 'full_region')
    
    dset['time_obj'] = ncio.read_icon_time(fname, itime = itime)
    dset['time_str'] =  time_obj.strftime('%Y-%m-%d %H:%M UTC')

    return dset

######################################################################
######################################################################


def plot_prods(fname, itime, prodname):

    '''
    Plots a selected NWCSAF product given a netcdf filename.


    Parameters
    ----------
    fname : str
        input data file name

    itime : int
        time index for which data is read

    prodname : str
        name of the product read
    

    Returns 
    --------
    None
    '''

    # input data
    dset = prepare_data_for_plotting( fname, itime, prodname)


    # get subpath from name
    basename = os.path.splitext( os.path.basename( fname ) )[0] 
    dirname = os.path.dirname( fname )
    subpath = dirname.split('/')[-1]


    if 'synsat' in basename:
        prefix = 'Synthetic'    

    else:
        prefix = 'Observed'
 

    # plots
    pl.figure( figsize = (12, 5) )
    mp = nawdex_map.nawdex_nwcsaf_plot(dset, vname = prodname)

    
    pl.title('%s NWCSAF %s  @  %s' % (subpath, prodname, time_str ))

    picname = '../pics/%s/nawdex-nwcsaf_%s_%s_%s.jpg' % (subpath, 
                                                  mode,
                                                  prodname,
                                                  time_obj.strftime('%Y-%m-%d_%H'))
    print '... save image to %s' % picname
    pl.subplots_adjust(bottom = 0.02, right = 0.85)
    pl.savefig(picname, dpi = 100)
    pl.close()

    return



######################################################################
######################################################################


def all_plots_for_file( fname ):

    '''
    Make NWCSAF plots for a file.


    Parameters
    ----------
    fname : str
        input data file name


    Returns
    --------
    None
    '''

    # first get the time dimension
    ntime = ncio.read_icon_dimension( fname, 'time' )


    # time loop
    for itime in range(ntime):
        plot_prods(fname, itime, 'CMa')
        plot_prods(fname, itime, 'CT')


    return

######################################################################
######################################################################

if __name__ == '__main__':


    # get arguments
    fname = sys.argv[1]

    # prodname = sys.argv[2]
    all_plots_for_file( fname )


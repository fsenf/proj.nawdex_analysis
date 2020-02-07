#!/usr/bin/env python

import os, sys
import numpy as np
import matplotlib
# matplotlib.use('AGG')



import pylab as pl
import datetime


import tropy.io_tools.netcdf as ncio
import tropy.io_tools.hdf as hio
from tropy.standard_config import *

from ..plot import nawdex_map
from ..io.input_lev2 import  read_data_field


######################################################################
######################################################################


def plot_prods(fname, itime, prodname, pics_dir = '../pics'):

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

    pics_dir : str, optional, default = '../pics'
        main directory for images
    

    Returns 
    --------
    None
    '''

    # input data
    dset = read_data_field( fname, itime, prodname)
    time_obj = dset['time_obj']
    time_str = dset['time_str']
    
    # get subpath from name
    basename = os.path.splitext( os.path.basename( fname ) )[0] 
    dirname = os.path.dirname( fname )


    if 'synsat' in basename:
        prefix = 'Synthetic'    
        mode = basename
    else:
        prefix = 'Observed'
        mode = 'meteosat'

    # plots
    pl.figure( figsize = (12, 5) )
    mp = nawdex_map.nawdex_nwcsaf_plot(dset, vname = prodname)

    
    pl.title('%s NWCSAF %s  @  %s' % (mode, prodname, time_str ))
    pl.subplots_adjust(bottom = 0.02, right = 0.85)


    # save image
    full_pics_dir = '%s/%s' % (pics_dir, mode)
    picname = '%s/nawdex-nwcsaf_%s_%s_%s.jpg' % (full_pics_dir, 
                                                 mode,
                                                 prodname,
                                                 time_obj.strftime('%Y-%m-%d_%H%M'))
    print(('... save image to %s' % picname))
    if not os.path.isdir(full_pics_dir):
        os.makedirs( full_pics_dir )

    pl.savefig(picname, dpi = 100)
    pl.close()

    return



######################################################################
######################################################################


def all_nwcsaf_plots_for_file( fname , pics_dir = '../pics/'):

    '''
    Make NWCSAF plots for a file.


    Parameters
    ----------
    fname : str
        input data file name

    pics_dir : str, optional, default = '../pics'
        main directory for images


    Returns
    --------
    None
    '''

    # first get the time dimension
    ntime = ncio.read_icon_dimension( fname, 'time' )


    # time loop
    for itime in range(ntime):
        plot_prods(fname, itime, 'CMa', pics_dir = pics_dir)
        plot_prods(fname, itime, 'CT', pics_dir = pics_dir)


    return

######################################################################
######################################################################

if __name__ == '__main__':


    # get arguments
    fname = sys.argv[1]

    # prodname = sys.argv[2]
    all_nwcsaf_plots_for_file( fname )


#!/usr/bin/env python

'''
A set of function of vertically stacked analysis plots.

Especially, to have a fast interface to make plot of CRE dependence
on cloud type.
'''

import os, sys
import numpy as np

import pylab as pl
import xarray as xr
import seaborn as sns

import string
abc = string.ascii_lowercase

# --------------------------------------------------------------------
from ..io import collector
from .exp_layout import get_plotting_order, get_exp_kws, get_exp_kws_bars
from ..io.tools import round2day


######################################################################
######################################################################

def vert_stacked_exp_plot( dset, vname, var_err = None, idlist = 'all', catlist = 'all', iddim = 'idname', catdim = 'ct', 
                           obsref_name = 'msevi-scaled', doffset = 0.05, offset0 = -0.4, connect2obs = True,
                           make_labels = True):

    '''
    A generic function that makes a colorful plot with categories stacked in the vertical.
    In each category, the different IDs are also stacked.
    
    
    Parameters
    ----------
    dset : xarray Dataset
        dataset object containing variables for different IDs and categories
    
    vname : str
        variable to be plotted

    var_err : xarray Dataset
        dataset containing error information to be plotted 
        (having similar dimensions as dset)
    
    idlist : list, optional, default = 'all'
        list of IDnames to be stacked and compared
        if 'all': all IDs will be used

    catlist : list, optional, default = 'all'
        list of categories to be stacked and compared
        if 'all': all categories will be used

    iddim : str, optional, default = 'idname'
        name of the dimension that contains IDnames

    catdim : str, optional, default = 'idname'
        name of the dimension that contains category names

    
    Returns
    --------
    ax : pylab axis object
        axis instance which contains the plot
    
    '''
    
    # preparation of plotting variables
    # ==================================
    
    # get ID list
    if idlist == 'all':
        idlist = list( dset[iddim].data )
        
    # get the plotting order (pre-defined)
    order = get_plotting_order( idlist )
    
    # get category list
    if catlist == 'all':
        catlist = list( dset[catdim].data )
        
    # extract variable
    var = dset[vname]
    
    cindex = []
    icount = 0
    for catname in catlist:
        
        # get variables for categories
        vc = var.sel({catdim : catname})
    
        cindex += [ 1 * icount, ]
        # yobs = icount
        offset = offset0
       

        # get y-position of obs data 
        for n, idname in enumerate( np.array(idlist)[order] ):
            y = icount + offset
                
            # select place
            if idname == obsref_name:
                yobs = y
            offset += doffset


        # do the plotting 
        offset = offset0

        for n, idname in enumerate( np.array(idlist)[order] ):

            
            # select variables
            x = vc.sel({iddim : idname})
            xo = vc.sel({iddim : obsref_name})
            y = icount + offset
 
            
            # get plotting style
            kws = get_exp_kws( idname, ptype = 'points' )
            kws['linewidth'] = 2
            
            if icount == 0:
                label = idname
            else:
                label = None
                
            pl.plot(x, y, label = label, **kws )
            
            # functionality for errobars
            if var_err is not None:
                dx = var_err.sel({catdim : catname, iddim : idname})[vname].data
                if np.size( dx ) == 2:
                    dx = dx.reshape(2, 1)

                kws = get_exp_kws( idname, ptype = 'lines' )
                pl.errorbar( x, y, xerr = dx, **kws)

            if connect2obs: 
                    pl.plot( [xo, x], [yobs, y], color = 'gray', lw = 1, alpha = 0.5)

            offset += doffset

        icount += 1
    
    pl.yticks( cindex, catlist )


    return


######################################################################
######################################################################

def plot_scre_lcre4set( set_number, dset = None, fig = None, ax = None, plot_legend = True, xlim = (-200,200), **kwargs ):
    
    '''
    Convenience function to easily plot shortwave vs. longwave CRE comparision
    
    
    Parameters
    ----------
    set_number : int
        number of the analysis set to be plotted
        
    dset : xarray dataset, optional, default = None
        to make fast plots input of data could be made externally
        and provide through this keyword
    
    fig : pylab figure object, optional, default = None
         to provide an already existing figure where the plot is placed in
         if None: as new figure is created
    
    ax : pylab axis object, optional, default = None
         to provide an already existing axis where the plot is placed in
         if None: as new axis is created
         
    plot_legend : bool, optional, default = True
        switch if legend is plotted
        
    xlim : tuple, optional, default = (-200, 200)
        default x-range 
        
    **kwargs : content of dict, optional
        keywords that are passed to ``vert_stacked_exp_plot``
    
    
    Returns
    --------
    None
    '''

    
    # input if needed
    if dset is None:
        dset = collector.get_cre4set( set_number )

    if set_number == 2:
        figsize = (12,15)
    else:
        figsize = (10,15)

    if fig is None:
        fig = pl.figure( figsize = figsize )
        
    if ax is not None:
        pl.sca( ax )
        
    
    # get time range
    tmin = dset.time.min().data.astype( dtype='datetime64[D]' )
    tmin = np.datetime_as_string( tmin, unit = 'D')

    tmax = dset.time.max()
    tmax = np.datetime_as_string( round2day( tmax ), unit = 'D')


    for vname in ['scre_ave', 'lcre_ave']:   #
        vert_stacked_exp_plot(dset.mean('time'), vname, **kwargs)

        if vname == 'scre_ave' and plot_legend:
            pl.legend( loc='center right', bbox_to_anchor=(1.75, 0.5) )
        
    pl.xlabel( 'CRE $(\mathrm{W\,m^{-2}}$)')
    pl.title('(%s) In-Cloud Radiative Effect per Cloud Type \n %s to %s' % ( abc[set_number - 1], tmin, tmax ), fontweight = 'bold')
    # pl.title('%s to %s' % ( dates.start, dates.stop ))
    # pl.suptitle('Cloud Cover per Cloud Type', fontweight = 'bold')
    
    pl.axvline( 0, color = 'gray', alpha = 0.5)
    if set_number == 2:
        pl.subplots_adjust( left = 0.35, right = 0.7)
    else:
        pl.subplots_adjust( left = 0.35)

    sns.despine()
    pl.text( xlim[0] / 2, -0.5, 'Shortwave', 
            color = 'gray', ha = 'center', va = 'center', alpha = 0.7, 
            fontweight = 'bold', fontsize = 'large')

    pl.text( xlim[1] / 2, -0.5, 'Longwave', 
            color = 'gray', ha = 'center', va = 'center', alpha = 0.7, 
            fontweight = 'bold', fontsize = 'large')
    pl.xlim(*xlim)
    
    return

######################################################################
######################################################################

def plot_net_cre_contrib4set( set_number, dset = None, plot_legend = True, plot_suptitle = True, **kwargs ):
    
    '''
    Convenience function to easily plot net CRE comparision.
    
    
    Parameters
    ----------
    set_number : int
        number of the analysis set to be plotted
        
    dset : xarray dataset, optional, default = None
        to make fast plots input of data could be made externally
        and provide through this keyword
    
    fig : pylab figure object, optional, default = None
         to provide an already existing figure where the plot is placed in
         if None: as new figure is created
    
    ax : pylab axis object, optional, default = None
         to provide an already existing axis where the plot is placed in
         if None: as new axis is created
         
    plot_legend : bool, optional, default = True
        switch if legend is plotted
        
    xlim : tuple, optional, default = (-200, 200)
        default x-range 
        
    **kwargs : content of dict, optional
        keywords that are passed to ``vert_stacked_exp_plot``
    
    
    Returns
    --------
    None
    '''
    
    # input if needed
    if dset is None:
        dset = collector.get_cre4set( set_number )

    if set_number == 2:
        figsize = (12,15)
    else:
        figsize = (10,15)

    if fig is None:
        fig = pl.figure( figsize = figsize )
        
    if ax is not None:
        pl.sca( ax )

    # get time range
    tmin = dset.time.min().data.astype( dtype='datetime64[D]' )
    tmin = np.datetime_as_string( tmin, unit = 'D')

    tmax = dset.time.max()
    tmax = np.datetime_as_string( round2day( tmax ), unit = 'D')

    # calculate net effect 
    dset['net_cre_ave'] = dset['afrac'] / 100. * (dset['lcre_ave'] + dset['scre_ave'])
    
    # and plot
    for vname in ['net_cre_ave',]:   #
        vert_stacked_exp_plot(dset.mean('time'), vname, **kwargs)
        pl.legend( loc='center right', bbox_to_anchor=(1.75, 0.5) )
        
            
    pl.xlabel( 'Net CRE (W/m**2)')
    if plot_suptitle:
        pl.suptitle('Net CRE per Cloud Type' , fontsize = 'x-large', fontweight = 'bold')

    pl.title('(%s) %s to %s' % ( abc[set_number - 1], tmin, tmax ), fontweight = 'bold')
    # pl.title('%s to %s' % ( dates.start, dates.stop ))
    # pl.suptitle('Cloud Cover per Cloud Type', fontweight = 'bold')
    
    pl.axvline( 0, color = 'gray', alpha = 0.5)

    if set_number == 2:
        pl.subplots_adjust( left = 0.35, right = 0.7)
    else:
        pl.subplots_adjust( left = 0.35)

    sns.despine()
    pl.text( -3, -0.5, 'Cooling', 
            color = 'gray', ha = 'center', va = 'center', alpha = 0.7, 
            fontweight = 'bold', fontsize = 'large')

    
    return

######################################################################
######################################################################

def hor_barplot_exp_plot( dset, vname, idlist = 'all', catlist = 'all', iddim = 'idname', catdim = 'ct', 
                           obsref_name = 'msevi-scaled', doffset = 0.05, offset0 = -0.4, icount0 = 0,
                           make_labels = True):

    '''
    A generic function that makes a colorful plot with categories stacked in the vertical.
    In each category, the different IDs are also stacked.
    
    
    Parameters
    ----------
    dset : xarray Dataset
        dataset object containing variables for different IDs and categories
    
    vname : str
        variable to be plotted
    
    idlist : list, optional, default = 'all'
        list of IDnames to be stacked and compared
        if 'all': all IDs will be used

    catlist : list, optional, default = 'all'
        list of categories to be stacked and compared
        if 'all': all categories will be used

    iddim : str, optional, default = 'idname'
        name of the dimension that contains IDnames

    catdim : str, optional, default = 'idname'
        name of the dimension that contains category names

    
    Returns
    --------
    ax : pylab axis object
        axis instance which contains the plot
    
    '''
    
    # preparation of plotting variables
    # ==================================
    
    # get ID list
    if idlist == 'all':
        idlist = list( dset[iddim].data )
        
    # get the plotting order (pre-defined)
    order = get_plotting_order( idlist )
    
    # get category list
    if catlist == 'all':
        catlist = list( dset[catdim].data )
        
    # extract variable
    var = dset[vname]
    
    cindex = []
    icount = icount0
    for catname in catlist:
        
        # get variables for categories
        vc = var.sel({catdim : catname})
    
        cindex += [ 1 * icount, ]
        
        yobs = icount
        offset = offset0
        
        for n, idname in enumerate( np.array(idlist)[order] ):

            
            # select variables
            x = vc.sel({iddim : idname})
            xo = vc.sel({iddim : obsref_name})
                
            # select place
            if idname == obsref_name:
                y = yobs
                continue
            else:
                y = yobs + offset
                
            
            # get plotting style
            kws = get_exp_kws_bars( idname )
            kws['linewidth'] = 2
            
            if icount == 0:
                label = idname
            else:
                label = None
                
            pl.bar( y, x - xo, doffset / 1.2, xo,  label = label, **kws )


            offset += doffset

        icount += 1

    pl.plot( [icount0 + offset0, icount0 + offset], [xo,xo],  color = 'k')

    pl.xticks( cindex, catlist )
    

    return

######################################################################
######################################################################

def stacker4flamingo( dv, vlist, scal = 0.1, offset = 0, output_stacked_vars = True ):
    
    '''
    Makes a cumulative data stack for flamingo plot.
    
    
    Parameters
    ----------
    dv : xarray dataset
        radiation flux deviations
        
    vlist : list
        list of radiation variable to be stacked
        
    scal : float, optional
        scaling of the x-variable (x is counter)

    offset : float, optional
        offset of the x-variable (x is counter)
    
    output_stacked_vars : bool, optional
        if True: the output is stacked (two values for each deviation)
        
        
    Returns
    --------
    x : numpy array
        counter variable
    
    y : numpy array
        cumulative deviaitons
    '''
    
    nvar = len( vlist )
    
    xi = np.arange( nvar ) * scal + offset
    
    
    yval = []
    for i in range( nvar ):    
        vname = vlist[i]
        yval.append( dv[vname].data )
    yval = np.array( yval )
    
    yi = yval.cumsum()
    
        
    x = []
    y = [0, ]
    
    for i in range( nvar ):
        x.append( xi[i] )
        x.append( xi[i] )
        y.append( yi[i] )
        y.append( yi[i] )
    y.pop(-1)
    
    x = np.array( x )
    y = np.array( y )
    
    if output_stacked_vars:
        return x, y
    else:
        return xi, yi

######################################################################
######################################################################

def hor_flamingo_plots(cset2, id1_list, id2_list, vlist = ['swf_up', 'swf_down', 'lwf'], scale = 0.2):

    '''
    Make a horizontal flamingo / snake plot.
    
    
    Parameters
    ----------
    cset2 : xarray dataset
        radiation data
        
    id1_list : list
        list for variable IDs that are used as reference (for deviation calculation)

    id2_list : list
        list for variable IDs from which reference is subtracted
        
    vlist : list, optional
        list of radiation variables
        
    scale : float, optional
        optional scaling of x-range (for variable stack)
        
        
    Returns
    -------
    None
        
    
    '''
    order = get_plotting_order( id2_list )

    for i, id2 in enumerate( np.array(id2_list)[order] ):

        # get reference ID
        id1 = np.array(id1_list)[order][i]
        
        # get variable fields
        v1 = cset2.sel(idname = id1)
        v2 = cset2.sel(idname = id2)

        # calculate difference
        dv = v2 - v1 

        # point plots
        x, y =  stacker4flamingo(dv, vlist, offset = scale * i)
        kws = get_exp_kws(id2, ptype='points')
        pl.plot( [ x[-1]], [ y[-1]], **kws )

        # line plots
        kws = get_exp_kws(id2, ptype='lines')
        pl.plot( x, y, **kws )

    pl.xticks([], [])

    sns.despine()
    pl.ylabel('$\Delta F_\mathrm{net} \;(\mathrm{W\,m^{-2}})$')
    pl.axhline(0, color = 'gray', alpha = 0.3, lw = 3)
    return 

######################################################################
######################################################################

#!/usr/bin/env python


from mpl_toolkits.basemap import Basemap
import numpy as np
import pylab as pl


from tropy.plotting_tools.colormaps import enhanced_colormap, enhanced_wv62_cmap


######################################################################
######################################################################

def nawdex_map( region = 'zenith75' , color = 'black'):
    
    '''
    Draws a map in cylindric projection.

    
    Parameters
    ----------
    region : str, optional, default = 'zenith75'
         region selection

         possible arguments:
         'max-extent' : full NAWDEX simulations region
         'zenith75' : cutout of the NAWDEX region where zenith_angle < 75 degree fits in
         'atlantic' : cutout of the North Atlantic

    color : str, optional, default = 'black'
         color of the coastlines and country borders
    '''

    if region == 'max-extent':
        m = Basemap(projection = 'cyl',llcrnrlat = 23, urcrnrlat = 81, llcrnrlon = -79, urcrnrlon = 41,resolution='i')
    elif region == 'zenith75':
        m = Basemap(projection = 'cyl',llcrnrlat = 23,urcrnrlat = 66.5, llcrnrlon = -65, urcrnrlon = 40,resolution='i')
    elif region == 'atlantic':
        m = Basemap(projection = 'cyl',llcrnrlat = 23, urcrnrlat = 66.5, llcrnrlon = -65, urcrnrlon = 10, resolution='i')
    
    m.drawcoastlines(color = color)
    m.drawcountries(color = color)
    
    return m

######################################################################
######################################################################

def nawdex_bt_plot(dset, region = 'zenith75', vname = 'bt108', plot_colorbar = True):
        

    mp = nawdex_map( region = region, color = 'gold' )
    
    # map geo-ref 
    x, y = mp(dset['lon'], dset['lat'])
    m  = dset['mask']
    vm = np.ma.masked_where( ~m, dset[vname] )

    if vname == 'bt062':
        mp.pcolormesh(x, y, vm, 
                            cmap = enhanced_wv62_cmap(vmax = 260, vmed2 = 235, vmed1 = 225, vmin = 210),
                            vmin = 210,
                            vmax = 260)
           
    elif vname == 'bt108':
        mp.pcolormesh(x, y, vm, 
                            cmap = enhanced_colormap(),
                            vmin = 200,
                            vmax = 300)

    if plot_colorbar:
        mp.colorbar()

    return mp


######################################################################
######################################################################


def nawdex_rad_plot(dset, region = 'zenith75', vname = 'lwf', is_clear = True):
        

    mp = nawdex_map( region = region, color = 'gold' )
    
    # map geo-ref 
    x, y = mp(dset['lon'], dset['lat'])
    m  = dset['mask']

    vm = np.ma.masked_where( ~m, dset[vname] )

    if vname == 'lwf':
        mp.pcolormesh(x, y, vm, 
                            cmap = pl.cm.jet, 
                            vmin = 150, vmax = 350 )           
    elif vname == 'swf_net':
        mp.pcolormesh(x, y, vm, 
                            cmap = pl.cm.jet, 
                            vmin = -50, vmax = -900 )           


    mp.colorbar()

    return mp


######################################################################
######################################################################





def nawdex_nwcsaf_plot(dset, vname = 'CMa',region = 'zenith75', plot_colorbar = True):
        
        

    mp = nawdex_map( region = region, color = 'gold' )
    
    # map geo-ref 
    x, y = mp(dset['lon'], dset['lat'])
    m  = dset['mask']

    vm = np.ma.masked_where( ~m, dset[vname] )

    cmap = pl.cm.get_cmap('bone', 4)

    if vname == 'CMa':
        pcm = mp.pcolormesh(x, y, vm, cmap = cmap, vmin = 1, vmax = 5)


    if vname == 'CT':
        

        cmap = pl.matplotlib.colors.ListedColormap(['#007800', '#000000','#fabefa','#dca0dc',
                                                 '#ff6400', '#ff6400', '#ffb400', '#ffb400',
                                                 '#f0f000', '#f0f000','#d7d796','#d7d796',
                                                 '#e6e6e6', '#e6e6e6', '#0050d7', '#00b4e6',
                                                 '#00f0f0', '#5ac8a0', '#c800c8'])

        pcm = mp.pcolormesh(x,y, vm, cmap = cmap, vmin = 1, vmax = 20)


    if plot_colorbar:
        nwcsaf_product_colorbar( pcm, vname = vname )

    return mp


######################################################################
######################################################################


def nwcsaf_product_colorbar( pcm, vname = 'CMa', **kwargs ):



    if vname == 'CMa':
        cbar = mp.colorbar( pcm, ticks = [1.5, 2.5, 3.5, 4.5], 
                            **kwargs)
        cbar.ax.set_yticklabels( ['clear','partly cloudy','cloudy','outside'])

    elif vname == 'CT':
        cbar = mp.colorbar( pcm,  ticks=[ 1.5, 2.5, 3.5, 4.5, 6, 8, 10,12,14,
                                          15.5, 16.5, 17.5, 18.5, 19.5], 
                            **kwargs) 

        cbar.ax.set_yticklabels(['land', 'sea', 'snow', 'sea ice', 
                                 'very low', 'low', 'middle', 'high opaque', 
                                 'very high opaque', 'semi. thin', 'semi. meanly thick', 
                                 'semi. thick', 'semi. above', 'fractional'
                             ])

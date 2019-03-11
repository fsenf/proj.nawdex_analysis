#!/usr/bin/env python

'''
Definitions for plotting layout of different experiments.
'''

import numpy as np

######################################################################
######################################################################


def get_exp_kws( expname, ptype = 'lines' ):
    
    '''
    Wrapper for plotting keywords for different experiments.

    
    Parameters
    ----------
    expname : str
        experiment name


    Returns
    --------
    kws : dict
        collected keywords
    '''
    
    if ptype == 'lines':
        return get_exp_kws_lines( expname )
    
    elif ptype == 'points':
        return get_exp_kws_points( expname )
    


######################################################################
######################################################################


def get_exp_kws_lines( expname ):

    '''
    Plotting keywords for different experiments - lines.

    
    Parameters
    ----------
    expname : str
        experiment name


    Returns
    --------
    kws : dict
        collected keywords
    '''
    
    kws = dict()
    
    clist = ['#2d7ec6', '#227f7e', '#7d8111', '#ef823b', '#e01950', '#7c0011' ]
    # clist = ['#2D7EC6', '#227F7E', '#7D8111', '#EF823B', '#E019050', '#7C0011' ]
    resolutions = ['2km', '5km', '10km', '20km', '40km', '80km']
    
    if 'msevi' in expname:
        kws['color'] = 'k'
        kws['linewidth'] = 4
        kws['linestyle'] = '-'
        kws['zorder'] = 10

    else:
        for i, res in enumerate(resolutions):
            if res in expname:
                kws['color'] = clist[i]
                kws['linewidth'] = 2
            
        mis_number = int(expname.split('-')[-1])
        if np.mod(mis_number, 2) == 0:
            kws['linestyle'] = '-'
        else:
            kws['linestyle'] = '--'

            
    return kws


# In[607]:
######################################################################
######################################################################


def get_exp_kws_points( expname ):

    '''
    Plotting keywords for different experiments - points.

    
    Parameters
    ----------
    expname : str
        experiment name


    Returns
    --------
    kws : dict
        collected keywords
    '''
    
    kws = dict()
    
    clist = ['#2d7ec6', '#227f7e', '#7d8111', '#ef823b', '#e01950', '#7c0011' ]
    # clist = ['#2D7EC6', '#227F7E', '#7D8111', '#EF823B', '#E019050', '#7C0011' ]
    resolutions = ['2km', '5km', '10km', '20km', '40km', '80km']
    
    if 'msevi' in expname:
        kws['color'] = 'k'
        kws['marker'] = 'o'
        kws['zorder'] = 10
        kws['markersize'] = 10

    else:
        kws['markersize'] = 8
        for i, res in enumerate(resolutions):
            if res in expname:
                kws['color'] = clist[i]
            
        mis_number = int(expname.split('-')[-1])
        res = expname.split('-')[1]
        
        if np.mod(mis_number, 2) == 0:
            kws['marker'] = 's'
        else:
            kws['marker'] = 'o'

        # now select conv vs. noConv
        if res == '2km' and mis_number in [3,4]:
            kws['fillstyle'] = 'full'
        elif res == '2km' :
            kws['fillstyle'] = 'none'
            kws['markeredgewidth'] = 1.5
        
        c5 = (res == '5km' and mis_number in [3,4])
        c10 =(res == '10km' and mis_number in [3,4])
        
        if c5 or c10:
            kws['fillstyle'] = 'none'
            kws['markeredgewidth'] = 1.5

        elif res != '2km' :
            kws['fillstyle'] = 'full'
    
   #     if res in ['20km', '40km', '80km']:            
   #         kws['fillstyle'] = 'full'

    
    kws['linewidth'] = 0
    
    return kws

######################################################################
######################################################################

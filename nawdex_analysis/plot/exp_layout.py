#!/usr/bin/env python

'''
Definitions for plotting layout of different experiments.
'''

import numpy as np

from nawdex_analysis.io.selector import convert_explist2idlist

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


def get_exp_kws_lines( idname ):

    '''
    Plotting keywords for different experiments - lines.

    
    Parameters
    ----------
    idname : str
        configuration ID name


    Returns
    --------
    kws : dict
        collected keywords
    '''
    
    kws = dict()


    # set color
    # =========
    
    clist = ['#2d7ec6', '#227f7e', '#7d8111', '#ef823b', '#e01950', '#7c0011' ]
    # clist = ['#2D7EC6', '#227F7E', '#7D8111', '#EF823B', '#E019050', '#7C0011' ]
    resolutions = ['2km', '5km', '10km', '20km', '40km', '80km']
    
    if idname == 'msevi-scaled':
        kws['color'] = 'k'
        kws['linewidth'] = 4
        kws['linestyle'] = '-'
        kws['zorder'] = 10

    elif idname == 'msevi-not_scaled':
        kws['color'] = 'gray'
        kws['linewidth'] = 2
        kws['linestyle'] = '-'
        kws['zorder'] = 9

    else:
        for i, res in enumerate(resolutions):
            if res in idname:
                kws['color'] = clist[i]
                kws['linewidth'] = 2



    # set linestyle
    # =============
    if 'twoMom' in idname:
        kws['linestyle'] = '-'
    elif 'oneMom' in idname:
        kws['linestyle'] = '--'
        
            
    return kws

######################################################################
######################################################################


def get_exp_kws_points( idname ):

    '''
    Plotting keywords for different experiments - points.

    
    
    Parameters
    ----------
    idname : str
        configuration ID name


    Returns
    --------
    kws : dict
        collected keywords
    '''
    
    kws = dict()
    

    # set color
    # =========
    
    clist = ['#2d7ec6', '#227f7e', '#7d8111', '#ef823b', '#e01950', '#7c0011' ]
    # clist = ['#2D7EC6', '#227F7E', '#7D8111', '#EF823B', '#E019050', '#7C0011' ]
    resolutions = ['2km', '5km', '10km', '20km', '40km', '80km']
    
    if idname == 'msevi-scaled':
        kws['color'] = 'k'
        kws['linewidth'] = 4
        kws['linestyle'] = '-'
        kws['zorder'] = 10

    elif idname == 'msevi-not_scaled':
        kws['color'] = 'lightgray'
        kws['markeredgecolor'] = 'black'
        kws['linewidth'] = 2
        kws['linestyle'] = '-'
        kws['zorder'] = 9

    else:
        for i, res in enumerate(resolutions):
            if res in idname:
                kws['color'] = clist[i]
                kws['linewidth'] = 2

    # set marker
    # =========
    if idname == 'msevi-scaled':
        kws['marker'] = 'o'
        kws['zorder'] = 10
        kws['markersize'] = 10

    elif idname == 'msevi-not_scaled':
        kws['marker'] = 'D'
        kws['zorder'] = 9
        kws['markersize'] = 10

    else:
        kws['markersize'] = 8
        
        if 'twoMom' in idname:
            kws['marker'] = 's'
        elif 'oneMom' in idname:
            kws['marker'] = 'o'


        if '_Conv' in idname:
            kws['fillstyle'] = 'full'
        elif '_noConv' in idname:
            kws['fillstyle'] = 'none'
            kws['markeredgewidth'] = 1.5

    
    kws['linewidth'] = 0
    
    return kws

######################################################################
######################################################################


def get_exp_kws_bars( idname ):

    '''
    Plotting keywords for different experiments - lines.

    
    Parameters
    ----------
    idname : str
        configuration ID name


    Returns
    --------
    kws : dict
        collected keywords
    '''
    
    kws = dict()


    # set color
    # =========
    
    clist = ['#2d7ec6', '#227f7e', '#7d8111', '#ef823b', '#e01950', '#7c0011' ]
    # clist = ['#2D7EC6', '#227F7E', '#7D8111', '#EF823B', '#E019050', '#7C0011' ]
    resolutions = ['2km', '5km', '10km', '20km', '40km', '80km']
    
    if idname == 'msevi-scaled':
        kws['color'] = 'k'
        kws['linewidth'] = 4
        kws['linestyle'] = '-'
        kws['zorder'] = 10

    elif idname == 'msevi-not_scaled':
        kws['color'] = 'gray'
        kws['linewidth'] = 2
        kws['linestyle'] = '-'
        kws['zorder'] = 9

    else:
        for i, res in enumerate(resolutions):
            if res in idname:
            
                if '_Conv' in idname:
                    kws['color'] = clist[i]
                elif '_noConv' in idname:
                    kws['edgecolor'] = clist[i]
                    kws['color'] = 'w'
                    
                kws['linewidth'] = 2



    # set linestyle
    # =============
    if 'twoMom' in idname:
        kws['linestyle'] = '-'
        kws['alpha'] = 1.
    elif 'oneMom' in idname:
        kws['linestyle'] = '-'
        kws['alpha'] = 0.3
        
        

#        if '_Conv' in idname:
#            kws['fillstyle'] = 'full'
#        elif '_noConv' in idname:
#            kws['fillstyle'] = 'none'
#            kws['markeredgewidth'] = 1.5


    return kws

######################################################################
######################################################################



def get_exp_kws_lines_expname( expname ):

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


def get_exp_kws_points_expname( expname ):

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

def get_plotting_order( vlist, direct_id_input = True ):

    '''
    Define a static order in which all different experiments 
    are plotted.

    
    Parameters
    ----------
    vlist : list of str
        list of variable names (either expnames or idnames)

    direct_id_input : bool, optional, default = True
        if idnames are used (not expnames)


    Returns
    --------
    index_list : list of int
        list of indices of the different names
        e.g. [7, 1, 3] means 1st plot entry 7, then 1 and then 3
    '''
    
    if not direct_id_input:
        idlist = convert_explist2idlist( vlist )
    else:
        idlist = vlist
    
    index_list = []
    
   
    for res in ['2km', '5km', '10km', '20km', '40km', '80km']:
        for muphys in ['oneMom', 'twoMom']:
            for cpar in ['noConv', 'Conv']:
                
                idtest = '%s_%s_%s' % (res, muphys, cpar)
                
                try:
                    index_list +=[idlist.index(idtest)]
                except:
                    pass


    nlength = len( index_list ) + 2
    

    try:
        index_list.insert(nlength / 2, idlist.index( 'msevi-not_scaled' ))
    except:
        pass

    try:
        index_list.insert(nlength / 2, idlist.index( 'msevi-scaled' ))
    except:
        pass    

    return np.array( index_list )

######################################################################
######################################################################

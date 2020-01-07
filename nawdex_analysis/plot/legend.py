#!/usr/bin/env python

'''
Helper for plotting labels and legends.
'''

import pylab as pl

######################################################################
######################################################################

def legend_renamer( labels ):
    
    '''
    A function to rename labels for plotting them into a legend.
    
    
    Parameters
    ----------
    labels : list
        list of labels
        
        
    Returns
    -------
    newlabels : list
        list of new label name that have been replaced by a 
        map defined within the function
    '''
        
    newnames = {'msevi-not_scaled': 'OBS (uncorrected)',
                'msevi-scaled' : 'OBS',
                "2km_oneMom_noConv" : "ICON( 2.5km, * )",
                "2km_oneMom_shConv" : "ICON( 2.5km, *,  sCP )",
                "2km_oneMom_Conv" : "ICON( 2.5km, *,  CP )",
                "2km_twoMom_noConv" : "ICON( 2.5km, ** )",
                "2km_twoMom_shConv" : "ICON( 2.5km, **, sCP )",
                "2km_twoMom_Conv" : "ICON( 2.5km, **, CP )",
                "5km_oneMom_noConv" : "ICON( 5km, * )",
                "5km_oneMom_Conv" : "ICON( 5km, *,  CP )",
                "5km_twoMom_noConv" : "ICON( 5km, ** )",
                "5km_twoMom_Conv" : "ICON( 5km, **, CP )",
                "10km_oneMom_noConv" : "ICON( 10km, * )",
                "10km_oneMom_Conv" : "ICON( 10km, *,  CP )",
                "10km_twoMom_noConv" : "ICON( 10km, ** )",
                "10km_twoMom_Conv" : "ICON( 10km, **, CP )",
                "20km_oneMom_Conv" : "ICON( 20km, *,  CP )",
                "20km_twoMom_Conv" : "ICON( 20km, **, CP )",
                "40km_oneMom_Conv" : "ICON( 40km, *,  CP )",
                "40km_twoMom_Conv" : "ICON( 40km, **, CP )",
                "80km_oneMom_Conv" : "ICON( 80km, *,  CP )",
                "80km_twoMom_Conv" : "ICON( 80km, **, CP )",}
    

    #newnames = {'msevi-not_scaled': 'OBS (uncalibrated)','msevi-scaled' : 'OBS',}

    newlabels = labels[:]
    
    for vname in labels:
        try:
            mindex = labels.index( vname )
            newlabels[mindex] = newnames[vname]
        except:
            # label not in label map
            pass
        
    return newlabels


######################################################################
######################################################################


def plegend(**kwargs):
    
    '''
    Convenience function for easier legend plotting.
    
    
    Parameters
    ----------
    **kwargs : dict
        set of keywords forwarded to the pl.legend method
        
    
    Returns
    -------
    labels : list
        list of legend labels
    
    '''
    default_kwargs = dict( frameon = False, loc='center right', 
                           bbox_to_anchor=(1.5, 0.5), fontsize = 'small' )

    merged_kwargs = default_kwargs.copy()
    merged_kwargs.update( kwargs )
    
    handles, labels = pl.gca().get_legend_handles_labels()
    

    # put msevi on top
    order = range(len(labels))

    
    for vname in ['msevi-not_scaled', 'msevi-scaled', ]:
        if vname in labels:
            mindex = labels.index( vname )
            order.remove(mindex)
            order.insert(0, mindex)

    labels = legend_renamer( labels )

    pl.legend([handles[idx] for idx in order],[labels[idx] for idx in order], 
         **merged_kwargs )
    
    return labels



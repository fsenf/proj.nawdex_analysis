#!/usr/bin/env python


######################################################################
######################################################################

'''
Set of tools for IO of either obs or sim.
'''

######################################################################
######################################################################

import datetime

######################################################################
######################################################################

def convert_time(t):

    '''
    Utility converts between two time formats A->B or B->A: 
    

    Parameters
    ----------
    t : float or datetime object
        time 
        A = either float as %Y%m%d.%f where %f is fraction of the day
        B = datetime object


    Returns
    -------
    tout : datetime object or float
        time, counterpart to t
    '''

    t0 = datetime.datetime(1970, 1, 1)

    if type(t) == type(t0):

        tout = np.int( t.strftime('%Y%m%d') )
        date = datetime.datetime.strptime(str(tout), '%Y%m%d')

        dt = (t - date).total_seconds()
        frac =  dt / (24 * 3600)

        tout +=  frac
    else:
        
        date = np.int(t)
        frac = t - date

        tout = datetime.datetime.strptime(str(date), '%Y%m%d')
        tout += datetime.timedelta( days = frac )


    return tout
        


######################################################################
######################################################################

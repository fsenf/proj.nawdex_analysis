#!/usr/bin/env python
# coding: utf-8


'''
A module to calculate

* averages under certain selection conditions or binning intervals
* area-weighted averages of selected interval ranges (bin-wise)
'''
## Binning and averaging


######################################################################
######################################################################


import os, sys, copy, glob
import numpy as np

######################################################################
######################################################################


def area_fractions( a, selector, bins ):

    '''
    Calculates area fractions of variable values in certain intervals.

    
    Parameters
    ----------
    a : numpy array, 2dim
        grid box areas

    selector : numpy array, 2dim
        field that selects the variable mask

    bins : numpy array, 1dim
        set of values used for binning


    Returns
    --------
    afrac : numpy array, 1dim
        relative area fractions
    '''

    # calculate total area
    atot = 1. * a.sum()

    nbins = len(bins)
    afrac = np.zeros(( nbins - 1, ))

    # loop over bin intervals
    for i in range( nbins - 1 ):

        # get outer bin values
        b1 = bins[i]
        b2 = bins[i + 1]
    
        mask = (selector >= b1) & (selector < b2) 
        
        
        afrac[i] = a[mask].sum() / atot

    return afrac

######################################################################
######################################################################


def area_weighted_binwise_averages( v, a, selector, bins ):

    '''
    Calculates area fractions of variable values in certain intervals.

    
    Parameters
    ----------
    v : numpy array, 2dim
        variables field to be averaged

    a : numpy array, 2dim
        grid box areas

    selector : numpy array, 2dim
        field that selects the variable mask

    bins : numpy array, 1dim
        set of values used for binning


    Returns
    --------
    afrac : numpy array, 1dim
        relative area fractions
    '''

    # calculate total area
    atot = 1. * a.sum()

    # variable times area
    va = v * a
    
    # init ave field
    nbins = len(bins)
    v_ave = np.zeros(( nbins - 1, ))

    # loop over bin intervals
    for i in range( nbins - 1 ):

        # get outer bin values
        b1 = bins[i]
        b2 = bins[i + 1]
    
        mask = (selector >= b1) & (selector < b2) & np.isfinite( va ) & ~va.mask 
        
        v_ave[i] = va[mask].sum() / a[mask].sum()

    return np.ma.masked_invalid( v_ave )

######################################################################
######################################################################

import os


# some important variables
SEVIRI_cutout = ((114, 1118), (271, 3047))  # edge based region defintion

# center-and-width-based region defintion 
# !!!! CARE: must be consistent with SEVIRI_cutout !!!!
NWCSAF_region = ((617, 1660), (1004, 2776)) 

if 'altair' in os.environ['HOSTNAME'] :
    fdir = '/vols/talos/home/fabian/data/icon/nawdex/meteosat/'
    meteosat_georef_file = '%s/msevi-nawdex-20160923.nc' % fdir

else:  # assume mistral 
    fdir = '/pf/b/b380352/data/nawdex/meteosat/'
    meteosat_georef_file = '%s/msevi-nawdex-20160923.nc' % fdir

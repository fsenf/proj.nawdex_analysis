import os


# some important variables
SEVIRI_cutout = ((114, 1118), (271, 3047))  # edge based region defintion

# center-and-width-based region defintion 
# !!!! CARE: must be consistent with SEVIRI_cutout !!!!
NWCSAF_region = ((617, 1660), (1004, 2776)) 

if 'altair' in os.environ['HOSTNAME'] :
    nawdex_dir = '/vols/talos/home/fabian/data/icon/nawdex/'
    nawdex_meteosat_dir = '%s/meteosat/' % nawdex_dir
    meteosat_georef_file = '%s/msevi-nawdex-20160923.nc' % nawdex_meteosat_dir
    
    nawdex_regions_file = '%s/region_masks_for_msevi_nawdex.h5' % nawdex_dir


else:  # assume mistral 
    nawdex_dir = '/pf/b/b380352/data/nawdex/'
    nawdex_meteosat_dir = '%s/meteosat/' % nawdex_dir
    meteosat_georef_file = '%s/msevi-nawdex-20160923.nc' % nawdex_meteosat_dir

    nawdex_regions_file = '%s/region_masks_for_msevi_nawdex.h5' % nawdex_dir

    simulation_dir = '/work/bm0834/b380459/NAWDEX/ICON_OUTPUT_NWP'

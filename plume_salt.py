import tracpy
import tracpy.calcs
import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as netCDF

proj = tracpy.tools.make_proj('nwgom-pyproj')
loc = "http://barataria.tamu.edu:8080/thredds/dodsC/NcML/txla_hindcast_agg"
grid = tracpy.inout.readgrid(loc, proj, usespherical=True)



# miss_count = np.zeros(23)
# atch_count = np.zeros(23)
# trin_count = np.zeros(23)

miss_lon = {}
miss_lat = {}
miss_salt = {}

atch_lon = {}
atch_lat = {}
atch_salt = {}

trin_lon = {}
trin_lat = {}
trin_salt = {}

#tp = []

years = np.arange(1995,1996)
days = np.arange(1,15)
for i,year in enumerate(years):
    miss_lon[year] = []   # stored longitudes. keys are years
    miss_lat[year] = []
    atch_lon[year] = []
    atch_lat[year] = []
    trin_lon[year] = []
    trin_lat[year] = []
    
    miss_salt[year] = []
    atch_salt[year] = []
    trin_salt[year] = []
    
    for day in days:
        
        # Find all drifters for each day that pass through _________ river inlet
        
        fname = "tracks/%d/2d_July%d.nc" %(year,day)
        d = netCDF.Dataset(fname)
        lonp = d["lonp"][:]   # lonp[drifter,hour]
        latp = d["latp"][:]
        tp = d["tp"][:]
        miss = np.unique(np.argwhere((lonp < -88.7) & (lonp > -89.5) & (latp > 28.5) & (latp < 29.5))[:,0])
        atch = np.unique(np.argwhere((lonp < -90.5) & (lonp > -92) & (latp > 29) & (latp < 30))[:,0])
        trin = np.unique(np.argwhere((lonp < -94.5) & (lonp > -95.5) & (latp > 29) & (latp < 30))[:,0])
        braz = np.unique(np.argwhere((lonp < -94.5) & (lonp > -95.5) & (latp > 29) & (latp < 30))[:,0])
        
        # Count the drifters that pass through inlets
#         miss_count[i] += len(miss)
#         atch_count[i] += len(atch)
#         trin_count[i] += len(trin)
        
        ### Mississippi River
        for j in miss:
            
            ## For every drifter that goes past the Miss. river inlet, store the track
            ## If calculating salinity works, unsure of need for storing track
            
            # lonp[j] is drifter track
            miss_lon[year].append(lonp[j])
            miss_lat[year].append(latp[j])
            
            ## Calculate and store the salt of the track
            
            # eliminate where drifters have naned out (might be the problem)
            inan = np.isnan(lonp[j])
            
            # convert to grid space
            miss_i,miss_j,t = tracpy.tools.interpolate2d(lonp[j],latp[j], grid, 'd_ll2ij')
            
            miss_i[inan] = np.nan
            miss_j[inan] = np.nan
            salt = tracpy.calcs.Var(miss_i,miss_j,tp[0],"salt",netCDF.Dataset(loc) )
            # nan out known nan locations
            salt[inan] = np.nan

            miss_salt[year].append(salt)

np.savez("salt_test_wo_tp.npz", mlon=miss_lon, mlat=miss_lat, msalt=miss_salt)
            
            
#         ### Atchafalaya River
#         for j in atch:
            
#             # lonp[j] is drifter track
#             atch_lon[year].append(lonp[j])
#             atch_lat[year].append(latp[j])
            
#             ## Calculate and store the salt of the track
            
#             # eliminate where drifters have naned out (might be the problem)
#             inan = np.isnan(lonp[j])
            
#             # convert to grid space
#             atch_i,atch_j,t = tracpy.tools.interpolate2d(lonp[j],latp[j], grid, 'd_ll2ij')
            
#             atch_i[inan] = np.nan
#             atch_j[inan] = np.nan
#             salt = tracpy.calcs.Var(atch_i,atch_j,tp[0],"salt",netCDF.Dataset(loc) )
#             # nan out known nan locations
#             salt[inan] = np.nan

#             atch_salt[year].append(salt)
        
        
#         ### Trinity River (Galveston Bay inlet)
#         for j in trin:
            
#             # lonp[j] is drifter track
#             trin_lon[year].append(lonp[j])
#             trin_lat[year].append(latp[j])
            
#             ## Calculate and store the salt of the track
            
#             # eliminate where drifters have naned out (might be the problem)
#             inan = np.isnan(lonp[j])
            
#             # convert to grid space
#             trin_i,trin_j,t = tracpy.tools.interpolate2d(lonp[j],latp[j], grid, 'd_ll2ij')
            
#             trin_i[inan] = np.nan
#             trin_j[inan] = np.nan
#             salt = tracpy.calcs.Var(trin_i,trin_j,tp[0],"salt",netCDF.Dataset(loc) )
#             # nan out known nan locations
#             salt[inan] = np.nan

#             trin_salt[year].append(salt)


#fin = np.argwhere(~np.isnan(lonp[j]))
        
    # print("=================")
    # print("Total drifters for", year, len(miss_lon[year]))
    # print("Salt check", year, len(miss_salt[year]))
    # print("=================")
    
    # plt.scatter(miss_lon[year], miss_lat[year], c=miss_salt[year])
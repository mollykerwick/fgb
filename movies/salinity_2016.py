import numpy as np
import netCDF4 as nc
import datetime
import matplotlib.pyplot as plt
import tracpy.tools
import tracpy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmocean as cmo
import cartopy
import tracpy.plotting
from matplotlib import cm, colors
import time
import xarray






loc = "http://barataria.tamu.edu:8080/thredds/dodsC/NcML/txla_hindcast_agg"
proj = tracpy.tools.make_proj('nwgom-pyproj')
grid = tracpy.inout.readgrid(loc, proj, usespherical=True)



def dt2oceanindex(dt):
    '''
    Takes in datetime object, converts to epoch time, and returns ocean_time index
    '''
    epoch = time.mktime(dt.timetuple())
    index = (epoch - 725850000 - (6*3600)) / 3600
    return int(index)





days = np.arange(1,91)

ds = xarray.open_dataset( loc )

passed = 0      # keeps track of drifters that exit in time
seconds = 0     # used for accessing salt at that time

for day in days:
    date_day = datetime.datetime.fromtimestamp(1462165200 + seconds).day
    date_month = datetime.datetime.fromtimestamp(1462165200 + seconds).month

    # if July 1 drifters have ended
    if (day > 59):
        # Close file passed+1
        passed += 1


    for hour in range(24):
        dt = datetime.datetime(2016, date_month, date_day, hour, 0, 1)
        ind = dt2oceanindex(dt)
        
    ### plot background
        fig = plt.figure(dpi=300)
        fig.tight_layout()   

        ax = fig.add_subplot(111, projection=ccrs.Mercator())
        tracpy.plotting.background(grid, ax=ax, fig=fig, extent=[-98, -87.5, 22.8, 30.5],
                                   col='grey', halpha=0.1, outline=[1, 1, 0, 1], res='10m',
                                   fontsize=8,proj=ccrs.Mercator())

        ax.add_feature(cfeature.NaturalEarthFeature(category = 'physical', 
            name='rivers_lake_centerlines',scale='10m', edgecolor='navy', facecolor='none', linewidths=0.3))
        ax.add_feature(cfeature.NaturalEarthFeature(category = 'physical', 
            name='rivers_north_america', scale='10m', edgecolor='navy', facecolor='none', linewidths=0.3))

    ### plot salinity
        mp = ax.pcolormesh(ds["lon_rho"][:, :], ds["lat_rho"][:, :], ds["salt"][ind, 29, :, :], transform=ccrs.PlateCarree(),
                           norm=colors.PowerNorm(gamma=2), alpha=1, cmap=cmo.cm.haline, vmax=38, vmin=0)

    ### colorbar
        cax = fig.add_axes([0.38, 0.25, 0.415, 0.025]) #colorbar axes
        cb = fig.colorbar(mp, cax=cax, orientation='horizontal')
        cb.ax.set_xticks( np.linspace(0, 35, 8) )
        cb.ax.set_xticklabels( ["0", "", "10","15","20","25","30","35"], fontsize=7 )
        cb.ax.tick_params(labelsize=10, length=0, color='0.2', labelcolor='0.2')
        cb.set_label(r'Salinity $[g \cdot kg^{-1}]$')
        
    ### date
        string = "2016 %s %.02d %.02d:00" %(dt.strftime("%B")[:3], date_day, hour)
        ax.text(-93.93,25.2, string,
               fontsize=12, color='0.2', transform=ccrs.PlateCarree())
        
    ### plot drifters
        for drifter in range(passed+1, min(day+1, 32)):
            fname = "tracks/2016/2d_July%d.nc" %(drifter)
            dd = xarray.open_dataset( fname )
            idrift = ((day-drifter) * 24 +1 ) + (hour)
            ax.scatter( dd["lonp"][:,-idrift], dd["latp"][:,-idrift], marker="o",
                       edgecolors="black", facecolors="white", s=12, linewidths=0.7, transform=ccrs.PlateCarree() )
            

        fig.savefig( "movies/sal_drif_2016/image%.04d.png" %( (day*24) + hour - 24 ) )
        plt.close(fig)

    seconds += 24*3600
    



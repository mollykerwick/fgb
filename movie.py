import numpy as np
import netCDF4 as nc
import datetime
import time

import matplotlib.pyplot as plt
from matplotlib import cm, colors
import tracpy
import tracpy.tools
import tracpy.plotting
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmocean as cmo
import xarray


def dt2oceanindex(dt):
    '''
    Takes in datetime object, converts to epoch time, and returns ocean_time ROMS index
    '''
    epoch = time.mktime(dt.timetuple())
    index = (epoch - 725850000 - (5*3600)) / 3600
    return int(index)

def movie( start_date=1, loc=None, grid=None, salinity=False, depth=False, res="10m" ):
	if salinity:
		label = "salinity"
	else: label = "depth"

	days = np.arange(start_date,92)

	ds = xarray.open_dataset( loc )

	passed = abs( min( 62-start_date, 0 ) ) 
	            # tracks days after drifters start to die
	            # EXAMPLE:
	            #    if day == 65: passed == 5
	            #    60 day simulations have ended drifters ending July 1 through July 5
	seconds = 24*3600*(start_date-1)


	for day in days:
	    date = datetime.datetime.fromtimestamp(1462165200 + seconds)
	    date_day = date.day
	    date_month = date.month
	    
	    if (day > 61):    # if drifters initialized on July first have ended
	        passed += 1   # "close" file passed+1 (just don't open it)
	        
	    # if (passed == 0): print("no drifters have died")
	    # else: print("dead drifters:", passed)

	    for hour in range(24):
	        dt = datetime.datetime(2016, date_month, date_day, hour, 0, 1)
	        ind = dt2oceanindex(dt)
	        
	        ### plot background
	        fig = plt.figure(dpi=300)
	        fig.tight_layout()   
	        ax = fig.add_subplot(111, projection=ccrs.Mercator())
	        tracpy.plotting.background(grid, ax=ax, fig=fig, extent=[-98, -87.5, 22.8, 30.5],
	                                   col='grey', halpha=0.1, outline=[1, 1, 0, 1], res=res,
	                                   fontsize=8,proj=ccrs.Mercator(), hlevs=np.array( [100, 400] ))
	        ax.add_feature(cfeature.NaturalEarthFeature(category='physical', name='rivers_lake_centerlines',
	        							scale=res, edgecolor='navy', facecolor='none', linewidths=0.3))
	        ax.add_feature(cfeature.NaturalEarthFeature('physical', 'rivers_north_america', res, edgecolor='navy', 
	        							facecolor='none', linewidths=0.3))

	        ### add date label
	        string = "2016 %s %.02d %.02d:00" %(dt.strftime("%B")[:3], date_day, hour)
	        ax.text(-93.93,25.2, string,
	               fontsize=12, color='0.2', transform=ccrs.PlateCarree())
	        


	        if salinity:
		        ### plot salinity
		        mp = ax.pcolormesh( ds["lon_rho"][:, :], ds["lat_rho"][:, :], ds["salt"][ind, 29, :, :], transform=ccrs.PlateCarree(),
		                           norm=colors.PowerNorm(gamma=2), alpha=1, cmap=cmo.cm.haline, vmax=38, vmin=0)
		    

		        ### add colorbar
		        cax = fig.add_axes([0.38, 0.25, 0.415, 0.025]) #colorbar axes
		        cb = fig.colorbar(mp, cax=cax, orientation='horizontal')
		        cb.ax.set_xticks( np.linspace(0, 35, 8) )
		        cb.ax.set_xticklabels( ["0", "", "10","15","20","25","30","35"], fontsize=7 )
		        cb.ax.tick_params(labelsize=10, length=0, color='0.2', labelcolor='0.2')
		        cb.set_label(r'Salinity $[g \cdot kg^{-1}]$')
	        
	       
	        
	        ### plot all drifters that are alive
	        for drifter in range(passed+1, min(day+1, 32)):  # drifters that are alive on day
	            fname = "tracks/2016/2d_July%d.nc" %(drifter)
	            
	            dd = xarray.open_dataset( fname )
	            idrift = ((day-drifter) * 24 +1 ) + (hour)   # gets drifter's position at certain hour on certain day
	            if depth:
	            	drif = ax.scatter( dd["lonp"][412:,-idrift], dd["latp"][412:,-idrift], c=abs(dd["zp"][412:,-idrift]),\
	            					cmap=cmo.cm.deep, vmin=0, vmax=500, marker="o", edgecolors="black", s=12, linewidths=0.5, transform=ccrs.PlateCarree() )
	            	cax = fig.add_axes([0.38, 0.25, 0.415, 0.025])	#colorbar axes
		            cb = fig.colorbar(drif, cax=cax, orientation='horizontal')
		            cb.set_label("Depth")
		        else:
		            ax.scatter( dd["lonp"][:,-idrift], dd["latp"][:,-idrift], marker="o",
		                       edgecolors="black", facecolors="white", s=12, linewidths=0.5, transform=ccrs.PlateCarree() )
	            
	        
	        fig.savefig("movies/frames/" + label + "%.04d.png" %( (day*24) + hour - 24 ))
	        plt.close(fig)
	        
	    
	    seconds += 24*3600



if __name__ == "__main__":
	loc = "http://copano.tamu.edu:8080/thredds/dodsC/NcML/txla_hindcast_agg"
	proj = tracpy.tools.make_proj('nwgom-pyproj')
	grid = tracpy.inout.readgrid(loc, proj, usespherical=True)

	movie( start_date=91, loc=loc, grid=grid,
		 salinity=True, depth=False, res="10m")




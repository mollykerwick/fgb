#!/usr/bin/python3

import numpy as np
import netCDF4 as netCDF  # file format
import tracpy
import tracpy.plotting
from tracpy.tracpy_class import Tracpy
from itertools import compress  # seeing which drifters leave the domain
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import os
import matplotlib
import datetime
matplotlib.rcParams.update({'font.size': 20})


# Location of TXLA model output file and grid, on a thredds server
# ROMS model output 1/1/1994-1/1/2017
loc = 'http://barataria.tamu.edu:8080/thredds/dodsC/NcML/txla_hindcast_agg'

# Time units
time_units = 'seconds since 1970-01-01'
proj = tracpy.tools.make_proj('nwgom-pyproj')   # projection object

ndays = 60
tseas = 3600
time_units = 'seconds since 1970-01-01'
nsteps = 5
N = 1
ff = -1
ah = 0.
av = 0.
doturb = 0
# 2d
do3d = 0
z0 = 's' 
num_layers = 30
zpar = num_layers-1
# # 3d
# do3d = 1
# z0 = np.zeros(681)
# num_layers = 30
# zpar = 'fromZeta'

# SETUP FOR SIMULATION

# 50 SURFACE DRIFTERS
# lon0, lat0 = np.meshgrid(np.linspace(-94,-93.7,10), \
#                             np.linspace(27.8,28,10)) # whole domain, 20 km

################### Multi-year simulation ###################






years = np.arange(1994,2017)

for year in years:
    month = 7     # July
    days = np.arange(1,32)#   for all 31 days in July
    for day in days:
	date = datetime.datetime(year, month, day, 0)
        name = '%dJuly%d' %(day,year)   # 27July2005
        if not os.path.exists('tracks/' + name + '.nc') and \
                    not os.path.exists('tracks/' + name + 'gc.nc'):
            print(day)
	    grid = tracpy.inout.readgrid(loc, proj, usespherical=True)
            tp = Tracpy(loc, grid, name=name, tseas=tseas, ndays=ndays, nsteps=nsteps,
                        N=N, ff=ff, ah=ah, av=av, doturb=doturb, do3d=do3d, z0=z0, zpar=zpar, time_units=time_units)
            # evenly spaced surface drifters
            dx = 1000  # in meters
            lonsink, latsink = -93.72595, 27.902   # exactly in between outer boundaries of banks from fgb website
            llcrnrlon = lonsink - 0.2
            urcrnrlon = lonsink + 0.2
            llcrnrlat = latsink - 0.12
            urcrnrlat = latsink + 0.12
            xcrnrs, ycrnrs = tp.grid.proj([llcrnrlon, urcrnrlon], [llcrnrlat, urcrnrlat]) 
            X, Y = np.meshgrid(np.arange(xcrnrs[0], xcrnrs[1], dx), np.arange(ycrnrs[0], ycrnrs[1], dx)) 
            lon0, lat0 = tp.grid.proj(X, Y, inverse=True)
            lon0, lat0 = tracpy.tools.check_points(lon0, lat0, tp.grid)
            lonp, latp, zp, t, T0, U, V = tracpy.run.run(tp, date, lon0, lat0) 












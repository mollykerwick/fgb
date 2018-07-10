#!/usr/bin/python3

import numpy as np
import netCDF4 as netCDF	# file format
import tracpy
import tracpy.plotting
from tracpy.tracpy_class import Tracpy
from itertools import compress	# seeing which drifters leave the domain
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import os
import matplotlib
import datetime
import sys
matplotlib.rcParams.update({'font.size': 20})


# Location of TXLA model output file and grid, on a thredds server
# ROMS model output 1/1/1994-1/1/2017
loc = "http://copano.tamu.edu:8080/thredds/dodsC/NcML/txla_hindcast_agg"

# Time units
time_units = 'seconds since 1970-01-01'
proj = tracpy.tools.make_proj('nwgom-pyproj')	 # projection object

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

################### Multi-year simulation ###################




grid = tracpy.inout.readgrid(loc, proj, usespherical=True)


## East Bank
# N: 27.98399444
# E: -93.57083333
# S: 27.88140000
# W: -93.64472222       
elon, elat = (-93.57083333-93.64472222) / 2. , (27.98399444+27.88140000) / 2.
elonrange = max( abs( abs(elon)-93.57083333 ), abs( abs(elon)-93.64472222 ) )
elatrange = max( abs( abs(elat)-27.98399444 ), abs( abs(elat)-27.88140000 ) )
elonlow = elon - elonrange
elonupp = elon + elonrange
elatlow = elat - elatrange
elatupp = elat + elatrange

## West Bank
# N: 27.91719722
# E: -93.78055556
# S: 27.81976111
# W: -93.88111111
wlon, wlat = (-93.78055556-93.88111111) / 2. , (27.91719722+27.81976111) / 2.
wlonrange = max( abs( abs(wlon)-93.78055556 ), abs( abs(wlon)-93.88111111 ) )
wlatrange = max( abs( abs(wlat)-27.91719722 ), abs( abs(wlat)-27.81976111 ) )
wlonlow = wlon - wlonrange
wlonupp = wlon + wlonrange
wlatlow = wlat - wlatrange
wlatupp = wlat + wlatrange

dx = 1000  # drifter spacing in meters 
ex, ey = proj([elonlow, elonupp], [elatlow, elatupp])
eX, eY = np.meshgrid(np.arange(ex[0], ex[1], dx), np.arange(ey[0], ey[1], dx))

wx, wy = proj([wlonlow, wlonupp], [wlatlow, wlatupp])
wX, wY = np.meshgrid(np.arange(wx[0], wx[1], dx), np.arange(wy[0], wy[1], dx))

ewX = np.append(eX,wX)
ewY = np.append(eY,wY)



year = int(sys.argv[1:][0])

month = 7	 # July
days = np.arange(1,32)
for day in days:
    date = datetime.datetime(year, month, day, 0)
    name = "2d_July%d" %(day) # 2d_July5
    if not os.path.exists("tracks/" + name + '.nc') and not os.path.exists("tracks/" + name + 'gc.nc'):
        if not os.path.exists("tracks/" + str(year) + "/" + name + '.nc') and not os.path.exists("tracks/" + str(year) + "/" + name + 'gc.nc'):
            os.makedirs("tracks/" + str(year) ,exist_ok=True)
            Name = str(year) + "/" + name

            print(day)
            tp = Tracpy(loc, grid, name=Name, tseas=tseas, ndays=ndays, nsteps=nsteps,N=N, ff=ff, ah=ah, av=av, doturb=doturb, do3d=do3d, z0=z0, zpar=zpar, time_units=time_units)

            lon0, lat0 = tp.grid.proj(ewX, ewY, inverse=True)
            lon0, lat0 = tracpy.tools.check_points(lon0, lat0, tp.grid)
            lonp, latp, zp, t, T0, U, V = tracpy.run.run(tp, date, lon0, lat0) 












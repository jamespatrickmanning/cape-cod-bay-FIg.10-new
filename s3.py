# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 20:59:48 2018

@author: xiaojian
"""
import sys
import datetime as dt
from matplotlib.path import Path
import netCDF4
from dateutil.parser import parse
import numpy as np
import math
import pandas as pd
from datetime import datetime, timedelta
from math import radians, cos, sin, atan, sqrt  
from matplotlib.dates import date2num,num2date

time0=datetime(1858,11,17,00,00,00)
time1=datetime(2014,12,26,00,00,00)
time2=datetime(2014,12,27,00,00,00)

d1 = (time1 - datetime(1858,11,17)).total_seconds()/86400 
d2 = (time2 - datetime(1858,11,17)).total_seconds()/86400
url='''http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Archive/NECOFS_MASS_BAY/2014/mbn_201412.nc?lon[0:1:98431],lat[0:1:98431],time[0:1:743],temp[0:1:743][0:1:9][0:1:98431]'''
#ds = netCDF4.Dataset('''mbn_201411.nc''','r').variables
ds = netCDF4.Dataset(url,'r').variables

time=ds['time'][:].tolist()
#time=np.load('time.npy')
index1=np.argmin(abs(np.array(time)-d1))
index2=np.argmin(abs(np.array(time)-d2))

print time0+timedelta(hours=time[index1]*24)#=np.argmin(abs(time-d1))*24)
print time0+timedelta(hours=time[index2]*24)#=np.argmin(abs(time-d1))*24)


print 'index1,index2',index1,index2


lon=ds['lon'][:].tolist()
lat=ds['lat'][:].tolist()

n=[]
for a in np.arange(len(lon)):
    if lon[a]>=-70.75 and lon[a]<=-69.8 and lat[a]>=41.5 and lat[a]<=42.23:
        n.append(a)
us=[]
#vs=[]
u=[]
for a in np.arange(index1,index2,1):
    print a
    '''
    for b in np.arange(len(n)):
        u=[]
        #v=[]
        print 'b,a',b,a
    '''
    u.append(ds['temp'][a][0][:])
        #v.append(ds['v'][a][0][n[b]])
w=[]
for a in np.arange(len(u)):
    print '###',a
    w1=[]
    for b in np.arange(len(n)): 
        w1.append(u[a][n[b]])
    w.append(w1)

lo=[]
la=[]
for a in np.arange(len(n)):
    lo.append(lon[n[a]])
    la.append(lat[n[a]])
np.save('low',lo)
np.save('law',la)

np.save('w12_26',w)
#np.save('w0_300',vs)


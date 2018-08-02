# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 20:59:48 2018
WHAT IS THE PURPOSE OF THIS PROGRAM BRIEFLY?
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

urltime='''http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Archive/NECOFS_GOM_WAVE/gom3v7_201411.nc?lonc[0:1:90997],latc[0:1:90997],time[0:1:719],uwind_speed[0:1:719][0:1:90997],vwind_speed[0:1:719][0:1:90997]'''
url='''http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Archive/NECOFS_GOM_WAVE/gom3v7_201411.nc?lonc[0:1:90997],latc[0:1:90997],time[0:1:719],uwind_speed[0:1:719][0:1:90997],vwind_speed[0:1:719][0:1:90997]'''
time0=datetime(1858,11,17,00,00,00)
time1=datetime(2014,11,18,00,00,00) # YOU ARE OUTPUTING 0-30 or 18-23?
time2=datetime(2014,11,23,00,00,00)

d1 = (time1 - datetime(1858,11,17)).total_seconds()/86400 
d2 = (time2 - datetime(1858,11,17)).total_seconds()/86400
"""
d2=(time2-time0).days+(time2-time0).seconds/(60*60*24)
d1=(time1-time0).days+(time1-time0).seconds/(60*60*24)

"""
'''
ds = netCDF4.Dataset(urltime,'r').variables

np.save('time',ds['time'][:])
np.save('lonc',ds['lonc'][:])
np.save('latc',ds['latc'][:])
'''
time=np.load('time.npy')
index1=np.argmin(abs(time-d1))
index2=np.argmin(abs(time-d2))

#print time0+timedelta(hours=time[index1]*24)#=np.argmin(abs(time-d1))*24)
#print time0+timedelta(hours=time[index2]*24)#=np.argmin(abs(time-d1))*24)
index1=0
index2=len(time)-1

print 'index1,index2',index1,index2
print time0+timedelta(hours=time[index1]*24)#=np.argmin(abs(time-d1))*24)
print time0+timedelta(hours=time[index2]*24)#=np.argmin(abs(time-d1))*24)

lon=np.load('lonc.npy')
lat=np.load('latc.npy')

n=[]
for a in np.arange(len(lon)):
    if lon[a]>=-70.75 and lon[a]<=-69.8 and lat[a]>=41.5 and lat[a]<=42.23:
        n.append(a)
ds = netCDF4.Dataset('''gom3v7_201411.nc''','r').variables
us=[]
vs=[]
'''
for b in np.arange(len(n)):
    u=[]
    v=[]
'''
u=[]
v=[]
for a in np.arange(index1,index2+1,1):
    print 'b,a',a
    u.append(ds['uwind_speed'][a][:])
    v.append(ds['vwind_speed'][a][:])
#    us.append(u)
#    vs.append(v)
np.save('uf',u)
np.save('vf',v)

for b in np.arange(len(n)):
    u1=[]
    v1=[]


    for a in np.arange(index1,index2+1,1):
        print 'x',b,a
        u1.append(u[a][n[b]])
        v1.append(v[a][n[b]])
    us.append(u1)
    vs.append(v1)
lo=[]
la=[]
for a in np.arange(len(n)):
    lo.append(lon[n[a]])
    la.append(lat[n[a]])
np.save('lo0_30',lo)
np.save('la0_30',la)
np.save('us0_30',us)
np.save('vs0_30',vs)

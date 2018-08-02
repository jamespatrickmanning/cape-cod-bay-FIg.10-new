# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 11:05:54 2018

@author: xiaojian
"""
from mpl_toolkits.basemap import Basemap  
import sys

from matplotlib.patches import Ellipse, Circle
import matplotlib.pyplot as plt
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

lo=np.load('lo18_23.npy')
la=np.load('la18_23.npy')
us=np.load('us18_23.npy')
vs=np.load('vs18_23.npy')
ff=500
x=lo
y=la
xi = np.arange(-70.75,-69.80000,0.05)
yi = np.arange(41.5,42.250000,0.05)
dr=dict(lon=[],lat=[],us=[],vs=[])
########################################################################
for a in np.arange(len(x)):
    print 'a',a
    for b in np.arange(len(xi)-1):
        for c in np.arange(len(yi)-1):
            if x[a]>=xi[b] and x[a]<xi[b+1] and y[a]>=yi[c] and y[a]<yi[c+1]:
                d='%s'%a+'%s'%b
                
                dr['lon'].append((xi[b]+xi[b+1])/2.0)
                dr['lat'].append((yi[c]+yi[c+1])/2.0)
                dr['us'].append(us[a])
                dr['vs'].append(vs[a])
                
####################################################################
lonlat=[]
ud=[]
vd=[]
lonz=[]
latz=[]
###################################################################
for a in np.arange(len(dr['lon'])):
    if "%s+%s"%(dr['lon'][a],dr['lat'][a]) not in lonlat:
        
        lonlat.append("%s+%s"%(dr['lon'][a],dr['lat'][a]))
        #lat.append(dr['lat'][a])
for a in np.arange(len(lonlat)):
    u=[]
    v=[]
    
    for b in np.arange(len(dr['lon'])):
        if "%s+%s"%(dr['lon'][b],dr['lat'][b])==lonlat[a]:
            
            for c in np.arange(len(dr['us'][b])):
                u.append(dr['us'][b][c])
                v.append(dr['vs'][b][c])
    ud.append(u)
    vd.append(v)
#########################################################################
fig = plt.figure(figsize=(15,12))
ax = fig.add_subplot(1,2,1)   
####################################################3
for a in np.arange(len(ud)):
    xie=np.cov(ud[a],vd[a])
    qxx=xie[0][0]
    qxy=xie[0][1]
    qyy=xie[1][1]
    st_2=math.atan(2*qxy/(qxx-qyy))
    st=st_2/2
    #dtd=st/(math.pi/180)
    rx=qxx*math.cos(st)*math.cos(st)+qyy*math.sin(st)*math.sin(st)+qxy*math.sin(st_2)
    ry=qxx*math.sin(st)*math.sin(st)+qyy*math.cos(st)*math.cos(st)-qxy*math.sin(st_2)
    dirr=[]
    if qxy>=0:
        print 'max=1,3'
        dirr.append(1)
        dirr.append(3)
        
    else:
        print 'max=2,4'
        dirr.append(2)
        dirr.append(4)
    if rx>=ry:
        ma=rx
        mi=ry
    else:
        ma=ry
        mi=rx
    
    f=[st,st+math.pi/2,st+math.pi,st+math.pi*3/2]
    f=0
    if st_2>=0:
        f=1
    if st_2<0:
        f=4
    dr=dict(d=[],df=[],x=[],xf=[])
    p=[]
    if f in dirr:
        dr['d'].append(ma)
        dr['df'].append(st)
        dr['x'].append(mi)
        dr['xf'].append(st+math.pi/2)
        #,ma,st+math.pi/2,mi,f)
    else:
        p.append(1)
        dr['d'].append(ma)
        dr['df'].append(st+math.pi/2)
        dr['x'].append(mi)
        dr['xf'].append(st)
    
    
    
    if p!=[]:
        print 1
        ell1 = Ellipse(xy = (float(lonlat[a][0:7]), float(lonlat[a][8:14])), width = dr['x'][0]/ff, height = dr['d'][0]/ff, angle = dr['xf'][0]/(math.pi/2/180), facecolor= 'red', alpha=1)
        #ax.plot([float(lonlat[a][0:7],],[float(lonlat[a][8:14]),])
        print 'width',dr['x'][0]/ff
    else:
        ell1 = Ellipse(xy = (float(lonlat[a][0:7]), float(lonlat[a][8:14])), width = dr['d'][0]/ff, height = dr['x'][0]/ff, angle = dr['df'][0]/(math.pi/2/180), facecolor= 'red', alpha=1)
        
        #ells = [Ellipse((float(lonlat[a][0:7]), float(lonlat[a][8:14])), int(dr['d'][0])/680, int(dr['x'][0])/680, dr['df'][0]/(math.pi/2/180)) for a in angles]
    
    ax.add_patch(ell1)
     

ax.set_title('a the mean wind vector with a variance ellipse')
ax.plot([-69.92,-69.87],[41.8,41.8],color='black')
ax.plot([-69.92,-69.92],[41.8,41.81],color='black')
ax.plot([-69.87,-69.87],[41.8,41.81],color='black')
ax.text(-69.94,41.83,'''25(m/s)^2''')
m = Basemap(projection='cyl',llcrnrlat=41.5,urcrnrlat=42.2,\
            llcrnrlon=-70.75,urcrnrlon=-69.8,resolution='h')#,fix_aspect=False)
    #  draw coastlines
m.drawcoastlines()
m.ax=ax
m.fillcontinents(color='grey',alpha=1,zorder=2)
m.drawmapboundary()
#draw major rivers
#m.drawrivers()
parallels = np.arange(41.5,42.2,0.1)
m.drawparallels(parallels,labels=[1,0,0,0],dashes=[1,1000],fontsize=10,zorder=0)
meridians = np.arange(-70.75,-69.8,0.2)
m.drawmeridians(meridians,labels=[0,0,0,1],dashes=[1,1000],fontsize=10,zorder=0)


'''
#####################################################################################
'''

#lo=np.load('lombx.npy')
#la=np.load('lambx.npy')
#umb18_23=np.load('umb18_23.npy')
#vmb18_23=np.load('vmb18_23.npy')

lo=np.load('lombx.npy')
la=np.load('lambx.npy')
us1=np.load('umb18_23.npy')
vs1=np.load('vmb18_23.npy')
ff=1.0
x=lo
y=la
xi = np.arange(-70.75,-69.80000,0.05)
yi = np.arange(41.5,42.250000,0.05)
dr=dict(lon=[],lat=[],us=[],vs=[])
########################################################################
for a in np.arange(len(x)):
    print 'a',a
    for b in np.arange(len(xi)-1):
        for c in np.arange(len(yi)-1):
            if x[a]>=xi[b] and x[a]<xi[b+1] and y[a]>=yi[c] and y[a]<yi[c+1]:
                d='%s'%a+'%s'%b
                
                dr['lon'].append((xi[b]+xi[b+1])/2.0)
                dr['lat'].append((yi[c]+yi[c+1])/2.0)
                dr['us'].append(us1[a])
                dr['vs'].append(vs1[a])
                
########################################################################
lonlat=[]
ud=[]
vd=[]
lonz=[]
latz=[]
#####################################################################
for a in np.arange(len(dr['lon'])):
    if "%s+%s"%(dr['lon'][a],dr['lat'][a]) not in lonlat:
        
        lonlat.append("%s+%s"%(dr['lon'][a],dr['lat'][a]))
        #lat.append(dr['lat'][a])
for a in np.arange(len(lonlat)):
    u=[]
    v=[]
    
    for b in np.arange(len(dr['lon'])):
        if "%s+%s"%(dr['lon'][b],dr['lat'][b])==lonlat[a]:
            
            for c in np.arange(len(dr['us'][b])):
                u.append(dr['us'][b][c])
                v.append(dr['vs'][b][c])
    ud.append(u)
    vd.append(v)
####################################################
ax = fig.add_subplot(1,2,2)
wid=[]
heigth=[]
####################################################
for a in np.arange(len(ud)):
    xie=np.cov(ud[a],vd[a])
    qxx=xie[0][0]
    qxy=xie[0][1]
    qyy=xie[1][1]
    st_2=math.atan(2*qxy/(qxx-qyy))
    st=st_2/2
    
    #dtd=st/(math.pi/180)
    
    rx=qxx*math.cos(st)*math.cos(st)+qyy*math.sin(st)*math.sin(st)+qxy*math.sin(st_2)
    ry=qxx*math.sin(st)*math.sin(st)+qyy*math.cos(st)*math.cos(st)-qxy*math.sin(st_2)
    dirr=[]
    if qxy>=0:
        print 'max=1,3'
        dirr.append(1)
        dirr.append(3)
        
    else:
        print 'max=2,4'
        dirr.append(2)
        dirr.append(4)
    if rx>=ry:
        ma=rx
        mi=ry
    else:
        ma=ry
        mi=rx
    
    f=[st,st+math.pi/2,st+math.pi,st+math.pi*3/2]
    f=0
    if st_2>=0:
        f=1
    if st_2<0:
        f=4
    dr=dict(d=[],df=[],x=[],xf=[])
    p=[]
    if f in dirr:
        dr['d'].append(ma)
        dr['df'].append(st)
        dr['x'].append(mi)
        dr['xf'].append(st+math.pi/2)
        #,ma,st+math.pi/2,mi,f)
    else:
        p.append(1)
        dr['d'].append(ma)
        dr['df'].append(st+math.pi/2)
        dr['x'].append(mi)
        dr['xf'].append(st)
    
    
    
    #ells = [Ellipse((1, 1), int(dr['d'][0]), int(dr['x'][0]), dr['df'][0]/(math.pi/2/180)) for a in angles]
    if p!=[]:
        print 1
        if  dr['d'][0]/ff>0.1 or dr['x'][0]/ff>0.1:#066401115712580779:
            pass
        else:
            ell1 = Ellipse(xy = (float(lonlat[a][0:7]), float(lonlat[a][8:14])), width = dr['x'][0]/ff, height = dr['d'][0]/ff, angle = dr['xf'][0]/(math.pi/2/180), facecolor= 'red', alpha=1)
            #ax.plot([float(lonlat[a][0:7],],[float(lonlat[a][8:14]),])
            print 'width',dr['x'][0]/ff
            wid.append(dr['d'][0]/ff)
            heigth.append(dr['x'][0]/ff)
    else:
        if  dr['d'][0]/ff>0.1 or dr['x'][0]/ff>0.1:
            pass
        else:
            ell1 = Ellipse(xy = (float(lonlat[a][0:7]), float(lonlat[a][8:14])), width = dr['d'][0]/ff, height = dr['x'][0]/ff, angle = dr['df'][0]/(math.pi/2/180), facecolor= 'red', alpha=1)
            #wid.append(dr['d'][0]/ff)
            #heigth.append(dr['x'][0]/ff)
            #ells = [Ellipse((float(lonlat[a][0:7]), float(lonlat[a][8:14])), int(dr['d'][0])/680, int(dr['x'][0])/680, dr['df'][0]/(math.pi/2/180)) for a in angles]
    try:
    
        ax.add_patch(ell1)
    except:
        continue
ax.plot([-69.92,-69.87],[41.8,41.8],color='black')
ax.plot([-69.92,-69.92],[41.8,41.81],color='black')
ax.plot([-69.87,-69.87],[41.8,41.81],color='black')
ax.text(-69.95,41.83,'''0.05(m/s)^2''')

ax.set_title('b the mean ocean vector with a variance ellipse')
m = Basemap(projection='cyl',llcrnrlat=41.5,urcrnrlat=42.2,\
            llcrnrlon=-70.75,urcrnrlon=-69.8,resolution='h')#,fix_aspect=False)
    #  draw coastlines
m.drawcoastlines()
m.ax=ax
m.fillcontinents(color='grey',alpha=1,zorder=2)
m.drawmapboundary()
#draw major rivers
#m.drawrivers()
parallels = np.arange(41.5,42.2,0.1)
m.drawparallels(parallels,labels=[1,0,0,0],dashes=[1,1000],fontsize=10,zorder=0)
meridians = np.arange(-70.75,-69.8,0.2)
m.drawmeridians(meridians,labels=[0,0,0,1],dashes=[1,1000],fontsize=10,zorder=0)

plt.xlim(-70.75,-69.80000)
plt.ylim(41.5,42.250000)
plt.savefig('spxxxxxxx',dpi=300,bbox_inches='tight')
plt.show()



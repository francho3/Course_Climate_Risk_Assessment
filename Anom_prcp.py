#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cartopy.crs as ccrs # for geographic plotting
import cartopy.feature as cfeature
from IPython.display import Image
import xarray as xr
import xclim as xc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import xclim as xc
import xarray as xr
from matplotlib.cm import get_cmap
from scipy import stats
from scipy.stats import t


# In[2]:


#pr_file = '/lhome/cra2022/climriskdata/EUR-11/MPI-M-MPI-ESM-LR_MPI-CSC-REMO2009_v1/historical/pr/pr_EUR-11_MPI-M-MPI-ESM-LR_historical_r1i1p1_MPI-CSC-REMO2009_v1_day_19710101-20001231_LL.nc'
pr_file = '/lhome/cra2022/climriskdata/EUR-11/ICHEC-EC-EARTH_CLMcom-CCLM4-8-17_v1/historical/pr/pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_19710101-20001231_LL.nc'

ds_pr = xr.open_dataset(pr_file)

pr_file85 = '/lhome/cra2022/climriskdata/EUR-11/ICHEC-EC-EARTH_CLMcom-CCLM4-8-17_v1/rcp85/pr/pr_EUR-11_ICHEC-EC-EARTH_rcp85_r12i1p1_CLMcom-CCLM4-8-17_v1_day_20710101-21001231_LL.nc'

ds_pr85 = xr.open_dataset(pr_file85)

ds_pr85


# In[3]:


pr_mm85 = ds_pr85.pr * 86400
pr_mm85.attrs['units'] = 'mm/day'
prcp_7100_85 = pr_mm85.sel(lat=slice(30,45))


# In[4]:


del ds_pr85


# In[5]:


pr_mm = ds_pr.pr * 86400
pr_mm.attrs['units'] = 'mm/day'
prcp_7100 = pr_mm.sel(lat=slice(30,45))


# In[6]:


del ds_pr


# In[7]:


mon_prcp_7100_85= prcp_7100_85.resample(time = 'M').sum()

mon_clim_rcp85 = mon_prcp_7100_85.groupby('time.month')

mon_mean_clim_rcp85 = mon_clim_rcp85.mean('time')


# In[8]:


season_prcp_7100_rcp85 = mon_prcp_7100_85.groupby('time.season')

season_mean_prcp_7100_rcp85 = season_prcp_7100_rcp85.sum('time')/30

season_var_prcp_7100_rcp85 = season_mean_prcp_7100_rcp85.var('season')


# In[9]:


clim_prcp_7100_85 = mon_prcp_7100_85.sum('time')/30


# In[10]:


del prcp_7100_85


# In[11]:


mon_prcp_7100= prcp_7100.resample(time = 'M').sum()


# In[12]:


clim_prcp_7100 = mon_prcp_7100.sum('time')/30

mon_clim = mon_prcp_7100.groupby('time.month')

mon_mean_clim = mon_clim.mean('time')


# In[13]:


season_prcp_7100 = mon_prcp_7100.groupby('time.season')

season_mean_prcp_7100 = season_prcp_7100.sum('time')/30

season_var_prcp_7100 = season_mean_prcp_7100.var('season')


# In[14]:


del prcp_7100


# In[25]:


season_var_prcp_7100


# In[36]:


anom_prcp = clim_prcp_7100_85 - clim_prcp_7100

anom_prcp_percentage = (anom_prcp/clim_prcp_7100)*100

anom_var_prcp = season_var_prcp_7100_rcp85 - season_var_prcp_7100

r_prcp = xr.corr(anom_prcp,anom_var_prcp)

n = 151*471

t0 = r_prcp * np.sqrt((n-2)/(1 - r_prcp**2))

n


# In[39]:


anom_var_prcp


# In[37]:


r_prcp


# In[38]:


t0


# In[18]:


ds_pop = xr.open_dataset('/lhome/cra2022/climriskdata/EUR-11S/Estimated_population/Estimated_population_2093_LL.nc')
ds_pop_medi = ds_pop.sel(lat=slice(30,45))


# In[19]:


col_map = get_cmap("BrBG").copy()
#col_map.set_under("white")
anom_precip_levels = np.arange(-50,50,10)

fig = plt.figure(figsize=(30,10))
ax = plt.axes(projection=ccrs.PlateCarree())


#Include a ready-to-use colormap with cmap=<colormap_name>
a = anom_prcp.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), cmap=col_map, levels = anom_precip_levels, add_colorbar=False)
d = ds_pop_medi.population.plot.contourf(ax=ax, transform=ccrs.PlateCarree(),levels=[0,500000], colors='none', hatches=['','+++'], add_colorbar=False)

# Hatch color has to be changed afterwards has edgecolor
d.collections[1].set_edgecolor('Black')

# Add a contour for clarity
ds_pop_medi.population.plot.contour(ax=ax, transform=ccrs.PlateCarree(), levels=[500000], colors = 'Black', linewidths=1, add_colorbar=False)

ax.add_feature(cfeature.COASTLINE, linestyle='-')
ax.add_feature(cfeature.BORDERS, linestyle=':');
ax.add_feature(cfeature.OCEAN, zorder=10)

cbar = fig.colorbar(a, ax=ax, fraction = 0.1, label=r'liters per year (mm)')
cbar.ax.tick_params(labelsize=15)
cbar.set_label("Liters per year (mm)", size=18)

gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='white', alpha=0.5, linestyle='--', zorder=11)
gl.top_labels = False # suppress gridline labels on the top
gl.right_labels = False # suppress gridline labels at the right edge

ax.set_title('')
#ax.set_title('Time:{}'.format(nice_time), loc='right');
ax.set_title('Anomaly of Precipitation (1971 - 2000  & 2071 - 2100) with populated areas (> 500k) in 2093', fontsize=24)
plt.savefig("/lhome/cra2022/l.quirino.2_2022/Quirino_Leonardo/Project/ANOMPrecip_Pop.png", dpi = 300, bbox_inches="tight",pad_inches=0)


# In[20]:


plt.close()


# In[21]:


col_map1 = get_cmap("PiYG").copy()
#col_map1.set_under("white")
anom_var_levels = np.arange(-2000,2000,500)

fig = plt.figure(figsize=(30,10))
ax = plt.axes(projection=ccrs.PlateCarree())

#Include a ready-to-use colormap with cmap=<colormap_name>
a1 = (anom_var_prcp).plot.contourf(ax=ax, transform=ccrs.PlateCarree(), levels=anom_var_levels, cmap=col_map1, add_colorbar=False)
d = ds_pop_medi.population.plot.contourf(ax=ax, transform=ccrs.PlateCarree(),levels=[0,500000], colors='none', hatches=['','+++'], add_colorbar=False)

# Hatch color has to be changed afterwards has edgecolor
d.collections[1].set_edgecolor('Black')

# Add a contour for clarity
ds_pop_medi.population.plot.contour(ax=ax, transform=ccrs.PlateCarree(), levels=[500000], colors = 'Black', linewidths=1, add_colorbar=False)

ax.add_feature(cfeature.COASTLINE, linestyle='-')
ax.add_feature(cfeature.BORDERS, linestyle=':');
ax.add_feature(cfeature.OCEAN, zorder=10)

cbar1 = fig.colorbar(a1, ax=ax, fraction = 0.1, label=r'Montly Variance')
cbar1.ax.tick_params(labelsize=15)
cbar1.set_label("Montly Variance", size=18)

gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='white', alpha=0.5, linestyle='--', zorder=11)

gl.top_labels = False # suppress gridline labels on the top
gl.right_labels = False # suppress gridline labels at the right edge

ax.set_title('')
#ax.set_title('Time:{}'.format(nice_time), loc='right');
ax.set_title('Seasonal Variance Anomaly of Precipitation (1971 - 2000 & 2071 - 2100) with populated areas (> 500k) in 2020', fontsize=24)
plt.savefig("/lhome/cra2022/l.quirino.2_2022/Quirino_Leonardo/Project/SeasonalVarAnomPrecip_Pop_2093.png", dpi = 300, bbox_inches="tight",pad_inches=0)


# In[22]:


plt.close()


# In[23]:


col_map = get_cmap("BrBG").copy()
#col_map.set_under("white")
anom_precip_levels = np.arange(-50,50,10)

fig = plt.figure(figsize=(30,10))
ax = plt.axes(projection=ccrs.PlateCarree())


#Include a ready-to-use colormap with cmap=<colormap_name>
a = anom_prcp_percentage.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), cmap=col_map, levels = anom_precip_levels, add_colorbar=False)
d = ds_pop_medi.population.plot.contourf(ax=ax, transform=ccrs.PlateCarree(),levels=[0,500000], colors='none', hatches=['','+++'], add_colorbar=False)

# Hatch color has to be changed afterwards has edgecolor
d.collections[1].set_edgecolor('Black')

# Add a contour for clarity
ds_pop_medi.population.plot.contour(ax=ax, transform=ccrs.PlateCarree(), levels=[500000], colors = 'Black', linewidths=1, add_colorbar=False)

ax.add_feature(cfeature.COASTLINE, linestyle='-')
ax.add_feature(cfeature.BORDERS, linestyle=':');
ax.add_feature(cfeature.OCEAN, zorder=10)

cbar = fig.colorbar(a, ax=ax, fraction = 0.1, label=r'%', format='%.1f')
#cbar.ax.tick_params(labelsize=24)
cbar.ax.tick_params(labelsize=15)
cbar.set_label("Percentage (%)", size=18)

gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='white', alpha=0.5, linestyle='--', zorder=11)
gl.top_labels = False # suppress gridline labels on the top
gl.right_labels = False # suppress gridline labels at the right edge

ax.set_title('')
#ax.set_title('Time:{}'.format(nice_time), loc='right');
ax.set_title('Anomaly of Precipitation in Percentage (1971 - 2000  & 2071 - 2100) with populated areas (> 500k) in 2093', fontsize=24)
plt.savefig("/lhome/cra2022/l.quirino.2_2022/Quirino_Leonardo/Project/ANOMPercent_Precip_Pop.png", dpi = 300, bbox_inches="tight",pad_inches=0)


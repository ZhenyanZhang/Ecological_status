import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
import matplotlib.patches as mpatches
import os

data=pd.read_excel("Figure1a.xlsx")

lat = np.array(data['latitude'])
lon = np.array(data['longitude'])
Cruise = np.array(data['group'])

plt.style.use('ggplot')
plt.figure(figsize=(10, 6))

# 初始化地图对象,正常坐标
map1 = Basemap(projection='robin', lat_0=90, lon_0=0,
                   resolution='l', area_thresh=1000.0)

map1.drawmeridians(np.arange(0, 360, 60))
map1.drawparallels(np.arange(-90, 90, 30))

map1.drawcoastlines(linewidth=0.2)
map1.drawmapboundary(fill_color='white')
map1.fillcontinents(color='lightgrey', alpha=0.8)

cm = mpl.colors.ListedColormap(['lightgreen','blue','mediumpurple','orange','red','yellow','black','purple'])

map1.scatter(lon, lat, latlon=True,
                alpha=1, s=10, c=Cruise,cmap=cm, linewidths=0, marker='s', zorder=1)

plt.show()
plt.close()
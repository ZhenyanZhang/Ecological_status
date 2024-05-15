import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
import matplotlib.patches as mpatches
import os

data=pd.read_excel("Figure2b.xlsx")

lat = np.array(data['lat'])
lon = np.array(data['lon'])
Cluster = np.array(data['Cluster_Label'])

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

cm = mpl.colors.ListedColormap(['lightgreen','blue','mediumpurple','orange','red','yellow','purple'])

map1.scatter(lon, lat, latlon=True,
                alpha=1, s=10, c=Cluster,cmap=cm, linewidths=0, marker='s', zorder=1)

# create legend
ES1 = mpatches.Patch(color='lightgreen', label='ES1')
ES2 = mpatches.Patch(color='blue', label='ES2')
ES3 = mpatches.Patch(color='mediumpurple', label='ES3')
ES4 = mpatches.Patch(color='orange', label='ES4')
ES5 = mpatches.Patch(color='red', label='ES5')
ES6 = mpatches.Patch(color='yellow', label='ES6')
ES7 = mpatches.Patch(color='purple', label='ES7')
plt.legend(handles=[ES1,ES2,ES3,ES4,ES5,ES6,ES7], title='Ecological Status',loc=1)

plt.show()
plt.close()
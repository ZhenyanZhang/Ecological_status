import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
import matplotlib.patches as mpatches
import os

data=pd.read_excel("Figure 4a.xlsx")

lat = np.array(data['lat'])
lon = np.array(data['lon'])
factor = np.array(data['index'])

plt.style.use('ggplot')
plt.figure(figsize=(10, 6))

map1 = Basemap(projection='robin', lat_0=90, lon_0=0,
                   resolution='l', area_thresh=1000.0)

map1.drawmeridians(np.arange(0, 360, 60))
map1.drawparallels(np.arange(-90, 90, 30))

map1.drawcoastlines(linewidth=0.2)
map1.drawmapboundary(fill_color='white')
map1.fillcontinents(color='lightgrey', alpha=0.8)



cm = mpl.colors.ListedColormap(['lightgreen','blue','mediumpurple','orange','red','yellow','purple','lightgrey','black','skyblue'])

map1.scatter(lon, lat, latlon=True,
                alpha=1, s=5, c=factor,cmap=cm, linewidths=0, marker='s', zorder=1)

# create legend
Factor1 = mpatches.Patch(color='lightgreen', label='Factor1')
Factor2 = mpatches.Patch(color='blue', label='Factor2')
Factor3 = mpatches.Patch(color='mediumpurple', label='Factor3')
Factor4 = mpatches.Patch(color='orange', label='Factor4')
Factor5 = mpatches.Patch(color='red', label='Factor5')
Factor6 = mpatches.Patch(color='yellow', label='Factor6')
Factor7 = mpatches.Patch(color='purple', label='Factor7')
Factor8 = mpatches.Patch(color='lightgrey', label='Factor8')
Factor9 = mpatches.Patch(color='black', label='Factor9')
Factor10 = mpatches.Patch(color='skyblue', label='Factor10')
plt.legend(handles=[Factor1,Factor2,Factor3,Factor4,Factor5,Factor6,Factor7,Factor8,Factor9,Factor10], title='Environmental factor',loc=1)

plt.show()
plt.close()
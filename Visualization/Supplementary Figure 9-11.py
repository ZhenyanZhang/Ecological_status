import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
import matplotlib.patches as mpatches
import os
import matplotlib.colors as mcolors


path = r"Supplementary Figure 9-11.csv"
files = glob.glob(path)
print(files)
plt.style.use('ggplot')
plt.figure(figsize=(10, 6))

for file in files:
    data=pd.read_csv(file)
    file_name = os.path.basename(file)
    file_name_without_extension = os.path.splitext(file_name)[0]
    print(file_name_without_extension)

    for col in data.columns[3:28]:

        map1 = Basemap(projection='robin', lat_0=90, lon_0=0,
                       resolution='l', area_thresh=1000.0)

        map1.drawcoastlines(linewidth=0.2)
        map1.drawmapboundary(fill_color='white')
        map1.fillcontinents(color='lightgrey', alpha=0.5)

        map1.drawmeridians(np.arange(0, 360, 60))
        map1.drawparallels(np.arange(-90, 90, 30))
        lat = data['lat']
        lon = data['lon']

        map1.scatter(lon, lat, latlon=True,
                     alpha=1, s=3.3, c=data[col],cmap='RdBu_r', linewidths=0, marker='s')
        #plt.colorbar()
        #plt.title(col)
        outfigure = "D:/Figures_2023/" + col + ".png"
        print(outfigure)
        plt.savefig(outfigure, dpi=300)
        plt.close()


import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import os
from matplotlib.ticker import MultipleLocator
import matplotlib.colors as mcolors


# 文件路径
path = r"Micro_changed_under_*_scenario.csv"
files = glob.glob(path)
plt.style.use('ggplot')

for file in files:
    data = pd.read_csv(file)
    print(data)
    file_name = os.path.basename(file)
    file_name_without_extension = os.path.splitext(file_name)[0]

    fig, axs = plt.subplots(nrows=4, ncols=3, figsize=(9, 7))
    axs = axs.ravel()

    used_axes = 0

    for idx, col in enumerate(data.columns[3:13]):
        ax = axs[idx]
        map1 = Basemap(projection='robin', lat_0=0, lon_0=0, resolution='c', ax=ax)
        map1.drawcoastlines()
        map1.fillcontinents(color='lightgray',lake_color='aqua')
        map1.drawmapboundary(fill_color='aqua')
        map1.drawmeridians(np.arange(0, 360, 30))
        map1.drawparallels(np.arange(-90, 90, 30))

        lat = data['lat']
        lon = data['lon']
        pred = data[col]

        norm = mcolors.TwoSlopeNorm(vmin=-10, vcenter=0, vmax=10)

        x, y = map1(lon.values, lat.values)
        sc = map1.scatter(x, y, c=pred, cmap='RdBu_r',  s=10, norm=norm, edgecolors=None, linewidth=0)

        ax.set_title(col, fontsize=10)

        used_axes += 1


    plt.tight_layout(pad=0.1, h_pad=0.1)
    for ax in axs[used_axes:]:
        ax.set_visible(False)

    cbar = fig.colorbar(sc, ax=axs, orientation='horizontal', fraction=0.025, pad=0.04)
    cbar.locator = MultipleLocator(1)
    cbar.update_ticks()

    outfigure = f"D:/factor_change/{file_name_without_extension}_combined.png"
    plt.savefig(outfigure, dpi=300)
    #plt.show()
    plt.close()

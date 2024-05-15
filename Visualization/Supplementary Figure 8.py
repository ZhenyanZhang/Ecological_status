import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_path = 'FigureS8.csv'

#load data
df = pd.read_csv(data_path)

print(df)


fig, ax = plt.subplots(figsize=(12, 8))

# plot
for _, sample_df in df.groupby('Variable'):
    ax.plot(sample_df['Model'], sample_df['R2_test'], '-o', color='black',  alpha=0.3, zorder=3)  # or R2_overall

groups = df['Model'].unique()
boxplot_data = [df[df['Model'] == group]['R2_test'].values for group in groups]

positions = np.arange(len(groups))
boxplot_result =ax.boxplot(boxplot_data, positions=positions, widths=0.3, patch_artist=True, zorder=2)

for box in boxplot_result['boxes']:
    box.set_facecolor('none')
    box.set_edgecolor('black')
    box.set_linewidth(2)

for median in boxplot_result['medians']:
    median.set_color('black')
    median.set_linewidth(3)

for whisker in boxplot_result['whiskers']:
    whisker.set_linewidth(2)

for cap in boxplot_result['caps']:
    cap.set_linewidth(2)

ax.set_xticks(positions)
ax.set_xticklabels(groups)


plt.grid(False)
plt.tight_layout()
plt.show()
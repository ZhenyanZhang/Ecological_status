import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
from scipy.stats import kruskal

# loading data
data_path = 'predictions_2023_RF.csv'
df = pd.read_csv(data_path)

# pre-
X = df.iloc[:, 13:]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#PCA
pca_95 = PCA(n_components=0.95)
X_pca_95 = pca_95.fit_transform(X_scaled)


# selected hyperparameter
n_clusters = 7
linkage_method = 'ward'
metric = 'euclidean'

# Hierarchical clustering with selected hyperparameter
clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage_method, metric=metric)
cluster_labels = clustering.fit_predict(X_pca_95)
# added the cluster label into original
df['Cluster_Label'] = cluster_labels

# results saving
output_path = 'cluster results.csv'
df.to_csv(output_path, index=False)

print(f"Results saved to {output_path}")

# PCA for visualization (only top three principal components
pca_3 = PCA(n_components=3)
X_pca_3 = pca_3.fit_transform(X_scaled)

# Kruskal-Wallis H test for three principal components
for i in range(3):
    groups = [X_pca_3[cluster_labels == j, i] for j in range(n_clusters)]
    stat, p = kruskal(*groups)
    print(f'Kruskal-Wallis H test for PCA Component {i+1}: Statistics={stat:.3f}, p={p:.3f}')



# obtaining explained variance ratio for each principal component
explained_variance_ratio = pca_3.explained_variance_ratio_
explained_variance_ratio_percentage = ['{:.2%}'.format(v) for v in explained_variance_ratio]

# PCA  visualization
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter(X_pca_3[:, 0], X_pca_3[:, 1], X_pca_3[:, 2], c=cluster_labels, cmap='Set1', marker='o', edgecolor='k', s=50)
ax.set_xlabel(f'PC1 ({explained_variance_ratio_percentage[0]})')
ax.set_ylabel(f'PC2 ({explained_variance_ratio_percentage[1]})')
ax.set_zlabel(f'PC3 ({explained_variance_ratio_percentage[2]})')
plt.colorbar(sc, label='Cluster Label')
plt.show()



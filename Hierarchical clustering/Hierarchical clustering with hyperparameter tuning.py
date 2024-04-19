import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score

# loading data
data_path = 'predictions_2023_RF.csv'
df = pd.read_csv(data_path)

# pre-
X = df.iloc[:, 13:]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA
pca = PCA(n_components=0.95)
X_pca = pca.fit_transform(X_scaled)
print(f"Original number of features: {X_scaled.shape[1]}, reduced to: {X_pca.shape[1]} after PCA")

# hyperparameter tuning
range_n_clusters = [5,6,7,8,9,10]
linkage_methods = ['ward', 'complete', 'average', 'single']
distance_metrics = {
    'ward': ['euclidean'],
    'complete': ['euclidean', 'manhattan', 'cosine'],
    'average': ['euclidean', 'manhattan', 'cosine'],
    'single': ['euclidean', 'manhattan', 'cosine']
}


results = []

# Hierarchical clustering with hyperparameter tuning
for n_clusters in range_n_clusters:
    print(n_clusters)
    for linkage_method in linkage_methods:
        print(linkage_method)
        for metric in distance_metrics[linkage_method]:
            print(metric)
            clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage_method, metric=metric)
            cluster_labels = clustering.fit_predict(X_pca)
            silhouette_avg = silhouette_score(X_pca, cluster_labels)

            print(silhouette_avg)

            results.append({
                'n_clusters': n_clusters,
                'linkage_method': linkage_method,
                'metric': metric,
                'silhouette_score': silhouette_avg
            })


results_df = pd.DataFrame(results)
print(results_df)

# results saving
results_df.to_csv('results of hyperparameter tuning.csv', index=False)

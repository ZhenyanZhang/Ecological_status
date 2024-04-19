import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

# loading data
df = pd.read_csv('data_for_classifier_random_sample.csv')
category_column = 'ES'

# random sampling
n_samples_per_class = 3000
sampled_dfs = []
for category, group in df.groupby(category_column):
    sampled = group.sample(n=n_samples_per_class, replace=True) if len(group) > n_samples_per_class else group
    sampled_dfs.append(sampled)
sampled_df = pd.concat(sampled_dfs)

# data saving (sampled)
sampled_df.to_csv('RANDOM_sampled_dataset.csv', index=False)

# data saving (remaining)
remaining_df = pd.concat([df, sampled_df]).drop_duplicates(keep=False)
remaining_df.to_csv('remaining_dataset.csv', index=False)

# verification for sampling (correlation between features)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
sns.heatmap(df.corr(), ax=axes[0], annot=False, cmap='coolwarm', fmt=".2f")
axes[0].set_title("Correlation Matrix of Original Dataset")
sns.heatmap(sampled_df.corr(), ax=axes[1], annot=False, cmap='coolwarm', fmt=".2f")
axes[1].set_title("Correlation Matrix of Sampled Dataset")
plt.tight_layout()
plt.show()

# verification for sampling (pca)
pca = PCA(n_components=2)
original_pca_fitted = pca.fit(df.select_dtypes(include=[np.number]).fillna(0))
original_pca = original_pca_fitted.transform(df.select_dtypes(include=[np.number]).fillna(0))
sampled_pca = original_pca_fitted.transform(sampled_df.select_dtypes(include=[np.number]).fillna(0))

# obtaining explained variance ratio
explained_variance_ratio = pca.explained_variance_ratio_

plt.figure(figsize=(12, 6))
plt.scatter(original_pca[:, 0], original_pca[:, 1], alpha=0.2, label="Original Dataset")
plt.scatter(sampled_pca[:, 0], sampled_pca[:, 1], alpha=0.2, label="Sampled Dataset")
plt.legend()
plt.xlabel(f"PC1 ({explained_variance_ratio[0]:.2%} explained)")
plt.ylabel(f"PC2 ({explained_variance_ratio[1]:.2%} explained)")
plt.title("PCA of Original vs. Sampled Dataset")
plt.show()
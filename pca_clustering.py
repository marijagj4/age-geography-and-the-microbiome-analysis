import matplotlib.pyplot as plt
import pandas as pd

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def run_pca_clustering(
        merged,
        bacteria_columns
):

    sampled = merged.sample(
        10000,
        random_state=42
    )

    print("\n========== PCA + CLUSTERING ==========\n")

    X = sampled[
        bacteria_columns
    ].fillna(0)

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=2)

    pca_result = pca.fit_transform(
        X_scaled
    )

    sampled["PC1"] = pca_result[:, 0]
    sampled["PC2"] = pca_result[:, 1]

    plt.figure(figsize=(10, 6))

    for region in sampled["region"].unique():

        subset = sampled[
            sampled["region"] == region
        ]

        plt.scatter(
            subset["PC1"],
            subset["PC2"],
            label=region,
            alpha=0.6
        )

    plt.title("PCA of Microbiome Data")

    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")

    plt.legend()

    plt.show()

    # KMeans clustering
    kmeans = KMeans(
        n_clusters=3,
        random_state=42
    )

    sampled["cluster"] = kmeans.fit_predict(
        X_scaled
    )

    plt.figure(figsize=(10, 6))

    for cluster in sampled["cluster"].unique():

        subset = sampled[
            sampled["cluster"] == cluster
        ]

        plt.scatter(
            subset["PC1"],
            subset["PC2"],
            label=f"Cluster {cluster}",
            alpha=0.6
        )

    plt.title(
        "KMeans Clustering of Microbiome Samples"
    )

    plt.xlabel("PC1")
    plt.ylabel("PC2")

    plt.legend()

    plt.show()

    cluster_region = pd.crosstab(
        sampled["cluster"],
        sampled["region"]
    )

    print("\nCluster vs Region:")

    print(cluster_region)

    return merged
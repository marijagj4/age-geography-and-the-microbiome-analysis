import matplotlib.pyplot as plt
import pandas as pd

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def run_pca_clustering(
        merged,
        bacteria_columns
):

    print("\n========== PCA + CLUSTERING ==========\n")

    X = merged[
        bacteria_columns
    ].fillna(0)

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=2)

    pca_result = pca.fit_transform(
        X_scaled
    )

    merged["PC1"] = pca_result[:, 0]
    merged["PC2"] = pca_result[:, 1]

    plt.figure(figsize=(10, 6))

    for region in merged["region"].unique():

        subset = merged[
            merged["region"] == region
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

    merged["cluster"] = kmeans.fit_predict(
        X_scaled
    )

    plt.figure(figsize=(10, 6))

    for cluster in merged["cluster"].unique():

        subset = merged[
            merged["cluster"] == cluster
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
        merged["cluster"],
        merged["region"]
    )

    print("\nCluster vs Region:")

    print(cluster_region)

    return merged
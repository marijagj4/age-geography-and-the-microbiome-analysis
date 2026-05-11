import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
metadata = pd.read_csv("sample_metadata (2).tsv", sep="\t")

print(metadata.head())
print(metadata.shape)
print(metadata.columns)
print(metadata.isnull().sum())
print(metadata["region"].value_counts())
metadata["region"].value_counts().plot(kind="bar")

plt.xlabel("Region")
plt.ylabel("Number of samples")
plt.title("Samples by Region")

plt.xticks(rotation=45)

plt.show()

tags = pd.read_csv("tags (1).tsv.gz", sep="\t", compression="gzip", low_memory=False)

print(tags.head())

print(tags.shape)

print(tags.columns)
print(tags["tag"].unique())

age_data = tags[tags["tag"] == "age"]

print(age_data.head())

print(age_data.shape)
age_data["value"] = pd.to_numeric(age_data["value"], errors="coerce")

print(age_data["value"].describe())
age_clean = age_data[(age_data["value"] >= 0) & (age_data["value"] <= 120)]

print(age_clean["value"].describe())
plt.hist(age_clean["value"], bins=20)

plt.xlabel("Age")
plt.ylabel("Number of samples")
plt.title("Age Distribution")

plt.show()
# taxa = pd.read_csv("taxonomic_table.csv.gz", compression="gzip", low_memory=False)
#
# print(taxa.head())
#
# print(taxa.shape)
#
# print(taxa.columns)
taxa = pd.read_csv(
    "taxonomic_table.csv.gz",
    compression="gzip",
    low_memory=False,
    nrows=5000
)

print(taxa.head())

print(taxa.shape)

print(taxa.columns)
print(taxa.isnull().sum().sum())
bacteria_sums = taxa.iloc[:, 2:].sum().sort_values(ascending=False)

print(bacteria_sums.head(10))
print(taxa["sample"].head())
taxa["srr"] = taxa["sample"].str.split("_").str[1]

print(taxa[["sample", "srr"]].head())

metadata_small = metadata[["srr", "region", "iso"]]

print(metadata_small.head())
age_small = age_clean[["srr", "value"]]

age_small = age_small.rename(columns={"value": "age"})

print(age_small.head())
merged = taxa.merge(metadata_small, on="srr", how="left")

merged = merged.merge(age_small, on="srr", how="left")

print(merged.head())

print(merged.shape)

top_bacteria = taxa.drop(
    columns=["Unnamed: 0", "sample", "srr", "region", "iso", "age"],
    errors="ignore"
).sum()
top10 = top_bacteria.sort_values(ascending=False).head(10)

print(top10)

import matplotlib.pyplot as plt

top10.plot(kind="bar")

plt.title("Top 10 Most Abundant Bacteria")
plt.xlabel("Bacteria")
plt.ylabel("Abundance")

plt.xticks(rotation=90)

plt.show()

plt.scatter(
    merged["age"],
    merged["Bacteria.Bacteroidota.Bacteroidia.Bacteroidales.Bacteroidaceae.Bacteroides"]
)

plt.xlabel("Age")
plt.ylabel("Bacteroides abundance")
plt.title("Age vs Bacteroides")

plt.show()
correlation = merged["age"].corr(
    merged["Bacteria.Bacteroidota.Bacteroidia.Bacteroidales.Bacteroidaceae.Bacteroides"]
)

print(correlation)

region_bacteria = merged.groupby("region")[
    "Bacteria.Bacteroidota.Bacteroidia.Bacteroidales.Bacteroidaceae.Bacteroides"
].mean()

print(region_bacteria)

region_bacteria.plot(kind="bar")

plt.title("Average Bacteroides Abundance by Region")
plt.xlabel("Region")
plt.ylabel("Average Abundance")

plt.xticks(rotation=45)

plt.show()

asia = merged[
    merged["region"] == "Eastern and South-Eastern Asia"
]

bacteria_columns = merged.select_dtypes(
    include="number"
).columns

bacteria_columns = bacteria_columns.drop(
    ["Unnamed: 0", "age"],
    errors="ignore"
)

asia_bacteria = asia[bacteria_columns].sum()

top_asia = asia_bacteria.sort_values(
    ascending=False
).head(10)

print(top_asia)

top_asia.plot(kind="bar")

plt.title("Top 10 Bacteria in Asia")

plt.xlabel("Bacteria")

plt.ylabel("Abundance")

plt.xticks(rotation=90)

plt.show()

# =========================
# TOP BACTERIA IN EUROPE
# =========================

europe = merged[
    merged["region"] == "Europe and Northern America"
]

bacteria_columns = merged.select_dtypes(
    include="number"
).columns

bacteria_columns = bacteria_columns.drop(
    ["Unnamed: 0", "age"],
    errors="ignore"
)

europe = merged[
    merged["region"] == "Europe and Northern America"
]

print(europe.shape)

print(
    europe[
        "Bacteria.Bacteroidota.Bacteroidia.Bacteroidales.Bacteroidaceae.Bacteroides"
    ].head()
)

europe_bacteria = europe[bacteria_columns].sum()

top_europe = europe_bacteria.sort_values(
    ascending=False
).head(10)

print(top_europe)

top_europe.plot(kind="bar")

plt.title("Top 10 Bacteria in Europe and Northern America")

plt.xlabel("Bacteria")

plt.ylabel("Abundance")

plt.xticks(rotation=90)

plt.show()


# =========================
# TOP BACTERIA IN AFRICA
# =========================

africa = merged[
    merged["region"] == "Sub-Saharan Africa"
]

africa_bacteria = africa[bacteria_columns].sum()

top_africa = africa_bacteria.sort_values(
    ascending=False
).head(10)

print(top_africa)

top_africa.plot(kind="bar")

plt.title("Top 10 Bacteria in Africa")

plt.xlabel("Bacteria")

plt.ylabel("Abundance")

plt.xticks(rotation=90)

plt.show()


# =========================
# COMPARISON BETWEEN REGIONS
# =========================

comparison = pd.DataFrame({
    "Asia": top_asia,
    "Europe": top_europe,
    "Africa": top_africa
}).fillna(0)

print(comparison)

comparison.plot(kind="bar", figsize=(14,7))

plt.title("Comparison of Top Bacteria Between Regions")

plt.xlabel("Bacteria")

plt.ylabel("Abundance")

plt.xticks(rotation=90)

plt.show()

top_bacteria_names = top10.index

heatmap_data = merged[top_bacteria_names]

corr_matrix = heatmap_data.corr()

print(corr_matrix)

plt.figure(figsize=(10,8))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlation Heatmap of Top Bacteria")

plt.show()

# =========================================
# BACTERIA CORRELATION ANALYSIS
# =========================================


# =========================================
# 1. STRONGEST POSITIVE CORRELATIONS
# =========================================

print("\nSTRONGEST POSITIVE CORRELATIONS\n")

corr_pairs = corr_matrix.unstack()

corr_pairs = corr_pairs.sort_values(
    ascending=False
)

print(corr_pairs.head(20))


# =========================================
# 2. STRONGEST NEGATIVE CORRELATIONS
# =========================================

print("\nSTRONGEST NEGATIVE CORRELATIONS\n")

corr_pairs = corr_matrix.unstack()

corr_pairs = corr_pairs.sort_values()

print(corr_pairs.head(20))


# =========================================
# 3. BACTEROIDES VS ALL BACTERIA
# =========================================

print("\nBACTEROIDES VS ALL BACTERIA\n")

bacteroides_corr = corr_matrix[
    "Bacteria.Bacteroidota.Bacteroidia.Bacteroidales.Bacteroidaceae.Bacteroides"
]

print(
    bacteroides_corr.sort_values(
        ascending=False
    )
)


# =========================================
# 4. MOST INDEPENDENT BACTERIA
# =========================================

print("\nMOST INDEPENDENT BACTERIA\n")

average_corr = corr_matrix.abs().mean()

print(
    average_corr.sort_values()
)


# =========================================
# 5. MOST CONNECTED BACTERIA
# =========================================

print("\nMOST CONNECTED BACTERIA\n")

average_corr = corr_matrix.abs().mean()

print(
    average_corr.sort_values(
        ascending=False
    )
)


# =========================================
# 6. ASIA CORRELATION HEATMAP
# =========================================

asia_heatmap = asia[top_bacteria_names]

asia_corr = asia_heatmap.corr()

plt.figure(figsize=(10,8))

sns.heatmap(
    asia_corr,
    annot=True,
    cmap="coolwarm"
)

plt.title("Asia Bacteria Correlation Heatmap")

plt.show()


# =========================================
# 7. AFRICA CORRELATION HEATMAP
# =========================================

africa_heatmap = africa[top_bacteria_names]

africa_corr = africa_heatmap.corr()

plt.figure(figsize=(10,8))

sns.heatmap(
    africa_corr,
    annot=True,
    cmap="coolwarm"
)

plt.title("Africa Bacteria Correlation Heatmap")

plt.show()


# =========================================
# 8. EUROPE CORRELATION HEATMAP
# =========================================

europe_heatmap = europe[top_bacteria_names]

europe_corr = europe_heatmap.corr()

plt.figure(figsize=(10,8))

sns.heatmap(
    europe_corr,
    annot=True,
    cmap="coolwarm"
)

plt.title("Europe Bacteria Correlation Heatmap")

plt.show()


# =========================================
# 9. HISTOGRAM OF CORRELATIONS
# =========================================

all_corr_values = corr_matrix.values.flatten()

plt.hist(
    all_corr_values,
    bins=30
)

plt.title("Distribution of Correlations")

plt.xlabel("Correlation")

plt.ylabel("Frequency")

plt.show()


# =========================================
# 10. TOP POSITIVE PAIRS WITHOUT DUPLICATES
# =========================================

print("\nTOP POSITIVE PAIRS WITHOUT DUPLICATES\n")

corr_pairs = corr_matrix.unstack()

corr_pairs = corr_pairs[
    corr_pairs < 1
]

corr_pairs = corr_pairs.sort_values(
    ascending=False
)

print(corr_pairs.head(20))


# =========================================
# 11. TOP NEGATIVE PAIRS WITHOUT DUPLICATES
# =========================================

print("\nTOP NEGATIVE PAIRS WITHOUT DUPLICATES\n")

corr_pairs = corr_matrix.unstack()

corr_pairs = corr_pairs[
    corr_pairs > -1
]

corr_pairs = corr_pairs.sort_values()

print(corr_pairs.head(20))


# =========================================
# 12. BARPLOT OF MOST CONNECTED BACTERIA
# =========================================

average_corr = corr_matrix.abs().mean()

top_connected = average_corr.sort_values(
    ascending=False
)

top_connected.plot(kind="bar")

plt.title("Most Connected Bacteria")

plt.xlabel("Bacteria")

plt.ylabel("Average Correlation")

plt.xticks(rotation=90)

plt.show()

# =========================
# AGE GROUPS ANALYSIS
# =========================

merged["age_group"] = pd.cut(
    merged["age"],
    bins=[0, 20, 40, 60, 120],
    labels=["0-20", "20-40", "40-60", "60+"],
    include_lowest=True
)

print(merged["age_group"].value_counts())


# =========================
# AVERAGE BACTEROIDES BY AGE GROUP
# =========================

age_group_bacteroides = merged.groupby("age_group")[
    "Bacteria.Bacteroidota.Bacteroidia.Bacteroidales.Bacteroidaceae.Bacteroides"
].mean()

print(age_group_bacteroides)

age_group_bacteroides.plot(kind="bar")

plt.title("Average Bacteroides Abundance by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Average Bacteroides Abundance")

plt.xticks(rotation=0)

plt.show()


# =========================
# TOP BACTERIA BY AGE GROUP
# =========================

bacteria_columns = merged.select_dtypes(
    include="number"
).columns

bacteria_columns = bacteria_columns.drop(
    ["Unnamed: 0", "age"],
    errors="ignore"
)

for group in merged["age_group"].dropna().unique():
    group_data = merged[
        merged["age_group"] == group
    ]

    top_group_bacteria = group_data[bacteria_columns].sum().sort_values(
        ascending=False
    ).head(10)

    print("\nTop bacteria for age group:", group)
    print(top_group_bacteria)

    top_group_bacteria.plot(kind="bar")

    plt.title(f"Top 10 Bacteria in Age Group {group}")
    plt.xlabel("Bacteria")
    plt.ylabel("Abundance")
    plt.xticks(rotation=90)

    plt.show()

    # =========================================
    # PCA ANALYSIS
    # =========================================

    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler

    # top bacteria columns
    top_bacteria_columns = top_bacteria.index.tolist()

    # земаме само top bacteria
    pca_data = merged[top_bacteria_columns]

    # scaling
    scaler = StandardScaler()

    scaled_data = scaler.fit_transform(pca_data)

    # PCA
    pca = PCA(n_components=2)

    principal_components = pca.fit_transform(scaled_data)

    # dataframe
    pca_df = pd.DataFrame(
        principal_components,
        columns=["PC1", "PC2"]
    )

    # додаваме region
    pca_df["region"] = merged["region"]

    print(pca_df.head())

    # visualization

    plt.figure(figsize=(10, 7))

    for region in pca_df["region"].dropna().unique():
        region_data = pca_df[
            pca_df["region"] == region
            ]

        plt.scatter(
            region_data["PC1"],
            region_data["PC2"],
            label=region,
            alpha=0.6
        )

    plt.title("PCA of Microbiome Data")

    plt.xlabel("Principal Component 1")

    plt.ylabel("Principal Component 2")

    plt.legend()

    plt.show()

# =========================================
# KMEANS CLUSTERING
# =========================================

from sklearn.cluster import KMeans

# правиме 3 clusters
kmeans = KMeans(
    n_clusters=3,
    random_state=42
)

# алгоритмот ги групира samples според microbiome data
clusters = kmeans.fit_predict(scaled_data)

# ги додаваме cluster резултатите во PCA dataframe
pca_df["cluster"] = clusters

print(pca_df.head())

print("Cluster counts:")
print(pca_df["cluster"].value_counts())


# =========================================
# VISUALIZE CLUSTERS ON PCA
# =========================================

plt.figure(figsize=(10, 7))

for cluster in pca_df["cluster"].unique():

    cluster_data = pca_df[
        pca_df["cluster"] == cluster
    ]

    plt.scatter(
        cluster_data["PC1"],
        cluster_data["PC2"],
        label=f"Cluster {cluster}",
        alpha=0.6
    )

plt.title("KMeans Clustering of Microbiome Samples")

plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")

plt.legend()

plt.show()


# =========================================
# COMPARE CLUSTERS WITH REGIONS
# =========================================

cluster_region_table = pd.crosstab(
    pca_df["cluster"],
    pca_df["region"]
)

print("Cluster vs Region:")
print(cluster_region_table)


cluster_region_table.plot(kind="bar")

plt.title("Cluster Distribution by Region")

plt.xlabel("Cluster")
plt.ylabel("Number of samples")

plt.xticks(rotation=0)

plt.show()

# =========================================
# DIVERSITY ANALYSIS
# =========================================

from scipy.stats import entropy

bacteria_columns = merged.select_dtypes(
    include="number"
).columns

bacteria_columns = bacteria_columns.drop(
    ["Unnamed: 0", "age", "diversity"],
    errors="ignore"
)

def shannon_diversity(row):
    values = row[row > 0]

    if values.sum() == 0:
        return 0

    proportions = values / values.sum()

    return entropy(proportions)

merged["diversity"] = merged[
    bacteria_columns
].apply(
    shannon_diversity,
    axis=1
)

print(merged["diversity"].head())
print(merged["diversity"].describe())


# =========================================
# DIVERSITY BY REGION
# =========================================

region_diversity = merged.groupby(
    "region"
)["diversity"].mean()

print(region_diversity)

region_diversity.plot(kind="bar")

plt.title("Average Microbiome Diversity by Region")
plt.xlabel("Region")
plt.ylabel("Average Diversity")
plt.xticks(rotation=20)

plt.show()


# =========================================
# DIVERSITY BY AGE GROUP
# =========================================

age_diversity = merged.groupby(
    "age_group"
)["diversity"].mean()

print(age_diversity)

age_diversity.plot(kind="bar")

plt.title("Average Microbiome Diversity by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Average Diversity")
plt.xticks(rotation=0)

plt.show()


# =========================================
# DIVERSITY DISTRIBUTION
# =========================================

plt.hist(
    merged["diversity"],
    bins=30
)

plt.title("Distribution of Microbiome Diversity")
plt.xlabel("Diversity")
plt.ylabel("Frequency")

plt.show()


# =========================================
# DIVERSITY VS AGE
# =========================================

plt.scatter(
    merged["age"],
    merged["diversity"],
    alpha=0.5
)

plt.title("Age vs Microbiome Diversity")
plt.xlabel("Age")
plt.ylabel("Diversity")

plt.show()
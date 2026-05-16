import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def run_region_analysis(
        merged,
        bacteria_columns
):

    print("\n========== REGION ANALYSIS ==========\n")

    # =========================================
    # 1. SAMPLES BY REGION
    # =========================================

    region_counts = merged["region"].value_counts()

    print("\nSamples by region:\n")
    print(region_counts)

    print("\nUnique regions:\n")
    print(merged["region"].unique())

    region_counts.plot(
        kind="bar"
    )

    plt.title("Samples by Region")
    plt.xlabel("Region")
    plt.ylabel("Count")

    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()

    plt.show()

    # =========================================
    # 2. TOP 10 BACTERIA OVERALL
    # =========================================

    bacteria_sums = merged[
        bacteria_columns
    ].sum()

    top_bacteria = bacteria_sums.sort_values(
        ascending=False
    ).head(10)

    print("\nTop 10 Bacteria Overall:\n")
    print(top_bacteria)

    # short names for graph
    top_bacteria_short = top_bacteria.copy()

    top_bacteria_short.index = [
        name.split(".")[-1]
        for name in top_bacteria_short.index
    ]

    top_bacteria_short.plot(
        kind="bar"
    )

    plt.title("Top 10 Bacteria Overall")
    plt.xlabel("Bacteria")
    plt.ylabel("Abundance")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.show()

    # =========================================
    # 3. FULL METADATA REGION COUNTS
    # =========================================

    metadata = pd.read_csv(
        "sample_metadata (2).tsv",
        sep="\t"
    )

    print("\nFull metadata region counts:\n")
    print(metadata["region"].value_counts())

    # =========================================
    # 4. REGION VS MICROBIOME HEATMAP
    # =========================================

    # remove unknown region because it is missing metadata
    region_data = merged[
        merged["region"] != "unknown"
    ].copy()

    top_bacteria_names = top_bacteria.index

    region_microbiome = region_data.groupby(
        "region"
    )[top_bacteria_names].mean()

    # make bacteria names shorter for visualization
    short_names = [
        name.split(".")[-1]
        for name in top_bacteria_names
    ]

    region_microbiome.columns = short_names

    print("\nRegion vs Microbiome - Average abundance:\n")
    print(region_microbiome)

    plt.figure(figsize=(14, 8))

    sns.heatmap(
        region_microbiome,
        annot=True,
        fmt=".1f",
        cmap="YlGnBu"
    )

    plt.title("Region vs Microbiome: Average Abundance of Top Bacteria")
    plt.xlabel("Bacteria")
    plt.ylabel("Region")

    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)

    plt.tight_layout()
    plt.show()

    return merged
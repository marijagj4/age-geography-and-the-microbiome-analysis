import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def extract_taxonomy_level(bacteria_name, level):
    parts = str(bacteria_name).split(".")

    if len(parts) > level:
        return parts[level]

    return "Unknown"


def run_taxonomy_analysis(
        merged,
        bacteria_columns
):

    print("\n========== TAXONOMY ANALYSIS ==========\n")

    # =========================================
    # 1. CREATE TAXONOMY TABLE
    # =========================================

    taxonomy_info = pd.DataFrame({
        "bacteria": bacteria_columns
    })

    taxonomy_info["kingdom"] = taxonomy_info["bacteria"].apply(
        lambda x: extract_taxonomy_level(x, 0)
    )

    taxonomy_info["phylum"] = taxonomy_info["bacteria"].apply(
        lambda x: extract_taxonomy_level(x, 1)
    )

    taxonomy_info["class"] = taxonomy_info["bacteria"].apply(
        lambda x: extract_taxonomy_level(x, 2)
    )

    taxonomy_info["order"] = taxonomy_info["bacteria"].apply(
        lambda x: extract_taxonomy_level(x, 3)
    )

    taxonomy_info["family"] = taxonomy_info["bacteria"].apply(
        lambda x: extract_taxonomy_level(x, 4)
    )

    taxonomy_info["genus"] = taxonomy_info["bacteria"].apply(
        lambda x: extract_taxonomy_level(x, 5)
    )

    print("\nTaxonomy table preview:\n")
    print(taxonomy_info.head())

    print("\nNumber of bacteria columns:")
    print(len(bacteria_columns))

    print("\nTop phyla by number of bacteria columns:\n")
    print(taxonomy_info["phylum"].value_counts().head(10))

    # =========================================
    # 2. TOP PHYLUM OVERALL
    # =========================================

    phylum_abundance = {}

    for phylum in taxonomy_info["phylum"].unique():

        cols = taxonomy_info[
            taxonomy_info["phylum"] == phylum
        ]["bacteria"]

        abundance = merged[
            cols
        ].sum().sum()

        phylum_abundance[phylum] = abundance

    phylum_abundance = pd.Series(
        phylum_abundance
    ).sort_values(
        ascending=False
    )

    print("\nTop Phylum Overall:\n")
    print(phylum_abundance.head(10))

    phylum_abundance.head(10).plot(
        kind="bar"
    )

    plt.title("Top 10 Phyla Overall")
    plt.xlabel("Phylum")
    plt.ylabel("Total Abundance")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.show()

    # =========================================
    # 3. TOP GENUS OVERALL
    # =========================================

    genus_abundance = {}

    for genus in taxonomy_info["genus"].unique():

        cols = taxonomy_info[
            taxonomy_info["genus"] == genus
        ]["bacteria"]

        abundance = merged[
            cols
        ].sum().sum()

        genus_abundance[genus] = abundance

    genus_abundance = pd.Series(
        genus_abundance
    ).sort_values(
        ascending=False
    )

    print("\nTop Genus Overall:\n")
    print(genus_abundance.head(10))

    genus_abundance.head(10).plot(
        kind="bar"
    )

    plt.title("Top 10 Genus Overall")
    plt.xlabel("Genus")
    plt.ylabel("Total Abundance")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.show()

    # =========================================
    # 4. REGION VS PHYLUM
    # =========================================

    region_data = merged[
        merged["region"] != "unknown"
    ].copy()

    top_phyla = phylum_abundance.head(8).index

    region_phylum = pd.DataFrame()

    for phylum in top_phyla:

        cols = taxonomy_info[
            taxonomy_info["phylum"] == phylum
        ]["bacteria"]

        region_phylum[phylum] = region_data.groupby(
            "region"
        )[cols].mean().sum(axis=1)

    print("\nRegion vs Phylum:\n")
    print(region_phylum)

    plt.figure(figsize=(12, 7))

    sns.heatmap(
        region_phylum,
        annot=True,
        fmt=".1f",
        cmap="YlGnBu"
    )

    plt.title("Region vs Phylum: Average Abundance")
    plt.xlabel("Phylum")
    plt.ylabel("Region")

    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)

    plt.tight_layout()
    plt.show()

    # =========================================
    # 5. AGE GROUP VS PHYLUM
    # =========================================

    if "age_group" in merged.columns:

        age_phylum = pd.DataFrame()

        for phylum in top_phyla:

            cols = taxonomy_info[
                taxonomy_info["phylum"] == phylum
            ]["bacteria"]

            age_phylum[phylum] = merged.groupby(
                "age_group"
            )[cols].mean().sum(axis=1)

        print("\nAge Group vs Phylum:\n")
        print(age_phylum)

        plt.figure(figsize=(12, 6))

        sns.heatmap(
            age_phylum,
            annot=True,
            fmt=".1f",
            cmap="YlGnBu"
        )

        plt.title("Age Group vs Phylum: Average Abundance")
        plt.xlabel("Phylum")
        plt.ylabel("Age Group")

        plt.xticks(rotation=45, ha="right")
        plt.yticks(rotation=0)

        plt.tight_layout()
        plt.show()

    return merged
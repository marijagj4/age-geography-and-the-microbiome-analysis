import matplotlib.pyplot as plt

from scipy.stats import entropy


def run_diversity_analysis(
        merged,
        bacteria_columns
):

    print("\n========== DIVERSITY ANALYSIS ==========\n")

    numeric_bacteria = merged[
        bacteria_columns
    ].select_dtypes(include="number").columns

    def shannon_diversity(row):

        values = row[row > 0]

        if values.sum() == 0:
            return 0

        proportions = values / values.sum()

        return entropy(proportions)

    merged["diversity"] = merged[
        numeric_bacteria
    ].apply(
        shannon_diversity,
        axis=1
    )

    print(
        merged["diversity"].describe()
    )

    # diversity by region
    region_diversity = merged.groupby(
        "region"
    )["diversity"].mean()

    print(region_diversity)

    region_diversity.plot(
        kind="bar"
    )

    plt.title(
        "Average Microbiome Diversity by Region"
    )

    plt.xlabel("Region")
    plt.ylabel("Average Diversity")

    plt.xticks(rotation=20)

    plt.show()

    # diversity by age group
    age_diversity = merged.groupby(
        "age_group"
    )["diversity"].mean()

    print(age_diversity)

    age_diversity.plot(
        kind="bar"
    )

    plt.title(
        "Average Microbiome Diversity by Age Group"
    )

    plt.xlabel("Age Group")
    plt.ylabel("Average Diversity")

    plt.show()

    # histogram
    plt.hist(
        merged["diversity"],
        bins=30
    )

    plt.title(
        "Distribution of Microbiome Diversity"
    )

    plt.xlabel("Diversity")
    plt.ylabel("Frequency")

    plt.show()

    # age vs diversity
    plt.scatter(
        merged["age"],
        merged["diversity"],
        alpha=0.5
    )

    plt.title(
        "Age vs Microbiome Diversity"
    )

    plt.xlabel("Age")
    plt.ylabel("Diversity")

    plt.show()
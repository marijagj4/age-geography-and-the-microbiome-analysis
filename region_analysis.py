import matplotlib.pyplot as plt


def run_region_analysis(
        merged,
        bacteria_columns
):

    print("\n========== REGION ANALYSIS ==========\n")

    region_counts = merged["region"].value_counts()

    print(region_counts)

    region_counts.plot(
        kind="bar"
    )

    plt.title("Samples by Region")
    plt.xlabel("Region")
    plt.ylabel("Count")

    plt.xticks(rotation=20)

    plt.show()

    return merged
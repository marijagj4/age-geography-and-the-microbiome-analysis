import pandas as pd
import matplotlib.pyplot as plt


def run_age_analysis(tags, merged, bacteria_columns):
    print("\n=========================")
    print("AGE ANALYSIS")
    print("=========================")

    # =========================
    # 1. EXTRACT AGE DATA
    # =========================

    age_data = tags[
        tags["tag"] == "age"
    ].copy()

    print(age_data.head())
    print(age_data.shape)

    # =========================
    # 2. CLEAN AGE VALUES
    # =========================

    age_data["value"] = pd.to_numeric(
        age_data["value"],
        errors="coerce"
    )

    print(age_data["value"].describe())

    age_clean = age_data[
        (age_data["value"] >= 0) &
        (age_data["value"] <= 120)
    ].copy()

    print(age_clean["value"].describe())

    # =========================
    # 3. AGE HISTOGRAM
    # =========================

    plt.hist(
        age_clean["value"],
        bins=20
    )

    plt.xlabel("Age")
    plt.ylabel("Number of samples")
    plt.title("Age Distribution")

    plt.show()

    # =========================
    # 4. AGE VS BACTEROIDES
    # =========================

    bacteroides = "Bacteria.Bacteroidota.Bacteroidia.Bacteroidales.Bacteroidaceae.Bacteroides"

    plt.scatter(
        merged["age"],
        merged[bacteroides]
    )

    plt.xlabel("Age")
    plt.ylabel("Bacteroides abundance")
    plt.title("Age vs Bacteroides")

    plt.show()

    # =========================
    # 5. AGE CORRELATION
    # =========================

    correlation = merged["age"].corr(
        merged[bacteroides]
    )

    print("Correlation between age and Bacteroides:")
    print(correlation)

    # =========================
    # 6. AGE GROUPS
    # =========================

    merged["age_group"] = pd.cut(
        merged["age"],
        bins=[0, 20, 40, 60, 120],
        labels=["0-20", "20-40", "40-60", "60+"],
        include_lowest=True
    )

    print(merged["age_group"].value_counts())

    # =========================
    # 7. AVERAGE BACTEROIDES BY AGE GROUP
    # =========================

    age_group_bacteroides = merged.groupby(
        "age_group"
    )[bacteroides].mean()

    print(age_group_bacteroides)

    age_group_bacteroides.plot(kind="bar")

    plt.title("Average Bacteroides Abundance by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Average Bacteroides Abundance")
    plt.xticks(rotation=0)

    plt.show()

    # =========================
    # 8. TOP BACTERIA BY AGE GROUP
    # =========================

    for group in merged["age_group"].dropna().unique():

        group_data = merged[
            merged["age_group"] == group
        ]

        top_group_bacteria = group_data[
            bacteria_columns
        ].sum().sort_values(
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

    return merged